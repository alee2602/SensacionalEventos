from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image
from clientes import cargar_datos
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, Table, TableStyle
from db.conexiondb import obtener_clientes_bd_byId
import os

base_dir = os.path.abspath(os.path.dirname(__file__))
logo_path = os.path.join(base_dir, 'logo.png')

def obtener_informacion_por_id(id_buscado):
    return obtener_clientes_bd_byId(id_buscado)


def generar_pdf(id_cliente, descripcion_pedido, total, fecha_entrega, fecha_recoger):
    inforCliente = obtener_informacion_por_id(id_cliente)
    nombre_cliente = inforCliente.get('nombre', 'Cliente Desconocido').replace(' ', '_')
    # Formatear el nombre del archivo
    nombre_archivo = f"{nombre_cliente}_pedido.pdf"

    # Usar os.path.join para construir la ruta completa del archivo
    ruta_pdf = os.path.join(base_dir, 'reportes', nombre_archivo)
    c = canvas.Canvas(ruta_pdf, pagesize=letter)
    width, height = letter
    margin = 36  # Margen en puntos

    # Dibujar el margen rojo en cada lado
    c.setFillColorRGB(1, 0, 0)  # Rojo
    # Margen izquierdo
    c.rect(0, 0, margin, height, fill=1)
    # Margen derecho
    c.rect(width - margin, 0, margin, height, fill=1)
    # Margen inferior
    c.rect(0, 0, width, margin, fill=1)
    # Margen superior
    c.rect(0, height - margin, width, margin, fill=1)

    titulo=f"Pedido para {nombre_cliente}"
    c.setFont("Helvetica",20)
    c.drawString(200,600,titulo)

    c.drawImage(logo_path,60,620,width=100,height=100)


    c.setFont("Helvetica",16)
    c.setFillColorRGB(0, 0, 0)  # Negro
    c.drawString(80, 550, f'Direccion de entrega: {inforCliente.get("direccion")}')
    c.drawString(80, 520, f'Fecha de entrega: {fecha_entrega}')
    c.drawString(80, 490, f'Fecha para recoger: {fecha_recoger}')
    pedidoSeparado=str(descripcion_pedido).split(",")
    print(pedidoSeparado)
    for i in pedidoSeparado:
        print(i)
    
    c.setFont("Helvetica",10)
    inicialPedidos=460
    contador=0
    for i in pedidoSeparado:

        cadena = f"{str(i).replace('---', '------------------------------------')}"
        c.drawString(80,inicialPedidos,cadena)
        inicialPedidos-=15
        contador+=1
    c.setFont("Helvetica",16)
    c.drawString(80,inicialPedidos-30,f"Total: Q{total}")

    c.setLineWidth(0)  # Ancho de línea cero para que sea un cuadrado vacío
    c.rect(65, 65, 30, 30)  # Coordenadas x, y y tamaño del cuadrado
    c.drawString(100,75,"Cancelado y finalizado")


    


    



    





    c.save()

    



