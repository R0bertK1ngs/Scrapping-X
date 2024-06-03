import time
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from supabase import create_client, Client
from datetime import datetime
import sys

# -----CONFIGURACIONES SUPABASE-----
url = "https://vrdvsuoyecwnqqpjfrzs.supabase.co"
key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InZyZHZzdW95ZWN3bnFxcGpmcnpzIiwicm9sZSI6ImFub24iLCJpYXQiOjE3MTYwOTEzMzcsImV4cCI6MjAzMTY2NzMzN30.0V-0HYbfxjhGJBUEE8DQK0tbyWmCLCMp1NP40AEXShw"
supabase: Client = create_client(url, key)
id_url_paracom = -1

# Iniciar sesión en Twitter (esta función no ha cambiado)
def login_twitter(driver, login_url):
    driver.get(login_url)
    print("Por favor, inicia sesión manualmente en Twitter.")
    time.sleep(150)  # Tiempo para iniciar sesión manualmente

def validar_url(linkscrap,minero):
    global id_url_paracom
    try:
        # Verificar si la URL ya existe en la base de datos
        response = supabase.table('URLS').select('ruta').eq('ruta', linkscrap).execute()
        if response.data:
            print("La URL ya ha sido scrappeada anteriormente. Cerrando el programa.")
            sys.exit()
        else:
            # Insertar la nueva URL en la base de datos y obtener el ID
            insert_response = supabase.table('URLS').insert({
                'ruta': linkscrap,
                'minero': minero,
                'fecha_add': datetime.utcnow().isoformat() + 'Z',
                'red_social': 'X'
            }).execute()

            # Recuperar el ID de la URL insertada
            if insert_response.data:
                url_id = insert_response.data[0]['id_url']
                print(f"La URL ha sido registrada con ID: {url_id}")
                id_url_paracom = url_id
            else:
                print("Error al insertar la URL.")
                return None
    except Exception as e:
        print("Error al validar o insertar la URL:", e)
        return None

def Extraer_Comentarios(driver, tweet_url,minero,id_url):
    # Validar la URL antes de proceder
    validar_url(tweet_url,minero)

    try:
        driver.get(tweet_url)
        time.sleep(2)  # Esperar a que la página del tweet se cargue completamente
    except Exception as e:
        print(f"Error al navegar a la URL del tweet: {e}")
        driver.quit()
        exit()

    # Intentar hacer clic en el botón "Mostrar más comentarios" varias veces
    while True:
        try:
            show_more_button = driver.find_element(By.XPATH, '//button[@role="button" and .//span[contains(text(), "Mostrar más respuestas")]]')
            driver.execute_script("arguments[0].click();", show_more_button)
            time.sleep(3)  # Esperar a que se carguen los comentarios adicionales
        except NoSuchElementException:
            break

    body = driver.find_element(By.TAG_NAME, 'body')
    for _ in range(40):  # Ajusta el rango según la cantidad de comentarios
        body.send_keys(Keys.PAGE_DOWN)
        time.sleep(1)

    # Extraer los comentarios
    try:
        users = driver.find_elements(By.CSS_SELECTOR, 'div[data-testid="User-Name"]')
        comments = driver.find_elements(By.CSS_SELECTOR, 'div[data-testid="tweetText"]')
        dates = driver.find_elements(By.CSS_SELECTOR, 'a > time')

        if not comments:
            print("No se encontraron comentarios con el selector actual.")
        else:
            for user, comment, date in zip(users, comments, dates):
                user_name = user.find_element(By.CSS_SELECTOR, 'span.css-1jxf684').text
                comment_text = comment.text
                comment_date = datetime.strptime(date.get_attribute('datetime'), '%Y-%m-%dT%H:%M:%S.%fZ').strftime('%Y-%m-%d %H:%M:%S')
                fecha_add = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                
                data = {                       # Creacion de diccionario data
                    "usuario": user_name,
                    "comentario": comment_text,
                    "fecha_com": comment_date,
                    "minero": minero,
                    "fecha_add": fecha_add,
                    'id_url': id_url_paracom
                }
                response = supabase.table("Comentarios").insert(data).execute()
                print(f"Insertado: {response.data}")
    except Exception as e:
        print(f"Error al extraer comentarios: {e}")
