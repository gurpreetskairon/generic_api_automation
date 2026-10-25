"""
XML Parser Utility — Namespace-Agnostic & Smart Return (stable + offset + attribute path)
----------------------------------------------------------------------------------------
• Works for both elements and attributes (e.g., //courseDetails@id=C123)
• Supports parent offsets like :-1, :-2
• Allows nested access (e.g., :-1/description)
• Namespace-free lookups, auto namespace extraction
• Smart returns: text for leaves, xml for subtrees
"""

import io
import re
import xml.etree.ElementTree as et
from typing import Union

from lxml import etree

DEFAULT_NAMESPACES = {
    "soap": "http://schemas.xmlsoap.org/soap/envelope/",
    "soap12": "http://www.w3.org/2003/05/soap-envelope"
}


# ---------- Helpers ----------
def extract_namespaces(xml: Union[str, bytes]) -> dict:
    """Extract all namespaces declared in XML."""
    if isinstance(xml, bytes):
        xml = xml.decode("utf-8")
    xml_bytes = xml.strip().encode("utf-8")
    ns_map = {}
    for _, (prefix, uri) in etree.iterparse(io.BytesIO(xml_bytes), events=("start-ns",)):
        ns_map[prefix or "ns"] = uri
    return ns_map


def load_xml_tree(xml: Union[str, bytes, etree._Element]) -> etree._Element:
    """Ensure parsed XML Element tree."""
    if isinstance(xml, etree._Element):
        return xml
    if isinstance(xml, (str, bytes)):
        xml = xml.strip().encode("utf-8") if isinstance(xml, str) else xml.strip()
        parser = etree.XMLParser(recover=True, remove_blank_text=True)
        return etree.fromstring(xml, parser=parser)
    raise TypeError("xml must be string/bytes/Element")


def _normalize_xpath(xpath_expr: str) -> str:
    """Make XPath namespace-agnostic (local-name match)."""
    parts = [p for p in xpath_expr.strip().split("/") if p]
    normalized = []
    for p in parts:
        if p == "*":
            normalized.append("*")
        else:
            normalized.append(f"* [local-name()='{p.replace(':', '')}']")
    return "//" + "/".join(normalized).replace(" ", "")


def _element_to_value(elem: etree._Element):
    """
    Convert an XML element to the best-fit Python type:
      - If it's a leaf → return text.
      - If it has children → return pretty, well-formed XML (no ns: clutter).
    """
    if len(elem) == 0:
        return (elem.text or "").strip()

    # Serialize with pretty print
    xml_str = etree.tostring(elem, encoding="unicode", pretty_print=True, with_tail=False)

    # Remove xmlns declarations (for readability)
    xml_str = re.sub(r'\s+xmlns(:\w+)?="[^"]+"', "", xml_str)

    # Clean prefixed tags while keeping closing slashes intact
    xml_str = re.sub(r"<(/?)ns:", r"<\1", xml_str)

    return xml_str.strip()


# ---------- Core ----------
def find_in_xml(xml_data, xpath_expr: str, default=None, raise_error=False):
    """Direct XPath lookup (namespace-free)."""
    root = load_xml_tree(xml_data)
    xml_str = etree.tostring(root, encoding="utf-8").decode("utf-8")
    ns = {**DEFAULT_NAMESPACES, **extract_namespaces(xml_str)}
    normalized = _normalize_xpath(xpath_expr)
    try:
        result = root.xpath(normalized, namespaces=ns)
        if not result:
            return default
        node = result[0]
        if isinstance(node, etree._Element):
            return _element_to_value(node)
        elif isinstance(node, bytes):
            return node.decode("utf-8")
        return node
    except Exception as e:
        print(f"[find_in_xml] XPath error for '{xpath_expr}': {e}")
        return default


