from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image
from clientes import cargar_datos
import json

def obtener_informacion_por_id(id_buscado):
    with open('clientes.json', 'r') as archivo:
        usuarios = json.load(archivo)

    for usuario in usuarios:
        if usuario['id'] == id_buscado:
            return usuario

    return None  # Retorna None si no se encuentra el usuario con el ID especificado

def generar_pdf(nombre_cliente, descripcion_pedido, total, fecha_entrega, fecha_recoger):
    inforCliente=obtener_informacion_por_id(nombre_cliente)

    # Ruta donde se guardará el PDF
    ruta_pdf = f"reportes/{inforCliente['nombre'].replace(' ', '_')}_pedido.pdf"

    # Crear un objeto PDF
    pdf = SimpleDocTemplate(ruta_pdf, pagesize=letter)

    # Configurar el estilo del documento
    estilos = getSampleStyleSheet()
    estilo_normal = estilos['Normal']
    estilo_titulo = estilos['Heading1']

    # Configurar el logo
    logo_path = "logo.png"
    logo = Image(logo_path, width=100, height=100)

    # Crear el contenido del PDF
    contenido = []
    contenido.append(logo)

    # Título
    contenido.append(Paragraph("Pedido - Sensacional Eventos", estilo_titulo))

    # Información del Cliente
    contenido.append(Spacer(1, 12))
    contenido.append(Paragraph(f"<b>Cliente:</b> {inforCliente['nombre']}", estilo_normal))
    contenido.append(Paragraph(f"<b>Dirección:</b> {inforCliente['direccion']}", estilo_normal))

    # Descripción del Pedido
    contenido.append(Spacer(1, 12))
    contenido.append(Paragraph("<b>Descripción del Pedido:</b>", estilo_normal))

    # Dividir la descripción en líneas si es necesario
    descripcion_lineas = descripcion_pedido.split('---')
    for linea in descripcion_lineas:
        contenido.append(Paragraph(linea, estilo_normal))

    # Información Adicional
    contenido.append(Spacer(1, 12))
    contenido.append(Paragraph(f"<b>Fecha de Entrega:</b> {fecha_entrega}", estilo_normal))
    contenido.append(Paragraph(f"<b>Fecha de Recoger:</b> {fecha_recoger}", estilo_normal))

    # Total
    contenido.append(Spacer(1, 12))
    contenido.append(Paragraph(f"<b>Total:</b> Q.{total:.2f}", estilo_normal))

    # Construir el PDF
    pdf.build(contenido)

    print(f"PDF generado y guardado en: {ruta_pdf}")


