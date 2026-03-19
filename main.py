# Scraping de RSS con BeautifulSoup de la página de El País
# Sacar título y fecha de publicación y crear un archivo HTML con los resultados

import requests
from bs4 import BeautifulSoup
from jinja2 import Environment, FileSystemLoader

# Dirección RSS de El País
url = "https://feeds.elpais.com/mrss-s/pages/ep/site/elpais.com/section/tecnologia/portada"

# Agregar un User-Agent para evitar bloqueos por parte del servidor
headers = {
    "User-Agent": "Mozilla/5.0"
}

# Realizar la solicitud HTTP al RSS
response = requests.get(url, headers=headers)

# Verificar que la solicitud fue exitosa
if response.status_code == 200:
    print("La petición fue exitosa.")

# Parsear el contenido XML del RSS con BeautifulSoup
soup = BeautifulSoup(response.content, 'xml')

# Encontrar todos los elementos <item> que representan cada noticia
articulos = soup.find_all('item')

# Crear lista de diccionarios para guardar los datos
noticias = []

# Recorrer cada artículo y extraer su información
for articulo in articulos:
    titulo = articulo.title.text if articulo.title else "Sin título"
    fecha = articulo.pubDate.text if articulo.pubDate else "Sin fecha"
    enlace = articulo.link.text if articulo.link else "#"
    
    # Extraer imagen (varias fuentes posibles)
    imagen = ""
    media_content = articulo.find('media:content')
    enclosure = articulo.find('enclosure')
    if media_content and media_content.has_attr('url'):
        imagen = media_content['url']
    elif enclosure and enclosure.has_attr('url'):
        imagen = enclosure['url']
        
    # Añadir a la lista 
    noticias.append({
        'imagen': imagen,
        'titulo': titulo,
        'fecha': fecha,
        'enlace': enlace,
    })

# Generar un archivo de texto con los resultados y mostrar por pantalla
with open("noticias_tecnologia.txt", "w", encoding="utf-8") as archivo_txt:
    for noticia in noticias:
        print(f"TÍTULO: {noticia['titulo']} - FECHA: {noticia['fecha']} - ENLACE: {noticia['enlace']}")
        archivo_txt.write(f"TÍTULO: {noticia['titulo']} - FECHA: {noticia['fecha']} - ENLACE: {noticia['enlace']}\n")


# Configurar Jinja2 para cargar la plantilla HTML
env = Environment(loader=FileSystemLoader('.'))
template = env.get_template('template.html')

# Renderizar la plantilla con los datos
html_renderizado = template.render(noticias=noticias)

# Guardar el HTML
with open("noticias.html", "w", encoding="utf-8") as archivo_html:
    archivo_html.write(html_renderizado)

print("Archivo 'noticias.html' generado exitosamente.")
