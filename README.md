# apple-notes-writer

A Python utility for writing properly formatted Apple Notes from Claude AI sessions (or any script). Uses `osascript` under the hood — no dependencies, no MCP tools, no formatting surprises.

## Why this exists

Every programmatic Apple Notes solution eventually breaks down because:
- The Apple Notes MCP tool produces run-on unformatted text
- Raw `osascript` string-building hits escaping errors with HTML attributes
- Native checkboxes **cannot** be written programmatically (Apple limitation, full stop)

This script solves the escaping problem cleanly by passing scripts via `osascript` stdin, and provides a set of HTML builder functions that produce correctly-formatted Notes every time.

## Requirements

- macOS (tested on macOS 15+)
- Python 3.9+
- Apple Notes app
- No third-party dependencies

## Installation

Copy `note_writer.py` anywhere on your system. For Claude sessions, `/Users/<you>/bin/note_writer.py` works well.

```bash
cp note_writer.py ~/bin/note_writer.py
```

## Usage

```python
import sys
sys.path.insert(0, '/Users/you/bin')
from note_writer import write_note, h1, h2, h3, div, b, br, ul, ol, table

body = (
    h1("My Note Title") +
    div("Updated: April 24, 2026") +
    br() +
    h2("SECTION ONE") +
    ul(["First item", "Second item", "Third item"]) +
    br() +
    h2("SECTION TWO") +
    table([
        ["Column A", "Column B", "Column C"],
        ["Row 1A",   "Row 1B",   "Row 1C"],
        ["Row 2A",   "Row 2B",   "Row 2C"],
    ])
)

write_note("My Note Title", body)
```

If a note with that name already exists, it's updated in place. If not, it's created.

## HTML Builders

| Function | Output | Renders as |
|---|---|---|
| `h1(text)` | `<h1>text</h1>` | Large bold title |
| `h2(text)` | `<h2>text</h2>` | Bold section header |
| `h3(text)` | `<h3>text</h3>` | Smaller sub-header |
| `div(text)` | `<div>text</div>` | Regular paragraph |
| `b(text)` | `<b>text</b>` | Bold inline text |
| `br()` | `<br>` | Blank line / spacing |
| `ul([items])` | `<ul><li>...</li></ul>` | Bullet list |
| `ol([items])` | `<ol><li>...</li></ol>` | Numbered list |
| `table([[rows]])` | `<object><table>...</table></object>` | Native table (first row = bold header) |

You can also mix in raw HTML strings — they're just concatenated.

## Emoji Status Convention

Since native checkboxes are impossible, use emoji prefixes in list items:

```python
ul([
    "🔴 Needs your input",
    "🟢 Ready to execute",
    "🟡 Discuss first",
    "🔵 Parked for later",
    "⚫ Deep backlog",
])
```

## What Doesn't Work (Apple Limitation)

- **Native checkboxes** — Apple strips `class="checklist"` and `data-checked` attributes. There is no programmatic workaround. Use emoji + `ul()` instead.
- **Hyperlinks** — stripped on save
- **Images** — technically possible with base64 but impractical

## Self-Test

Run directly to create a test note:

```bash
python3 note_writer.py
```

This creates a note called `__ note_writer format test` demonstrating all supported formatting.

## For Claude AI Sessions

Add this to your Claude context file (`.claude_context.md`):

```
- APPLE NOTES: ALWAYS use /Users/claw/bin/note_writer.py via python3.
  NEVER use the Apple Notes MCP tool — it cannot produce proper formatting.
  Import: sys.path.insert(0, '/Users/claw/bin'); from note_writer import write_note, h1, h2, h3, div, b, br, ul, ol, table
  Body = concatenated builder strings. Pass to write_note(exact_note_name, body).
```

## License

MIT
