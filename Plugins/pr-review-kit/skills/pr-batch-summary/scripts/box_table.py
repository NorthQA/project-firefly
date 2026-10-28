#!/usr/bin/env python3
"""Render a box-drawing table (for Discord code blocks) from JSON.

Usage: python box_table.py <table.json>
JSON: {"widths": [22, 10, 9, 40], "headers": ["PR", ...], "rows": [["#123 Login fix", ...], ...]}
Cells wrap to their column width; the output is plain text to put inside a ``` block.
"""
import json
import sys
import textwrap


def line(widths, left, mid, right):
    return left + mid.join("─" * (w + 2) for w in widths) + right


def row(widths, cells, center=False):
    wrapped = [textwrap.wrap(str(c), w) or [""] for c, w in zip(cells, widths)]
    out = []
    for i in range(max(len(c) for c in wrapped)):
        parts = [(c[i] if i < len(c) else "") for c in wrapped]
        parts = [p.center(w) if center else p.ljust(w) for p, w in zip(parts, widths)]
        out.append("│ " + " │ ".join(parts) + " │")
    return out


def render(widths, headers, rows):
    out = [line(widths, "┌", "┬", "┐"), *row(widths, headers, center=True)]
    for r in rows:
        out += [line(widths, "├", "┼", "┤"), *row(widths, r)]
    out.append(line(widths, "└", "┴", "┘"))
    return "\n".join(out)


if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    with open(sys.argv[1], encoding="utf-8") as f:
        t = json.load(f)
    text = render(t["widths"], t["headers"], t["rows"])
    width = sum(t["widths"]) + 3 * len(t["widths"]) + 1
    assert all(len(l) == width for l in text.splitlines()), "row width mismatch"
    sys.stdout.reconfigure(encoding="utf-8")
    print(text)
