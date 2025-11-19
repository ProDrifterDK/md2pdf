from pygments.formatters import HtmlFormatter
from pygments.styles import get_style_by_name

# Intentaremos usar el estilo 'material' o 'dracula' si están disponibles,
# ya que son muy similares a VS Code Dark.
# Si no, usaremos 'monokai' pero ajustaremos el fondo manualmente en el CSS.

# List available styles to be sure
from pygments.styles import get_all_styles
styles = list(get_all_styles())
print(f"Available styles: {styles}")

# Prefer 'material' or 'dracula' for VS Code look
selected_style = 'monokai' # Fallback
if 'material' in styles:
    selected_style = 'material'
elif 'dracula' in styles:
    selected_style = 'dracula'
elif 'one-dark' in styles:
    selected_style = 'one-dark'

print(f"Selected style: {selected_style}")

formatter = HtmlFormatter(style=selected_style, cssclass='codehilite')
css_content = formatter.get_style_defs('.codehilite')

print("-" * 20)
print(css_content)
print("-" * 20)