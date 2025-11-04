from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import random
from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException, TimeoutException
from urllib.parse import urlparse, parse_qs


def human_sleep(min_sec=0.8, max_sec=2.4):
    jitter = random.uniform(-0.1, 0.2)
    time.sleep(max(0.3, random.uniform(min_sec, max_sec) + jitter))


def slow_typing(element, text, delay_range=(0.08, 0.22)):
    for char in text:
        element.send_keys(char)
        time.sleep(random.uniform(*delay_range))


def hover_and_click(element, driver):
    ActionChains(driver).move_to_element(element).pause(random.uniform(0.3, 0.8)).click().perform()
    human_sleep()


def wait_and_find(driver, by, selector, timeout=10):
    try:
        return WebDriverWait(driver, timeout).until(EC.presence_of_element_located((by, selector)))
    except TimeoutException:
        return None


def get_current_horse_id(driver):
    try:
        url = driver.current_url
        parsed = urlparse(url)
        query = parse_qs(parsed.query)
        return query.get("id", [None])[0]
    except Exception:
        return None


# sprawdzamy czy nie lata ufo
def click_ufo(driver):
    try:
        ufo = WebDriverWait(driver, 3).until(
            EC.presence_of_element_located((By.CLASS_NAME, "ufo--moving"))
        )
        print("UFO lata")
        try:
            ufo.click()
            print("UFO klikniete")
            human_sleep(1, 2)
        except ElementClickInterceptedException:
            print("UFO zaslania")
            human_sleep(2, 3)
            return click_ufo(driver)

        # Kliknij przycisk OK
        ok_btn = WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((By.XPATH, "//span[text()='Ok']"))
        )
        hover_and_click(ok_btn, driver)
        print("UFO ZLAPANE!.")
        human_sleep(1, 2)

    except TimeoutException:
        pass  # UFO nie ma

# --- Konfiguracja przeglądarki ---
options = webdriver.FirefoxOptions()
options.set_preference("dom.webdriver.enabled", False)
options.set_preference('useAutomationExtension', False)


browser = webdriver.Firefox(options=options)
browser.get("https://www.howrse.pl/site/logIn")
print("Logowanie...")

# Akceptuj cookies
cookie_btn = wait_and_find(browser, By.XPATH, '/html/body/div[7]/main/aside/div/article/div/div[2]/div/div/div[2]/form/button')
if cookie_btn:
    hover_and_click(cookie_btn, browser)

# Login
userLogin = wait_and_find(browser, By.ID, "login")
if userLogin:
    slow_typing(userLogin, "login")  # <-- Twój login
    human_sleep()

# Hasło
passwordElem = wait_and_find(browser, By.ID, "password")
if passwordElem:
    slow_typing(passwordElem, "haslo")  # <-- Twoje hasło
    human_sleep()


submitBtn = wait_and_find(browser, By.ID, "authentificationSubmit")
if submitBtn:
    hover_and_click(submitBtn, browser)

human_sleep(2, 4)

# --- Przejście do konia ---
print("Szukanie pierwszego konia...")
browser.get("https://www.howrse.pl/elevage/chevaux/cheval?id=") # pamietaj o podaniu id pierwszego konia
human_sleep(2, 4)

# --- Pętla oporządzania ---

while True:
    try:
        horse_id = get_current_horse_id(browser)
        if horse_id:
            last_horse_id = horse_id
            print(f"Pracuję nad koniem ID: {last_horse_id}")

        click_ufo(browser)
        # odbiór porodu
        try:
            klacz = get_current_horse_id(browser)
            browser.find_element(By.ID, "boutonVeterinaire")
            browser.find_element(By.ID, "boutonVeterinaire").click()
            human_sleep(2, 5)
            browser.find_element(By.CLASS_NAME, "input").send_keys("Krezus Junior")
            browser.find_element(By.XPATH, "//span[text()='Kontynuuj']").click()
            browser.get(f"https://www.howrse.pl/elevage/chevaux/cheval?id={klacz}")
            human_sleep(2, 5)
        except NoSuchElementException:
            pass

        try:
            browser.find_element(By.XPATH, "//a[contains(@class, 'panser') and contains(@class, 'action-disabled')]")
            oporzadzony = True
        except NoSuchElementException:
            oporzadzony = False

        try:
            browser.find_element(By.ID, "boutonAllaiter")
            zreb = True
        except NoSuchElementException:
            zreb = False

        if zreb:
            if not oporzadzony:
                browser.find_element(By.ID, "boutonAllaiter").click()
                human_sleep()
                browser.find_element(By.ID, "boutonPanser").click()
                human_sleep()
                browser.find_element(By.ID, "boutonCoucher").click()
            else:
                browser.find_element(By.ID, "nav-next").click()
                continue
        else:
            try:
                browser.find_element(By.XPATH, "//span[text()=' w ośrodku jeździeckim, aby położyć go spać już teraz!']")
                pozaOsrodkiem = True
            except NoSuchElementException:
                pozaOsrodkiem = False

            if pozaOsrodkiem:
                browser.find_element(By.XPATH, "//a[text()='Zarejestruj swojego konia']").click()
                human_sleep(3, 5)
                browser.find_element(By.XPATH, "//a[text()='60 dni']").click()
                human_sleep(2, 4)
                try:
                    browser.find_element(By.XPATH, "//strong[text()='1 200']").click()
                except Exception:
                    browser.find_element(By.XPATH, "//strong[text()='1 200']").click()
                human_sleep(2, 4)

            if not oporzadzony:
                browser.find_element(By.ID, "boutonCoucher").click()
                human_sleep()
                browser.find_element(By.ID, "boutonPanser").click()
                human_sleep()
                browser.find_element(By.ID, "boutonNourrir").click()
                human_sleep()

                try:
                    browser.find_element(By.XPATH, "//span[contains(text(),'niedowagę')]")
                    browser.find_element(By.XPATH, "//span[text()='20']").click()
                    human_sleep()
                    browser.find_element(By.ID, "feed-button").click()
                except NoSuchElementException:
                    try:
                        browser.find_element(By.XPATH, "//span[contains(text(),'zbyt gruba') or contains(text(),'zbyt gruby')]")
                        browser.find_element(By.CLASS_NAME, "float-right").click()
                    except NoSuchElementException:
                        iloscZarcia = browser.find_element(By.CLASS_NAME, "section-fourrage-target").text
                        browser.find_element(By.XPATH, f"//span[contains(@class, 'slider-number') and text()='{iloscZarcia}']").click()
                        human_sleep()
                        browser.find_element(By.ID, "feed-button").click()

            try:
                zlecenie_klik = browser.find_element(By.XPATH, "//a[contains(@class, 'missionEquus') or contains(@class, 'missionForet')  or contains(@class, 'missionMontagne')]")
                zlecenie_klik.click()
                human_sleep()
            except NoSuchElementException:
                pass

        browser.find_element(By.ID, "nav-next").click()
        human_sleep()

    except Exception as e:
        print(f" Wystąpił wyjątek: {e}")
        if last_horse_id:
            print(f"WARN: Powrót do konia {last_horse_id}")
            browser.get(f"https://www.howrse.pl/elevage/chevaux/cheval?id={last_horse_id}")
            human_sleep(2, 5)
        else:
            print(" Brak ID konia — przerywam")
            break
