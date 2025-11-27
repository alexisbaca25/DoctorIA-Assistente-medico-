from PIL import Image, ImageDraw, ImageFont
import os
import textwrap

def generar_pdf_diagnostico(nombre_app, paciente_sintomas, resultado, recomendaciones_list=None, salida_path="diagnostico.pdf"):
    """
    Crea un PDF simple usando Pillow: renderiza texto sobre una imagen y la guarda como PDF.
    """
    # Tamaño A4 aproximado a 300 dpi => (2480 x 3508) but we'll use smaller for portability
    W, H = 1240, 1754
    img = Image.new("RGB", (W, H), "white")
    draw = ImageDraw.Draw(img)

    # Cargar una fuente
    try:
        font_title = ImageFont.truetype("DejaVuSans-Bold.ttf", 48)
        font_normal = ImageFont.truetype("DejaVuSans.ttf", 22)
    except Exception:
        font_title = ImageFont.load_default()
        font_normal = ImageFont.load_default()

    padding = 60
    y = padding

    draw.text((padding, y), nombre_app, font=font_title, fill=(20, 70, 130))
    y += 80

    draw.text((padding, y), "Diagnóstico generado:", font=font_normal, fill=(0,0,0))
    y += 35
    draw.text((padding, y), str(resultado), font=font_normal, fill=(0,0,0))
    y += 50

    draw.text((padding, y), "Síntomas seleccionados:", font=font_normal, fill=(0,0,0))
    y += 30
    wrapped = textwrap.fill(", ".join(paciente_sintomas), width=80)
    draw.multiline_text((padding, y), wrapped, font=font_normal, fill=(0,0,0))
    y += 140

    if recomendaciones_list:
        draw.text((padding, y), "Recomendaciones sugeridas:", font=font_normal, fill=(0,0,0))
        y += 30
        for rec in recomendaciones_list:
            for line in textwrap.wrap("- " + rec, width=100):
                draw.text((padding+20, y), line, font=font_normal, fill=(0,0,0))
                y += 28
            y += 6

    # Footer
    draw.text((padding, H-80), "DoctorIA - Generado automáticamente", font=font_normal, fill=(120,120,120))

    # Guardar como PDF
    img.save(salida_path, "PDF", resolution=100.0)
    return salida_path
