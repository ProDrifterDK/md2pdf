import markdown
from playwright.sync_api import sync_playwright
import os

# The content from the file
md_content_raw = r"primitives are strictly defined (e.g., \<View\>, \<Text\>, \<Image\>)."

# Proposed fix: Double escape the entities
# We want the final HTML to be: ... <View> ...
# python-markdown might consume one level of escaping.

pre_replaced = md_content_raw.replace(r'\<', '&lt;').replace(r'\>', '&gt;')
print(f"Pre-replaced Input: {pre_replaced}")

html_body_pre = markdown.markdown(pre_replaced)
print(f"HTML Body from Pre-replaced: {html_body_pre}")

html_template = f"""
<!DOCTYPE html>
<html>
<body>
    <h1>Pre-replaced Processing (Double Escaped)</h1>
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