def find_pattern_in_xml(
    xml_data, tag_pattern, value=None, start_expr=None, parent_offset=0, expression=None, attribute_only=False
):
    """Find element/attribute by pattern=value, with parent traversal and offsets."""
    root = load_xml_tree(xml_data)
    xml_str = etree.tostring(root, encoding="utf-8").decode("utf-8")
    ns = {**DEFAULT_NAMESPACES, **extract_namespaces(xml_str)}

    start_nodes = [root]
    if start_expr:
        start_nodes = root.xpath(_normalize_xpath(start_expr), namespaces=ns)
        if not start_nodes:
            return None

    pattern = re.compile(tag_pattern.lstrip("@").replace("*", ".*") + "$")
    found_elem = None
    found_stack = []

    def recursive_find(node, stack):
        nonlocal found_elem, found_stack
        if found_elem is not None:
            return
        localname = etree.QName(node).localname

        # --- Attribute match ---
        if attribute_only and node.get(tag_pattern.lstrip("@")) == str(value):
            found_elem, found_stack = node, stack
            return

        # --- Element text match ---
        if value is not None and pattern.match(localname):
            if (node.text or "").strip() == str(value):
                found_elem, found_stack = node, stack
                return

        # --- Attribute value match (normal case) ---
        for attr_name, attr_val in node.attrib.items():
            if pattern.match(attr_name) and str(attr_val) == str(value):
                found_elem, found_stack = node, stack
                return

        # --- Recurse children ---
        for child in node:
            recursive_find(child, stack + [node])

    for s in start_nodes:
        recursive_find(s, [])

    if found_elem is None:
        return None

    # --- Parent offset handling ---
    result = found_elem
    if parent_offset < 0:
        idx = abs(parent_offset)
        if len(found_stack) >= idx:
            result = found_stack[-idx]
        else:
            return None

    # --- Nested expression (:-1/description) ---
    if expression:
        rel_nodes = result.xpath(_normalize_xpath(expression), namespaces=ns)
        if not rel_nodes:
            return None
        rel = rel_nodes[0]
        if isinstance(rel, etree._Element):
            return _element_to_value(rel)
        return rel

    return _element_to_value(result)


def query_xml(xml_data, pattern):
    """
    Wrapper over find_in_xml() and find_pattern_in_xml().
    Supports:
        //weekCode/value
        value=WK3
        value=WK3:-1
        value=WK3:-1/description
        //courseDetails//value=WK1:-1/description
        courseDetails@id=C123
    """
    key = pattern.strip()
    start_expr = None
    value = None
    expression = None
    parent_offset = 0
    attribute_only = False

    # Handle attributes and element path e.g. //courseDetails@id=C123
    if "=" in key:
        lhs, rhs = key.split("=", 1)
        value = rhs.strip()

        # If attribute syntax used
        if "@" in lhs:
            at_index = lhs.rfind("@")
            start_expr = lhs[:at_index].strip() or None
            tag_pattern = lhs[at_index:].strip()  # e.g. @id
            attribute_only = True
        else:
            tag_pattern = lhs.strip()

            # Handle embedded start path (e.g. //courseDetails//value=WK1)
            if "//" in lhs:
                last_double = lhs.rfind("//")
                start_expr = lhs[:last_double].strip() or None
                tag_pattern = lhs[last_double + 2 :].split("/")[-1]

        # --- Parse offset and nested path ---
        if ":" in value:
            value, expr = map(str.strip, value.split(":", 1))
            if expr:
                m = re.match(r"^\s*(-?\d+)(?:[./](.*))?$", expr)
                if m:
                    parent_offset = int(m.group(1))
                    expression = m.group(2)
                else:
                    expression = expr

        return find_pattern_in_xml(
            xml_data,
            tag_pattern=tag_pattern,
            value=value,
            start_expr=start_expr,
            parent_offset=parent_offset,
            expression=expression,
            attribute_only=attribute_only
        )
    else:
        return find_in_xml(xml_data, key)


def replace_tag_value(xml_data: str, tag_to_replace: str, replacement_value: str = "", parent_tag: str = None) -> str:
    """This function takes an XML string, and replaces a value of a tag within it
    :param xml_data: full xml payload
    :param tag_to_replace: name of the tag of the value to replace. e.g if tag is <v15:code> just pass code
    :param replacement_value: the new value to update the above tag to
    :param parent_tag: Name of the parent tag the tag_to_replace is under, used if there are duplicate tag_to_replace
    :return: full XML payload"""
    if parent_tag is not None:
        tag = ".//{*}" + parent_tag + "//{*}" + tag_to_replace
    else:
        tag = ".//{*}" + tag_to_replace
    root = et.fromstring(xml_data)
    current_value = root.find(tag)
    current_value.text = replacement_value
    return et.tostring(root, encoding="unicode")


def replace_tag(xml_string: str, tag_to_replace: str, replacement_value: str = "") -> str:
    """This function takes an XML string, and replaces the tag (not its value)
    :param xml_string: full xml payload
    :param tag_to_replace: name of the tag of the value to replace. e.g if tag is <v15:code> pass v15:code
    :param replacement_value: the new value to update the above tag to
    :return: full XML payload"""

    xml_string = re.sub(rf"<{tag_to_replace}>.*?</{tag_to_replace}>", replacement_value, xml_string, flags=re.DOTALL)
    return xml_string
