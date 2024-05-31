from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time
import os
from cookies import save_cookies, load_cookies
from twitter_scraper import login_twitter, Extraer_Comentarios

'''
# Minero
minero = 'Robert Reyes'
'''

# Ruta para almacenar las cookies
cookies_path = 'twitter_cookies.pkl'

def start_scraping(tweet_url,minero):
    # Inicializar el ChromeDriver
    try:
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    except Exception as e:
        print(f"Error al iniciar el ChromeDriver: {e}")
        return

    # Verificar si las cookies existen
    if os.path.exists(cookies_path):
        # Cargar las cookies y navegar a la URL del tweet
        driver.get('https://twitter.com')
        time.sleep(3)  # Esperar a que la página de Twitter se cargue
        load_cookies(driver, cookies_path)
        driver.refresh()
        time.sleep(3)  # Esperar a que la página se recargue con las cookies
    else:
        # Iniciar sesión manualmente y guardar cookies
        login_twitter(driver, 'https://twitter.com/login')
        save_cookies(driver, cookies_path)

    Extraer_Comentarios(driver, tweet_url, minero,id_url=None)

    # Cerrar el navegador
    driver.quit()
    print("El scraping se ha completado correctamente.")

if __name__ == "__main__":
    from interfaz import create_gui
    create_gui()
