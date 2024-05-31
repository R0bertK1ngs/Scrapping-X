import pickle
import os

# Función para guardar cookies
def save_cookies(driver, path):
    with open(path, 'wb') as filehandler:
        pickle.dump(driver.get_cookies(), filehandler)

# Función para cargar cookies
def load_cookies(driver, path):
    if os.path.exists(path):
        with open(path, 'rb') as cookiesfile:
            cookies = pickle.load(cookiesfile)
            for cookie in cookies:
                driver.add_cookie(cookie)
