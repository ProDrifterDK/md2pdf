import sys
import os
import markdown
from playwright.sync_api import sync_playwright

# --- INICIO: FUNCIÓN DE PREPROCESAMIENTO AVANZADO (OPCIONAL) ---
# Esta función representa el enfoque programático. Se recomienda mantenerla
# comentada y usar la solución CSS como método principal. Actívela solo si
# necesita un control granular sobre los puntos de ruptura de línea.

# def preprocess_markdown_for_wrapping(md_content: str, threshold: int = 80, break_interval: int = 15) -> str:
#     """
#     Preprocesa el contenido Markdown para insertar inteligentemente etiquetas <wbr>
#     en cadenas largas e indivisibles dentro de bloques de código cercados.
#     """
#     code_block_pattern = re.compile(r'(```[a-zA-Z]*\n)(.*?)(```)', re.DOTALL)
#
#     def process_code_block(match):
#         header, code, footer = match.group(1), match.group(2), match.group(3)
#         processed_lines =
#         for line in code.split('\n'):
#             long_word_pattern = re.compile(rf'([^\s]{{{threshold},}})')
#
#             def inject_wbr_into_word(word_match):
#                 word = word_match.group(1)
#                 parts = [word[i:i+break_interval] for i in range(0, len(word), break_interval)]
#                 return '<wbr>'.join(parts)
#
#             processed_line = long_word_pattern.sub(inject_wbr_into_word, line)
#             processed_lines.append(processed_line)
#
#         processed_code = '\n'.join(processed_lines)
#         return f"{header}{processed_code}{footer}"
#
#     return code_block_pattern.sub(process_code_block, md_content)
# --- FIN: FUNCIÓN DE PREPROCESAMIENTO AVANZADO ---


def convertir_md_a_pdf(input_md_file: str, output_pdf_file: str, css_file: str = None):
    """
    Convierte un archivo Markdown a un PDF utilizando Playwright.
    Este enfoque utiliza un navegador sin interfaz para una renderización de alta calidad.

    :param input_md_file: La ruta al archivo Markdown de entrada.
    :param output_pdf_file: La ruta al archivo PDF de salida.
    :param css_file: La ruta a un archivo CSS opcional para estilizar el PDF.
    """
    try:
        # Lee el contenido del archivo Markdown
        with open(input_md_file, 'r', encoding='utf-8') as f:
            md_content = f.read()

        # --- Punto de integración para el preprocesamiento opcional ---
        # Si decide usar el enfoque programático, descomente la siguiente línea:
        # md_content = preprocess_markdown_for_wrapping(md_content)
        # -------------------------------------------------------------

        # Convierte Markdown a HTML usando 'python-markdown'
        # Usamos las extensiones 'fenced_code' y 'tables' para un mejor soporte de GFM
        html_body = markdown.markdown(md_content, extensions=['fenced_code', 'tables'])

        # Lee el contenido del archivo CSS si se proporciona
        custom_css = ""
        if css_file and os.path.exists(css_file):
            with open(css_file, 'r', encoding='utf-8') as f:
                custom_css = f.read()
        
        # Crea la plantilla HTML completa, incluyendo el CSS
        html_template = f"""
        <!DOCTYPE html>
        <html lang="es">
        <head>
            <meta charset="UTF-8">
            <title>Documento convertido a PDF</title>
            <style>
                {custom_css}
            </style>
        </head>
        <body>
            {html_body}
        </body>
        </html>
        """
        
        # Usa Playwright para generar el PDF
        print("Iniciando Playwright para convertir a PDF...")
        with sync_playwright() as p:
            browser = p.chromium.launch()
            page = browser.new_page()
            # Carga el contenido HTML en la página
            page.set_content(html_template)
            # Genera el PDF con un formato A4
            page.pdf(path=output_pdf_file, format="A4")
            browser.close()
        
        print(f"El archivo '{input_md_file}' ha sido convertido a '{output_pdf_file}' con éxito.")

    except FileNotFoundError:
        print(f"Error: No se encontró el archivo '{input_md_file}' o '{css_file}'.")
    except Exception as e:
        print(f"Ocurrió un error durante la conversión: {e}")

if __name__ == "__main__":
    if len(sys.argv) < 3 or len(sys.argv) > 4:
        print("Uso: python convertir_md.py <archivo_de_entrada.md> <archivo_de_salida.pdf> [archivo_de_estilo.css]")
        sys.exit(1)

    input_path = sys.argv[1]
    output_path = sys.argv[2]
    css_path = sys.argv[3] if len(sys.argv) == 4 else None
    
    convertir_md_a_pdf(input_path, output_path, css_path)