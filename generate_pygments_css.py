from pygments.formatters import HtmlFormatter

# Generate CSS for the 'monokai' style (similar to VS Code dark)
# We can also try 'material', 'dracula', or 'one-dark' if available, but monokai is standard.
# Let's check available styles first or just use a known good one.
# 'monokai' is a safe bet for a dark IDE look.

formatter = HtmlFormatter(style='monokai', cssclass='codehilite')
css_content = formatter.get_style_defs('.codehilite')

print(css_content)