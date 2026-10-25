import json

import jmespath


def open_json_file(file_path: str, mode: str = None):
    if mode is None:
        with open(file_path) as file_content:
            json_content = json.load(file_content)
    else:
        with open(file_path, mode) as file_content:
            json_content = json.load(file_content)

    return json_content


def load_json(data):
    """Accepts a JSON string or dict/list and returns a Python object."""
    if isinstance(data, str):
        if data.strip().startswith(("{", "[")):
            try:
                return json.loads(data)
            except json.JSONDecodeError:
                return data
        return data
    return data if isinstance(data, (dict, list)) else data


def find_in_json(data, key_pattern, default=None, raise_error=False):
    """
    Perform a standard JMESPath query on JSON data.
    Used for simple, direct lookups when there is no '=' in the pattern.
    """
    data = load_json(data)
    try:
        result = jmespath.search(key_pattern, data)
        if result is None and raise_error:
            raise KeyError(f"No match for expression: {key_pattern}")
        return result if result is not None else default
    except Exception as e:
        if raise_error:
            raise
        print(f"[find_in_json] Error evaluating '{key_pattern}': {e}")
        return default


def find_pattern_in_json(data, key_pattern, value=None, start_expr=None, parent_offset=0, expression=None):
    """
    Recursively search JSON data to find the first dictionary
    where obj[key_pattern] == value, or a key matching a wildcard/regex pattern.
    Supports:
      - start_expr: JMESPath subtree to begin searching from
      - parent_offset: -1 for parent, -2 for grandparent, etc.
      - expression: optional nested JMESPath lookup inside the found object
    """
    data = load_json(data)
    if start_expr:
        data = find_in_json(data, start_expr)
        if data is None:
            return None

    # pattern = re.compile(key_pattern.replace("*", ".*") + "$")
    found_obj = None
    found_ancestors = []

    def recursive_find(obj, ancestors):
        nonlocal found_obj, found_ancestors
        if found_obj is not None:
            return  # stop at first match

        if isinstance(obj, dict):
            # Check for key=value match
            if value is not None and key_pattern in obj and str(obj[key_pattern]) == str(value):
                found_obj = obj
                found_ancestors = ancestors
                return

            for v in obj.values():
                recursive_find(v, ancestors + [obj])

        elif isinstance(obj, list):
            # Include the list itself as an ancestor for correct parent_offset handling
            for item in obj:
                recursive_find(item, ancestors + [obj])

    recursive_find(data, [])

    if found_obj is None:
        return None

    # Apply parent offset (-1, -2, etc.)
    if parent_offset < 0:
        idx = abs(parent_offset)
        if len(found_ancestors) >= idx:
            result = found_ancestors[-idx]
        else:
            return None
    else:
        result = found_obj

    # Apply nested JMESPath query if specified
    if expression and result is not None:
        return find_in_json(result, expression)
    return result


def query_json(json_data, pattern):
    """
    Wrapper over `find_in_json` and `find_pattern_in_json`.
    Automatically parses a flexible pattern string and calls
    the appropriate method depending on the syntax.

    Examples:
        query_json(data, "weekDetails[0].weekCode.value")
            → uses find_in_json()  (direct JMESPath)

        query_json(data, "weekDetails..value=WK3:-1")
            → uses find_pattern_in_json()  (key-value search)
    """

    # --- Defaults ---
    start_expression = None
    key = pattern.strip()
    value = None
    expression = None
    parent_offset = 0

    # --- Split on ".." (start_expr vs main expression) ---
    if ".." in key:
        start_expression, key = map(str.strip, key.split("..", 1))

    # --- If it’s a key=value type pattern, call find_pattern_in_json() ---
    if "=" in key:
        key, value = map(str.strip, key.split("=", 1))

        # --- Split value:expression if applicable ---
        if ":" in value:
            value, expression = map(str.strip, value.split(":", 1))
            if not expression:
                expression = None

        # --- Handle parent_offset like "-1.something" or ":-2" ---
        if expression:
            parts = [p.strip() for p in expression.split(".", 1)]
            first_part = parts[0]

            if first_part.lstrip("-").isdigit():
                parent_offset = int(first_part)
                expression = parts[1] if len(parts) > 1 else None
            elif expression.lstrip("-").isdigit():
                parent_offset = int(expression)
                expression = None

        # --- Use find_pattern_in_json() ---
        return find_pattern_in_json(
            json_data,
            key_pattern=key,
            value=value,
            start_expr=start_expression,
            parent_offset=parent_offset,
            expression=expression
        )

    else:
        # --- If no '=', treat it as a simple JMESPath query ---
        return find_in_json(json_data, key)
