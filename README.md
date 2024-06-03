# Scrapping-X
# Twitter Scraper

Este proyecto es una herramienta para realizar scraping de comentarios en publicaciones de Twitter utilizando Selenium y almacenar los datos en una base de datos Supabase.

## Requisitos

- Python 3.6 o superior
- pip
- Google Chrome
- [Chromedriver](https://chromedriver.chromium.org/downloads)

## Instalación

1. Clona este repositorio:
    ```bash
    git clone https://github.com/R0bertK1ngs/Scrapping-X
    cd Scrapping-X
    ```

2. Instala las dependencias:
    ```bash
    pip install -r requirements.txt
    ```

3. Configura tu entorno:
    - Asegúrate de tener Google Chrome instalado.
    - Descarga y coloca `chromedriver` en tu PATH o en el mismo directorio del proyecto.

## Archivos del Proyecto

### `twitter_scraper.py`

Este archivo contiene las funciones principales para realizar el scraping de comentarios en Twitter y almacenarlos en una base de datos Supabase.

- `validar_url(linkscrap, minero)`: Valida si la URL ya ha sido scrappeada y, de no ser así, la inserta en la base de datos.
- `Extraer_Comentarios(driver, tweet_url, minero, id_url)`: Extrae los comentarios de la URL proporcionada y los almacena en la base de datos.

### `interfaz.py`

Este archivo contiene la interfaz gráfica de usuario (GUI) construida con Tkinter. Permite al usuario ingresar la URL del tweet y el nombre del minero.

- `create_gui()`: Crea y muestra la interfaz gráfica.
- `on_scrape_button_click(url_entry, minero_entry, scrape_button, loading_label)`: Maneja el evento de clic en el botón de scraping.
- `run_scraping(tweet_url, minero, scrape_button, loading_label)`: Ejecuta el scraping en un hilo separado.

### `main.py`

Este archivo es el punto de entrada principal del programa. Inicializa el navegador, maneja las cookies y llama a las funciones de scraping.

- `start_scraping(tweet_url, minero)`: Inicia el proceso de scraping para la URL y minero proporcionados.

### `cookies.py`

Este archivo contiene funciones para guardar y cargar cookies utilizando pickle.

- `save_cookies(driver, path)`: Guarda las cookies del navegador en un archivo.
- `load_cookies(driver, path)`: Carga las cookies desde un archivo y las añade al navegador.

### `requirements.txt`

Este archivo contiene las dependencias necesarias para ejecutar el proyecto.

## Uso

1. Ejecuta la interfaz gráfica:
    ```bash
    python main.py
    ```

2. Ingresa la URL del tweet y el nombre del minero en la interfaz gráfica.

3. Haz clic en "Iniciar Scraping".

## Contribución

Las contribuciones son bienvenidas. Por favor, abre un issue o envía un pull request para mejoras y correcciones.

