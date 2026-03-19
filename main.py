# Scraping de RSS con BeautifulSoup de la página de El País
# Sacar título y fecha de publicación

import requests
from bs4 import BeautifulSoup

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

# Recorrer cada artículo y extraer el título y la fecha de publicación y mostrarlos por pantalla
for articulo in articulos:
    titulo = articulo.title.text if articulo.title else "Sin título"
    fecha = articulo.pubDate.text if articulo.pubDate else "Sin fecha"
    print(f"TÍTULO: {titulo} - FECHA: {fecha}")

# Generar un archivo de texto con los resultados
with open("noticias_tecnologia.txt", "w", encoding="utf-8") as archivo:
    for articulo in articulos:
        titulo = articulo.title.text if articulo.title else "Sin título"
        fecha = articulo.pubDate.text if articulo.pubDate else "Sin fecha"
        archivo.write(f"TÍTULO: {titulo} - FECHA: {fecha}\n")

