#!/usr/bin/env uv run --no-project

import sys, json, html

if len(sys.argv) != 2:
    print("Usage: convert.py input.json")
    sys.exit(1)

input_file = sys.argv[1]
output_file = input_file.replace('.json', '.tmTheme')

with open(input_file, 'r', encoding='utf-8') as f:
    theme = json.load(f)

def esc(s):
    return html.escape(s, quote=False)

def keyval(key, val):
    return f"<key>{esc(key)}</key><string>{esc(val)}</string>"

def dict_block(content):
    return f"<dict>{content}</dict>"

def scope_entry(token):
    scope = token.get("scope", "")
    if isinstance(scope, list):
        scope = ", ".join(scope)
    settings = token.get("settings", {})
    inner = ""
    if "foreground" in settings:
        inner += keyval("foreground", settings["foreground"])
    if "background" in settings:
        inner += keyval("background", settings["background"])
    if "fontStyle" in settings:
        inner += keyval("fontStyle", settings["fontStyle"])
    return dict_block(
        keyval("scope", scope) +
        "<key>settings</key>" +
        dict_block(inner)
    )

token_blocks = "".join(scope_entry(t) for t in theme.get("tokenColors", []))

xml = f'''<?xml version="1.0" encoding="UTF-8"?>
<plist version="1.0">
<dict>
  {keyval("name", theme.get("name", "Converted Theme"))}
  <key>settings</key>
  <array>
    {token_blocks}
  </array>
</dict>
</plist>
'''

with open(output_file, 'w', encoding='utf-8') as f:
    f.write(xml)

print(f"✅ Wrote {output_file}")
