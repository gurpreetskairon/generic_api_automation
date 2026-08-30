"""
dynamic_tokens.py

Resolves two kinds of tokens embedded in raw CSV cell values (payloads,
QUERY_STRING, VALIDATE_DATA, etc.) BEFORE the {placeholder} substitution
step runs:

  <name>          -> VARIABLE lookup (no parentheses, ever). Value comes
                     from VARIABLES, set via set_variable().
  <name()>        -> FUNCTION call with zero args. Parentheses are always
                     required for a function call, even when there are no
                     arguments to pass — this is what disambiguates a call
                     from a variable reference.
  <name(a, b)>    -> FUNCTION call with args.

Usage in a CSV cell:
    "auditId":"<generate_uuid()>"
    "{request_date_time}":<resolve_date_token()>
    "{expiry}":<resolve_date_token("%Y-%m-%d", 7)>
    "{amount}":<random_int(1000,9999)>
    "{client_id}":"<base_client_id>"        <- variable, set elsewhere via
                                                set_variable("base_client_id", ...)

Add new token functions anywhere by decorating them with @register_token.
"""

import ast
import json
import random
import re
import uuid
from datetime import datetime, timedelta, timezone
from typing import Any, Callable, Dict

# --------------------------------------------------------------------------
# 1. Registry
# --------------------------------------------------------------------------

TOKEN_REGISTRY: Dict[str, Callable[..., Any]] = {}

# Plain variable lookups — <name> with NO parentheses at all.
# Populate via set_variable(), e.g. once per test run or per row.
VARIABLES: Dict[str, Any] = {}


def register_token(name: str):
    """
    Decorator: registers a function under the name used in CSV cells.
    Function tokens ALWAYS require parentheses in the CSV, even with no
    args, e.g. @register_token("generate_uuid") -> usable as
    <generate_uuid()>  (NOT <generate_uuid> — that's a variable lookup).
    """
    def _wrap(fn: Callable[..., Any]):
        TOKEN_REGISTRY[name] = fn
        return fn
    return _wrap


def set_variable(name: str, value: Any) -> None:
    """Registers a plain value usable in CSV cells as <name> (no parens)."""
    if name in TOKEN_REGISTRY:
        import warnings
        warnings.warn(
            f"'{name}' is registered as both a function and a variable. "
            f"Bare '<{name}>' will always resolve to the FUNCTION (called "
            f"with zero args) — the variable value is unreachable except "
            f"via a differently-named token.",
            stacklevel=2,
        )
    VARIABLES[name] = value


# --------------------------------------------------------------------------
# 2. Built-in token functions — add your own here or in another module,
#    as long as it's imported before resolve_dynamic_tokens() is called.
# --------------------------------------------------------------------------
#
# @register_token("generate_uuid")
# def generate_uuid() -> str:
#     return str(uuid.uuid4())
# # CSV usage: <generate_uuid()>  -- note the () even though there are no args


# @register_token("resolve_date_token")
# def resolve_date_token(fmt: str = "%Y-%m-%dT%H:%M:%SZ", offset_days: int = 0) -> str:
#     dt = datetime.now(timezone.utc) + timedelta(days=offset_days)
#     return dt.strftime(fmt)
# # CSV usage: <resolve_date_token()>  or  <resolve_date_token("%Y-%m-%d", 7)>


@register_token("random_int")
def random_int(min_val: int = 1, max_val: int = 999999) -> int:
    return random.randint(min_val, max_val)
# CSV usage: <random_int()>  or  <random_int(1000, 9999)>


# Example of a token that needs an argument pulled from elsewhere in your
# framework (e.g. an env value) — just have the CSV pass it explicitly:
#   <lookup_env("BASE_CLIENT_ID")>
@register_token("lookup_env")
def lookup_env(var_name: str, default: str = "") -> str:
    import os
    return os.getenv(var_name, default)


# --------------------------------------------------------------------------
# 3. Core resolution logic
# --------------------------------------------------------------------------

# Group 1: name. Group 2: the WHOLE "(...)" chunk, or None if absent.
# Group 3: just the inner contents of the parens (may be "").
# It's group 2 being None vs "" that tells us variable vs zero-arg call —
# NOT whether the name happens to exist in one registry or the other.
_QUOTED_TOKEN = re.compile(r'"<([A-Za-z_]\w*)(\((.*?)\))?>"')
_BARE_TOKEN = re.compile(r'<([A-Za-z_]\w*)(\((.*?)\))?>')


