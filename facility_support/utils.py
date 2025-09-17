"""
Utility functions for formatting and displaying text in HTML tables
within Jupyter notebooks.
"""

import re

from IPython.display import HTML, display


def format_text(text):
    # Format headings
    text = re.sub(r"^\*\*(.*?)\*\*:", r"<strong>\1:</strong>", text, flags=re.MULTILINE)
    text = re.sub(r"^\*\*(.*?)\*\*", r"<strong>\1</strong>", text, flags=re.MULTILINE)
    # Format bold and italics
    text = re.sub(r"\*\*(.*?)\*\*", r"<strong>\1</strong>", text)
    text = re.sub(r"\*(.*?)\*", r"<em>\1</em>", text)
    # Format numbered steps
    text = re.sub(
        r"^\s*\*\*STEP (\d+)\*\*:",
        r"<strong>STEP \1:</strong>",
        text,
        flags=re.MULTILINE,
    )
    # Format code blocks (JSON and indented examples)
    text = re.sub(
        r"```(.*?)```", r'<pre class="dark-pre">\1</pre>', text, flags=re.DOTALL
    )
    text = re.sub(r"(\{\{[\s\S]*?\}\})", r'<pre class="dark-pre">\1</pre>', text)
    text = re.sub(
        r'(\{[\s\S]*?"explanation":.*?\})', r'<pre class="dark-pre">\1</pre>', text
    )

    # Format bullet points with indentation
    def bullets_to_html(match):
        line = match.group(0)
        spaces = len(re.match(r"^\s*", line).group(0))
        content = line.lstrip()[2:]  # Remove '- ' after leading spaces
        return f'<li style="margin-left:{spaces*10}px">{content}</li>'

    text = re.sub(r"^( *)- (.+)", bullets_to_html, text, flags=re.MULTILINE)
    # Wrap all <li> in <ul>
    text = re.sub(r"((<li.*?</li>\s*)+)", r"<ul>\1</ul>", text, flags=re.DOTALL)
    text = re.sub(r"</ul>\s*<ul>", "", text)

    # Preserve newlines for non-list, non-pre content
    # (Wrap everything in a div with white-space: pre-wrap)
    return f'<div style="white-space: pre-wrap;">{text}</div>'


def print_html_table(
    s1,
    s2,
    format_text_enabled=False,
    col1_title="BEFORE OPTIMIZATION",
    col2_title="AFTER OPTIMIZATION",
):
    s1_fmt = (
        format_text(s1)
        if format_text_enabled
        else f'<div style="white-space: pre-wrap;">{s1}</div>'
    )
    s2_fmt = (
        format_text(s2)
        if format_text_enabled
        else f'<div style="white-space: pre-wrap;">{s2}</div>'
    )
    table = f"""
    <style>
        table {{
            width: 100%;
            table-layout: fixed;
            border-collapse: collapse;
        }}
        th, td {{
            border: 1px solid #444;
            padding: 8px;
            vertical-align: top;
        }}
        th {{
            background-color: #222;
            color: #eee;
        }}
        td {{
            width: 50%;
            word-break: break-word;
            background-color: #181818;
            color: #eee;
        }}
        pre.dark-pre {{
            background-color: #23272e;
            color: #eee;
            border-radius: 4px;
            padding: 8px;
            font-size: 13px;
            font-family: 'Fira Mono', 'Consolas', 'Monaco', monospace;
            white-space: pre-wrap;
        }}
        ul {{
            margin: 0 0 0 20px;
            padding: 0;
        }}
        li {{
            margin-bottom: 4px;
        }}
        strong {{
            color: #7cb4ff;
        }}
        em {{
            color: #ffb47c;
        }}
    </style>
    <table>
        <tr>
            <th style="text-align:left;"><strong>{col1_title}</strong></th>
            <th style="text-align:left;"><strong>{col2_title}</strong></th>
        </tr>
        <tr>
            <td style="text-align:left; vertical-align:top;">{s1_fmt}</td>
            <td style="text-align:left; vertical-align:top;">{s2_fmt}</td>
        </tr>
    </table>
    """
    display(HTML(table))
