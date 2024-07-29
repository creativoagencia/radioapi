# Extractor de Metadatos

🚀 Con implementación estándar en Digital Ocean

[![Deploy to DO](https://www.deploytodo.com/do-btn-blue.svg)](https://cloud.digitalocean.com/apps/new?repo=https://github.com/jailsonsb2/FastAPI-StreamTitle-Extractor/tree/main)

## Descripción general

FastAPI Stream Title Metadata Extractor es una aplicación sencilla que permite a los usuarios obtener el título de los metadatos de una transmisión de audio y extraer el artista y el nombre de la canción. Utiliza la biblioteca FastAPI para crear una API web que acepta la URL de una transmisión de audio MP3 como entrada y devuelve el nombre del artista y la canción en formato JSON.

Este repositorio sirve como modelo mínimo para implementar una aplicación FastAPI en Digital Ocean. Está diseñado para proporcionar una forma sencilla de ejecutar su aplicación FastAPI con la menor cantidad de dolores de cabeza y bloatware.

## Características

•⁠  ⁠Recuperación del título a partir de los metadatos de una transmisión de audio.
•⁠  ⁠Extracción del artista y el nombre de la canción del título de la transmisión.
•⁠  ⁠Configuración mínima de FastAPI
•⁠  ⁠Listo para implementar en Digital Ocean
•⁠  ⁠Configuraciones básicas para un inicio rápido

## Requiremientos

Antes de ejecutar la aplicación, asegúrese de tener instalado lo siguiente:
•⁠  ⁠Python 3.x
•⁠  ⁠FastAPI
•⁠  ⁠Uvicorn

## Inicio Rápido

1.⁠ ⁠Haga clic en el botón "Implementar para HACER" en la parte superior.
2.⁠ ⁠Siga las instrucciones de Digital Ocean para implementar su aplicación.
3.⁠ ⁠¡Disfruta de tu aplicación FastAPI ejecutándose en la nube!

---

### Recuperador de títulos de transmisión

Para recuperar el título de la transmisión y la imagen de portada, simplemente reemplace el parámetro URL en el enlace API que se proporciona a continuación:

*API Endpoint:* 
⁠ https://free.radioapi.lat/get_stream_title/?url= ⁠

*Ejemplo de Uso:*
Remplace ⁠ https://stream.zeno.fm/yn65fsaurfhvv ⁠ with your desired stream URL:

https://free.radioapi.lat/get_stream_title/?url=https://stream.zeno.fm/yn65fsaurfhvv
https://free.radioapi.lat/radio_info/?radio_url=https://stream.zeno.fm/yn65fsaurfhvv


Esto devolverá un enlace a la imagen de portada de la transmisión junto con el título.

--- 

## Contribution

¡Las contribuciones son bienvenidas! No dudes en abrir un problema o enviar una solicitud de extracción para recibir sugerencias, correcciones de errores o nuevas funciones.

¡Feliz codificación! 🎉
