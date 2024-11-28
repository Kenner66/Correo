CATEGORIAS_POR_PALABRAS = {
    "Trabajo": ["reunión", "proyecto", "cliente", "informe","trabajo"],
    "Personal": ["cumpleaños", "familia", "viaje", "amigo"],
    "Finanzas": ["factura", "pago", "banco", "transferencia"],
    "Promociones": ["oferta", "descuento", "promoción", "compra"],
    "Saludos": ["hola","saludos","bienvenido"],
    "Otros": []  # Categoría por defecto
}
def clasificar_por_asunto(asunto):
    """Clasifica el asunto de un correo según palabras clave."""
    asunto = asunto.lower()  # Convertir a minúsculas para evitar problemas de mayúsculas
    for categoria, palabras_clave in CATEGORIAS_POR_PALABRAS.items():
        for palabra in palabras_clave:
            if palabra in asunto:
                return categoria
    return "Otros"  # Categoría por defecto
