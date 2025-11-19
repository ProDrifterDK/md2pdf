import markdown
from playwright.sync_api import sync_playwright
import os

# The content from the file
md_content_raw = r"primitives are strictly defined (e.g., \<View\>, \<Text\>, \<Image\>)."

# 1. Simulate the current script logic
# md_content_fixed = md_content_raw.replace(r'\<', '<').replace(r'\>', '>')
# print(f"Fixed Markdown Content: {md_content_fixed}")

# html_body = markdown.markdown(md_content_fixed)
# print(f"HTML Body: {html_body}")

# 2. Simulate what we WANT
# We want the HTML to contain <View> so the browser renders <View>
# If we pass \<View\> to python-markdown, it produces <View>
# Let's verify this behavior again.

print(f"Raw Input: {md_content_raw}")
html_body_raw = markdown.markdown(md_content_raw)
print(f"HTML Body from Raw: {html_body_raw}")

# If python-markdown produces <View>, then the browser should render <View>.
# If the user says it's blank, maybe it's producing <View> (literal tags) which the browser hides?

# Let's try to force double escaping to see if that's what's needed
# If we want <View> in the HTML source, we need python-markdown to output <View>
# If python-markdown outputs <View>, the browser sees a tag.

# Let's test what happens if we replace \< with < BEFORE markdown processing
pre_replaced = md_content_raw.replace(r'\<', '<').replace(r'\>', '>')
print(f"Pre-replaced Input: {pre_replaced}")
html_body_pre = markdown.markdown(pre_replaced)
print(f"HTML Body from Pre-replaced: {html_body_pre}")

html_template = f"""
<!DOCTYPE html>
<html>
<body>
    <h1>Raw Processing</h1>
    {html_body_raw}
    <h1>Pre-replaced Processing</h1>
    {html_body_pre}
</body>
</html>
"""

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page()
    page.set_content(html_template)
    # Get the text content of the body to see what the browser rendered
    text = page.inner_text("body")
    print(f"Browser Rendered Text:\n{text}")
    
    # Also print the HTML content to see what the browser actually has in the DOM
    content = page.content()
    print(f"Browser DOM Content:\n{content}")
    
    browser.close()