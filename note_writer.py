#!/usr/bin/env python3
"""
note_writer.py — Apple Notes writer for Claude sessions.
Writes properly formatted notes using HTML via osascript stdin.
Handles all escaping automatically.

Usage:
    from note_writer import write_note
    write_note("Note Title", html_body)

HTML reference:
    <h1>Title</h1>                          — large bold title
    <h2>Section Header</h2>                 — bold section header
    <h3>Sub Header</h3>                     — smaller sub header
    <div>Regular text</div>                 — normal paragraph
    <b>bold</b>  <i>italic</i>              — inline formatting
    <br>                                    — blank line / spacing
    <ul><li>item</li></ul>                  — bullet list
    <ol><li>item</li></ol>                  — numbered list
    <object><table><tbody>
      <tr><td>A</td><td>B</td></tr>
    </tbody></table></object>               — native table

Emoji status convention:
    🔴 Needs your input
    🟢 Claude solo
    🟡 Discuss first
    🔵 Parked / future
    ⚫ Deep backlog

Notes:
    - Native checkboxes are NOT possible programmatically (Apple limitation)
    - Use emoji + ul/li for task lists instead
    - Always pass full HTML body — this does a full replace
"""

import subprocess
import sys


def write_note(note_name: str, html_body: str) -> bool:
    """
    Find existing note by name and replace its body with html_body.
    If note does not exist, creates it.
    Returns True on success, False on failure.
    """
    escaped_body = _escape(html_body)
    escaped_name = _escape_simple(note_name)

    script = f'''tell application "Notes"
    set noteBody to "{escaped_body}"
    try
        set n to first note whose name is "{escaped_name}"
        set body of n to noteBody
    on error
        make new note at folder "Notes" with properties {{name:"{escaped_name}", body:noteBody}}
    end try
end tell'''

    import tempfile, os
    with tempfile.NamedTemporaryFile(mode='w', suffix='.scpt', delete=False) as f:
        f.write(script)
        tmp_path = f.name
    try:
        result = subprocess.run(
            ['osascript', tmp_path],
            capture_output=True,
            text=True
        )
    finally:
        os.unlink(tmp_path)

    if result.returncode != 0 or result.stderr.strip():
        print(f"ERROR: {result.stderr}", file=sys.stderr)
        return False

    return True


def find_note_name(partial_name: str):
    """Find a note by partial name match. Returns full name or None."""
    script = '''tell application "Notes"
    set output to ""
    repeat with n in every note
        set output to output & name of n & "|"
    end repeat
    return output
end tell'''

    result = subprocess.run(['osascript'], input=script, capture_output=True, text=True)
    if result.returncode != 0:
        return None

    for name in result.stdout.strip().split('|'):
        if partial_name.lower() in name.lower():
            return name
    return None


def _escape(s: str) -> str:
    """Escape string for AppleScript double-quoted string."""
    s = s.replace('\\', '\\\\')
    s = s.replace('"', '\\"')
    s = s.replace('\n', '').replace('\r', '')
    return s


def _escape_simple(s: str) -> str:
    s = s.replace('\\', '\\\\')
    s = s.replace('"', '\\"')
    return s


# ─── HTML builders ───────────────────────────────────────────────────────────

def h1(text):  return f"<h1>{text}</h1>"
def h2(text):  return f"<h2>{text}</h2>"
def h3(text):  return f"<h3>{text}</h3>"
def div(text): return f"<div>{text}</div>"
def b(text):   return f"<b>{text}</b>"
def br():      return "<br>"

def ul(items: list) -> str:
    return "<ul>" + "".join(f"<li>{i}</li>" for i in items) + "</ul>"

def ol(items: list) -> str:
    return "<ol>" + "".join(f"<li>{i}</li>" for i in items) + "</ol>"

def table(rows: list) -> str:
    """rows = list of lists. First row auto-bolded as header."""
    html = "<object><table><tbody>"
    for i, row in enumerate(rows):
        html += "<tr>"
        for cell in row:
            content = f"<b>{cell}</b>" if i == 0 else str(cell)
            html += f"<td>{content}</td>"
        html += "</tr>"
    html += "</tbody></table></object>"
    return html


# ─── Self-test ───────────────────────────────────────────────────────────────

if __name__ == "__main__":
    body = (
        h1("note_writer.py — Format Test") +
        div("Updated: April 24, 2026") +
        br() +
        h2("Headings") +
        h3("This is h3 — sub section") +
        div("This is div — regular paragraph text.") +
        br() +
        h2("Lists") +
        ul(["🔴 Needs your input", "🟢 Claude solo", "🟡 Discuss first", "🔵 Parked"]) +
        br() +
        h2("Numbered") +
        ol(["Step one", "Step two", "Step three"]) +
        br() +
        h2("Table") +
        table([
            ["Feature",       "Status",      "Notes"],
            ["h1/h2/h3",      "🟢 Works",    "Native headings"],
            ["ul/ol lists",   "🟢 Works",    "Native bullets"],
            ["Tables",        "🟢 Works",    "Native table"],
            ["Checkboxes",    "🔴 Blocked",  "Apple limitation"],
        ])
    )
    ok = write_note("__ note_writer format test", body)
    print("✅ Success" if ok else "❌ Failed")
