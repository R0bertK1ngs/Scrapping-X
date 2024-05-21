from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time

# Credenciales de Twitter
username = 'El_Infunabl3' #usuario twitter
password = '149)/SmB<6' #contraseña twitter

# URL del tweet
tweet_url = 'https://x.com/Cooperativa/status/1792170942661046686'

# Inicializar el ChromeDriver
try:
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
except Exception as e:
    print(f"Error al iniciar el ChromeDriver: {e}")
    exit()

# Navegar a la página de inicio de sesión
driver.get('https://twitter.com/login')
time.sleep(5)  # Esperar a que la página de inicio de sesión se cargue

# Iniciar sesión en Twitter
try:
    username_field = driver.find_element(By.NAME, 'text')
    username_field.send_keys(username)
    username_field.send_keys(Keys.RETURN)
    time.sleep(3)

    password_field = driver.find_element(By.NAME, 'password')
    password_field.send_keys(password)
    password_field.send_keys(Keys.RETURN)
    
    time.sleep(5)  # Esperar a que el inicio de sesión se complete
except Exception as e:
    print(f"Error al iniciar sesión: {e}")
    driver.quit()
    exit()

# Navegar a la URL del tweet
try:
    driver.get(tweet_url)
    time.sleep(5)  # Esperar a que la página del tweet se cargue completamente
except Exception as e:
    print(f"Error al navegar a la URL del tweet: {e}")
    driver.quit()
    exit()
    
# Capturar el primer comentario (texto de la publicación original)
try:
    first_comment = driver.find_element(By.CSS_SELECTOR, 'div[data-testid="tweetText"]').text
except Exception as e:
    print(f"Error al capturar el primer comentario: {e}")
    first_comment = ""

# Desplazarse hacia abajo para cargar más comentarios
"""body = driver.find_element(By.TAG_NAME, 'body')
for _ in range(4):  # Ajusta el rango según la cantidad de comentarios
    body.send_keys(Keys.PAGE_DOWN)
    time.sleep(2)
"""
body = driver.find_element(By.TAG_NAME, 'body')
last_height = driver.execute_script("return document.body.scrollHeight")
scroll_attempts = 0
max_scroll_attempts = 100  # Ajusta este número según sea necesario

while scroll_attempts < max_scroll_attempts:
    body.send_keys(Keys.PAGE_DOWN)
    time.sleep(3)  # Espera 3 segundos para cargar nuevos comentarios
    new_height = driver.execute_script("return document.body.scrollHeight")
    if new_height == last_height:  # No hay más contenido cargado
        break
    last_height = new_height
    scroll_attempts += 1

# Extraer los comentarios
try:
    comments = driver.find_elements(By.CSS_SELECTOR, 'div[data-testid="tweetText"]')
    with open("comentarios.txt", "w", encoding="utf-8") as file:
        # Guardar el primer comentario
        if first_comment:
            print(f"Publicación original: {first_comment}\n")
            file.write(f"Publicación original:\n{first_comment}\n\n")
        # Guardar los comentarios
        for index, comment in enumerate(comments, start=1):
            comment_text = comment.text.strip()
            print(f"Comentario {index}: {comment_text}\n")
            file.write(f"{index}. {comment_text}\n\n")
    print("Comentarios guardados en 'comentarios.txt'.")
except Exception as e:
    print(f"Error al extraer comentarios: {e}")

# Cerrar el navegador
driver.quit()