def _parse_args(arg_str: str):
    """
    Turns the raw text inside the parentheses into real Python args.
    Wrapping in [...] lets ast.literal_eval safely handle multiple args,
    strings, numbers, nested lists/dicts, without a fragile comma-split.
    """
    if not arg_str or not arg_str.strip():
        return []
    try:
        return ast.literal_eval(f"[{arg_str}]")
    except (ValueError, SyntaxError) as e:
        raise ValueError(f"Could not parse token arguments '{arg_str}': {e}")


def _resolve_token(name: str, paren_group: str, arg_str: str) -> Any:
    """
    paren_group is the regex's group(2): None if the CSV wrote <name>
    with no parens, or a string like "()" / "(1,2)" if it wrote
    <name(...)> explicitly.

    Resolution order:
      - Parens present  -> ALWAYS a function call (args parsed and passed).
                            <name> must be in TOKEN_REGISTRY or this errors.
      - Parens absent   -> try TOKEN_REGISTRY first, called with zero args
                            (covers "<generate_uuid>" used as shorthand for
                            "<generate_uuid()>"). If no such function exists,
                            fall back to VARIABLES.
    """
    if paren_group is not None:
        if name not in TOKEN_REGISTRY:
            raise KeyError(
                f"No token FUNCTION registered for '<{name}(...)>'. "
                f"Known functions: {sorted(TOKEN_REGISTRY.keys())}"
            )
        args = _parse_args(arg_str or "")
        return TOKEN_REGISTRY[name](*args)

    # No parens: zero-arg function shorthand takes priority over variables.
    if name in TOKEN_REGISTRY:
        return TOKEN_REGISTRY[name]()
    if name in VARIABLES:
        return VARIABLES[name]

    raise KeyError(
        f"'<{name}>' is neither a registered function nor a registered "
        f"variable. Known functions: {sorted(TOKEN_REGISTRY.keys())}. "
        f"Known variables: {sorted(VARIABLES.keys())}."
    )


def resolve_dynamic_tokens(raw_text: str) -> str:
    """
    Scans raw_text for <function_name> / <function_name(args)> tokens and
    replaces each with the function's return value.

    - "<token>"  (quoted)  -> function must return something str()-able;
                              result is re-wrapped in quotes, JSON-escaped.
    - <token>    (bare)    -> result is inserted via json.dumps, so ints/
                              floats/bools/strings all serialize correctly
                              as valid JSON.

    Safe to call on non-JSON strings too (e.g. QUERY_STRING values) —
    quoted-case just won't match and only the bare-token pass applies.
    """
    if not raw_text or "<" not in raw_text:
        return raw_text

    def _replace_quoted(m: re.Match) -> str:
        name, paren_group, arg_str = m.group(1), m.group(2), m.group(3)
        result = _resolve_token(name, paren_group, arg_str)
        return json.dumps(str(result))  # re-adds the quotes, escaped

    def _replace_bare(m: re.Match) -> str:
        name, paren_group, arg_str = m.group(1), m.group(2), m.group(3)
        result = _resolve_token(name, paren_group, arg_str)
        return json.dumps(result)

    def _replace_keyed(m: re.Match) -> str:
        raw_key, fn_name, arg_str = m.group(1), m.group(2), m.group(3)

        if fn_name not in TOKEN_REGISTRY:
            return m.group(0)  # not a function-call token, leave for normal passes

        args = _parse_args(arg_str)
        result = TOKEN_REGISTRY[fn_name](*args)

        # Remember it so later bare <key> references in this same blob resolve
        # to the SAME value instead of calling the function again.
        var_name = raw_key.strip("{}")
        set_variable(var_name, result)

        return f'"{raw_key}": {json.dumps(str(result))}'

    raw_text = _KEYED_TOKEN.sub(_replace_keyed, raw_text)
    raw_text = _QUOTED_TOKEN.sub(_replace_quoted, raw_text)
    raw_text = _BARE_TOKEN.sub(_replace_bare, raw_text)
    return raw_text


def resolve_row_tokens(row: dict) -> dict:
    """
    Convenience wrapper for a whole testcase_row dict — run this once,
    right after the CSV row is read, so PAYLOAD, QUERY_STRING,
    VALIDATE_DATA etc. are all resolved in one pass before anything else
    touches them.
    """
    return {
        key: resolve_dynamic_tokens(value) if isinstance(value, str) else value
        for key, value in row.items()
    }

# Matches "{key}": "<func(args)>"  -- i.e. only function-call tokens tied
# to a JSON key. Captures the key so we can remember the resolved value.
_KEYED_TOKEN = re.compile(
    r'"(\{?[A-Za-z_]\w*\}?)"\s*:\s*"<([A-Za-z_]\w*)\((.*?)\)>"'
)





