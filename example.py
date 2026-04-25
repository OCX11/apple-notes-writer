#!/usr/bin/env python3
"""
example.py — Demonstrates all note_writer.py features.
Run this to create a sample note called "note_writer — Example Note".
"""

import sys
sys.path.insert(0, '.')
from note_writer import write_note, h1, h2, h3, div, b, br, ul, ol, table

body = (
    # Title + datestamp
    h1("note_writer — Example Note") +
    div("Updated: April 24, 2026") +
    br() +

    # Section headers
    h2("SECTION HEADERS") +
    div("h2 produces bold section headers like the one above.") +
    h3("h3 produces smaller sub-headers like this one") +
    div("div produces regular paragraph text like this.") +
    div("You can also use " + b("bold inline text") + " inside a div.") +
    br() +

    # Bullet list
    h2("BULLET LISTS") +
    ul([
        "Plain bullet item",
        "🔴 Red dot — needs input",
        "🟢 Green dot — ready to go",
        "🟡 Yellow dot — needs discussion",
        "🔵 Blue dot — parked for later",
        "⚫ Black dot — deep backlog",
    ]) +
    br() +

    # Numbered list
    h2("NUMBERED LISTS") +
    ol([
        "First step",
        "Second step",
        "Third step",
    ]) +
    br() +

    # Table
    h2("TABLES") +
    div("First row is automatically bold (header row).") +
    table([
        ["Name",            "Status",       "Est. time"],
        ["Feature A",       "🟢 Ready",     "~1hr"],
        ["Feature B",       "🔴 Blocked",   "~2hr"],
        ["Feature C",       "🟡 Discuss",   "~3hr"],
    ]) +
    br() +

    # Limitations callout
    h2("KNOWN LIMITATIONS") +
    ul([
        "🔴 Native checkboxes — not possible programmatically (Apple limitation)",
        "🔴 Hyperlinks — stripped on save",
        "🟢 Workaround: use emoji + bullet lists for task tracking",
    ])
)

ok = write_note("note_writer — Example Note", body)
print("✅ Example note written" if ok else "❌ Failed")
