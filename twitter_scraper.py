import time
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from supabase import create_client, Client
from datetime import datetime
import sys
import re
import unicodedata

# -----CONFIGURACIONES SUPABASE-----
url = "https://vrdvsuoyecwnqqpjfrzs.supabase.co"
key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InZyZHZzdW95ZWN3bnFxcGpmcnpzIiwicm9sZSI6ImFub24iLCJpYXQiOjE3MTYwOTEzMzcsImV4cCI6MjAzMTY2NzMzN30.0V-0HYbfxjhGJBUEE8DQK0tbyWmCLCMp1NP40AEXShw"
supabase: Client = create_client(url, key)
id_url_paracom = -1

# Iniciar sesión en Twitter
def login_twitter(driver, login_url):
    driver.get(login_url)
    print("Por favor, inicia sesión manualmente en Twitter.")
    time.sleep(150)  # Tiempo para iniciar sesión manualmente

def validar_url(linkscrap, minero):
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

def clean_text(text):
    text = unicodedata.normalize('NFKD', text)
    text = ''.join(c for c in text if unicodedata.category(c) != 'Mn' or c in 'áéíóúñÁÉÍÓÚÑ')
    text = re.sub(r'[^\w\s@]', '', text)
    text = re.sub(r'\s+', ' ', text)
    text = text.replace('\n', ' ')
    return text

def es_duplicado(user_name, comment_text, comment_date, recorded_comments):
    comment_id = (user_name, comment_text, comment_date)
    if comment_id in recorded_comments:
        return True
    else:
        recorded_comments.add(comment_id)
        return False

def Extraer_Comentarios(driver, tweet_url, minero, id_url):
    # Validar la URL antes de proceder
    validar_url(tweet_url, minero)

    try:
        driver.get(tweet_url)
        time.sleep(2)
    except Exception as e:
        print(f"Error al navegar a la URL del tweet: {e}")
        driver.quit()
        exit()

    body = driver.find_element(By.TAG_NAME, 'body')
    recorded_comments = set()
    comment_count = 0

    previous_comment_count = -1
    no_change_attempts = 0

    while no_change_attempts < 3:
        body.send_keys(Keys.PAGE_DOWN)
        time.sleep(1)

        try:
            users = driver.find_elements(By.CSS_SELECTOR, 'div[data-testid="User-Name"]')
            comments = driver.find_elements(By.CSS_SELECTOR, 'div[data-testid="tweetText"]')
            dates = driver.find_elements(By.CSS_SELECTOR, 'a > time')

            if not comments:
                print("No se encontraron comentarios con el selector actual.")
            else:
                nuevos_comentarios = []
                for user, comment, date in zip(users, comments, dates):
                    user_name = clean_text(user.find_element(By.CSS_SELECTOR, 'span.css-1jxf684').text.replace('@', ''))
                    comment_text = clean_text(comment.text)
                    comment_date = datetime.strptime(date.get_attribute('datetime'), '%Y-%m-%dT%H:%M:%S.%fZ').strftime('%Y-%m-%d %H:%M:%S')
                    fecha_add = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

                    if not es_duplicado(user_name, comment_text, comment_date, recorded_comments) and comment_text:
                        comment_count += 1
                        data = {
                            "usuario": user_name,
                            "comentario": comment_text,
                            "fecha_com": comment_date,
                            "minero": minero,
                            "fecha_add": fecha_add,
                            'id_url': id_url_paracom
                        }
                        nuevos_comentarios.append(data)

                for comentario in nuevos_comentarios:
                    response = supabase.table("Comentarios").insert(comentario).execute()
                    print(f"Insertado: {response.data}")

                if comment_count == previous_comment_count:
                    no_change_attempts += 1
                else:
                    no_change_attempts = 0
                previous_comment_count = comment_count

        except Exception as e:
            print(f"Error al extraer comentarios: {e}")
            no_change_attempts += 1

    print(f"Cantidad total de comentarios registrados: {comment_count}")