# """
# dynamic_tokens.py
#
# Resolves two kinds of tokens embedded in raw CSV cell values (payloads,
# QUERY_STRING, VALIDATE_DATA, etc.) BEFORE the {placeholder} substitution
# step runs:
#
#   <name(args)>   -> FUNCTION call. Parentheses present ALWAYS mean "call
#                      this function" (with whatever args are inside, even
#                      none: "<name()>").
#   <name>         -> No parentheses. Checked in this order:
#                        1. Is `name` a registered FUNCTION? -> call it with
#                           zero args (shorthand for "<name()>").
#                        2. Otherwise, is `name` a registered VARIABLE? ->
#                           use its value (set via set_variable()).
#                      Neither -> KeyError with the list of known names.
#
# Functions are registered with @register_token where they're actually
# defined (e.g. date_utils.py, id_utils.py) — no need to re-implement or
# wrap them here. See the NOTE further down for both registration patterns.
#
# Usage in a CSV cell:
#     "auditId":"<generate_uuid>"                       (or <generate_uuid()>)
#     "{request_date_time}":<resolve_date_token>
#     "{expiry}":<resolve_date_token("date_minus_3m")>
#     "{amount}":<random_int(1000,9999)>
#     "{client_id}":"<base_client_id>"        <- variable, set elsewhere via
#                                                 set_variable("base_client_id", ...)
# """
#
# import ast
# import json
# import random
# import re
# from typing import Any, Callable, Dict
#
# # --------------------------------------------------------------------------
# # 1. Registry
# # --------------------------------------------------------------------------
#
# TOKEN_REGISTRY: Dict[str, Callable[..., Any]] = {}
#
# # Plain variable lookups — <name> with NO parentheses at all.
# # Populate via set_variable(), e.g. once per test run or per row.
# VARIABLES: Dict[str, Any] = {}
#
#
# def register_token(name: str):
#     """
#     Decorator: registers a function under the name used in CSV cells.
#     Function tokens ALWAYS require parentheses in the CSV, even with no
#     args, e.g. @register_token("generate_uuid") -> usable as
#     <generate_uuid()>  (NOT <generate_uuid> — that's a variable lookup).
#     """
#     def _wrap(fn: Callable[..., Any]):
#         TOKEN_REGISTRY[name] = fn
#         return fn
#     return _wrap
#
#
# def set_variable(name: str, value: Any) -> None:
#     """Registers a plain value usable in CSV cells as <name> (no parens)."""
#     if name in TOKEN_REGISTRY:
#         import warnings
#         warnings.warn(
#             f"'{name}' is registered as both a function and a variable. "
#             f"Bare '<{name}>' will always resolve to the FUNCTION (called "
#             f"with zero args) — the variable value is unreachable except "
#             f"via a differently-named token.",
#             stacklevel=2,
#         )
#     VARIABLES[name] = value
#
#
# # --------------------------------------------------------------------------
# # 2. Built-in token functions — add your own here or in another module,
# #    as long as it's imported before resolve_dynamic_tokens() is called.
# # --------------------------------------------------------------------------
#
# @register_token("random_int")
# def random_int(min_val: int = 1, max_val: int = 999999) -> int:
#     return random.randint(min_val, max_val)
# # CSV usage: <random_int()>  or  <random_int(1000, 9999)>
#
#
# # Example of a token that needs an argument pulled from elsewhere in your
# # framework (e.g. an env value) — just have the CSV pass it explicitly:
# #   <lookup_env("BASE_CLIENT_ID")>
# @register_token("lookup_env")
# def lookup_env(var_name: str, default: str = "") -> str:
#     import os
#     return os.getenv(var_name, default)
#
#
# # --------------------------------------------------------------------------
# # NOTE on functions that already live elsewhere (e.g. date_utils.py,
# # id_utils.py): do NOT re-implement them here. Just register the real ones,
# # either at the definition site:
# #
# #     # date_utils.py
# #     from utils.comparison.dynamic_tokens import register_token
# #
# #     @register_token("resolve_date_token")
# #     def resolve_date_token(token: str = "date_now") -> str | None:
# #         ...  # existing implementation
# #
# # ...or from a small central registration module imported once (e.g. in
# # conftest.py), if you'd rather keep date_utils.py decoupled from the
# # token dispatch system entirely:
# #
# #     # token_registrations.py
# #     from utils.comparison.dynamic_tokens import register_token
# #     from utils.date_utils import resolve_date_token
# #     from utils.id_utils import generate_uuid
# #
# #     register_token("resolve_date_token")(resolve_date_token)
# #     register_token("generate_uuid")(generate_uuid)
# #
# # Either way, whatever module contains the @register_token call MUST be
# # imported somewhere before resolve_dynamic_tokens() runs (e.g. import it
# # in conftest.py) — decorators only take effect once the module is loaded.
# # --------------------------------------------------------------------------
#
#
# # --------------------------------------------------------------------------
# # 3. Core resolution logic
# # --------------------------------------------------------------------------
#
# # Group 1: name. Group 2: the WHOLE "(...)" chunk, or None if absent.
# # Group 3: just the inner contents of the parens (may be "").
# # It's group 2 being None vs "" that tells us variable vs zero-arg call —
# # NOT whether the name happens to exist in one registry or the other.
# _QUOTED_TOKEN = re.compile(r'"<([A-Za-z_]\w*)(\((.*?)\))?>"')
# _BARE_TOKEN = re.compile(r'<([A-Za-z_]\w*)(\((.*?)\))?>')
#
#
# def _parse_args(arg_str: str):
#     """
#     Turns the raw text inside the parentheses into real Python args.
#     Wrapping in [...] lets ast.literal_eval safely handle multiple args,
#     strings, numbers, nested lists/dicts, without a fragile comma-split.
#     """
#     if not arg_str or not arg_str.strip():
#         return []
#     try:
#         return ast.literal_eval(f"[{arg_str}]")
#     except (ValueError, SyntaxError) as e:
#         raise ValueError(f"Could not parse token arguments '{arg_str}': {e}")
#
#
# def _resolve_token(name: str, paren_group: str, arg_str: str) -> Any:
#     """
#     paren_group is the regex's group(2): None if the CSV wrote <name>
#     with no parens, or a string like "()" / "(1,2)" if it wrote
#     <name(...)> explicitly.
#
#     Resolution order:
#       - Parens present  -> ALWAYS a function call (args parsed and passed).
#                             <name> must be in TOKEN_REGISTRY or this errors.
#       - Parens absent   -> try TOKEN_REGISTRY first, called with zero args
#                             (covers "<generate_uuid>" used as shorthand for
#                             "<generate_uuid()>"). If no such function exists,
#                             fall back to VARIABLES.
#     """
#     if paren_group is not None:
#         if name not in TOKEN_REGISTRY:
#             raise KeyError(
#                 f"No token FUNCTION registered for '<{name}(...)>'. "
#                 f"Known functions: {sorted(TOKEN_REGISTRY.keys())}"
#             )
#         args = _parse_args(arg_str or "")
#         return TOKEN_REGISTRY[name](*args)
#
#     # No parens: zero-arg function shorthand takes priority over variables.
#     if name in TOKEN_REGISTRY:
#         return TOKEN_REGISTRY[name]()
#     if name in VARIABLES:
#         return VARIABLES[name]
#
#     raise KeyError(
#         f"'<{name}>' is neither a registered function nor a registered "
#         f"variable. Known functions: {sorted(TOKEN_REGISTRY.keys())}. "
#         f"Known variables: {sorted(VARIABLES.keys())}."
#     )
#
#
# def resolve_dynamic_tokens(raw_text: str) -> str:
#     """
#     Scans raw_text for <function_name> / <function_name(args)> tokens and
#     replaces each with the function's return value.
#
#     - "<token>"  (quoted)  -> function must return something str()-able;
#                               result is re-wrapped in quotes, JSON-escaped.
#     - <token>    (bare)    -> result is inserted via json.dumps, so ints/
#                               floats/bools/strings all serialize correctly
#                               as valid JSON.
#
#     Safe to call on non-JSON strings too (e.g. QUERY_STRING values) —
#     quoted-case just won't match and only the bare-token pass applies.
#     """
#     if not raw_text or "<" not in raw_text:
#         return raw_text
#
#     def _replace_quoted(m: re.Match) -> str:
#         name, paren_group, arg_str = m.group(1), m.group(2), m.group(3)
#         result = _resolve_token(name, paren_group, arg_str)
#         return json.dumps(str(result))  # re-adds the quotes, escaped
#
#     def _replace_bare(m: re.Match) -> str:
#         name, paren_group, arg_str = m.group(1), m.group(2), m.group(3)
#         result = _resolve_token(name, paren_group, arg_str)
#         return json.dumps(result)
#
#     raw_text = _QUOTED_TOKEN.sub(_replace_quoted, raw_text)
#     raw_text = _BARE_TOKEN.sub(_replace_bare, raw_text)
#     return raw_text
#
#
# def resolve_row_tokens(row: dict) -> dict:
#     """
#     Convenience wrapper for a whole testcase_row dict — run this once,
#     right after the CSV row is read, so PAYLOAD, QUERY_STRING,
#     VALIDATE_DATA etc. are all resolved in one pass before anything else
#     touches them.
#     """
#     return {
#         key: resolve_dynamic_tokens(value) if isinstance(value, str) else value
#         for key, value in row.items()
#     }