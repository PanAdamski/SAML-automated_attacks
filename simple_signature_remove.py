import sys
import re
import base64
from urllib.parse import unquote_plus
import xml.etree.ElementTree as ET

if len(sys.argv) > 1:
    raw_value = sys.argv[1]
else:
    raw_value = sys.stdin.read().strip()

url_decoded = unquote_plus(raw_value)
b64_compact = re.sub(r"\s+", "", url_decoded)
missing = (-len(b64_compact)) % 4
if missing:
    b64_compact += "=" * missing

try:
    xml_bytes = base64.b64decode(b64_compact, validate=False)
except Exception as e:
    print(f"Błąd dekodowania Base64: {e}", file=sys.stderr)
    sys.exit(1)

try:
    root = ET.fromstring(xml_bytes)
except Exception as e:
    print(f"Błąd parsowania XML: {e}", file=sys.stderr)
    sys.exit(1)

for parent in root.iter():
    to_remove = []
    for child in list(parent):
        tag = child.tag
        if "}" in tag:
            local = tag.split("}", 1)[1]
        else:
            local = tag
        if "signature" in local.lower():
            to_remove.append(child)
    for child in to_remove:
        parent.remove(child)

print(ET.tostring(root, encoding="unicode"))
