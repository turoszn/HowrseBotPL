from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from random import randint
import time

# ponizej kod zmieniajacy rozmiar okna
# def set_viewport_size(driver, width, height):
#    window_size = driver.execute_script("""
#        return [window.outerWidth - window.innerWidth + arguments[0],
#          window.outerHeight - window.innerHeight + arguments[1]];
#       """, width, height)
#  browser.set_window_size(*window_size)


profile = webdriver.FirefoxProfile()
profile.set_preference("dom.webdriver.enabled", False)
profile.set_preference('useAutomationExtension', False)

browser = webdriver.Firefox(firefox_profile=profile)
user_agent = browser.execute_script("return navigator.userAgent;")
profile.set_preference("general.useragent.override", user_agent)
# set the viewport size to 800 x 600
# set_viewport_size(browser, 800, 600)

browser.get("https://www.howrse.pl/site/logIn")
print("Logowanie...")
# Zaakceptowanie cookies
browser.find_element_by_xpath('/html/body/aside/div/article/div/div[2]/div/div/div[3]/form/button').click()

try:
    userLogin = browser.find_element_by_id("login")
    userLogin.send_keys("login") # login gracza. Symulacja wpisania przed uruchomieniem należy podmienić
except NoSuchElementException:
    pass
try:
    passwordElem= browser.find_element_by_id("password")
    passwordElem.send_keys("haslo") # hasło gracza. Symulacja wpisania. Przed uruchomieniem należy podmienić
except NoSuchElementException:
    pass
submitButn= browser.find_element_by_id("authentificationSubmit")
submitButn.click() # kliknięcie "zaloguj"
time.sleep(randint(2, 5))

# To była część pierwsza teraz przejście do konii
print("Szukanie pierwszego konia...")
browser.get("link do pierwszego konia") # wklej tu link lub zakomentuj tą linijkę i odhacz linijki 48-49 żeby samo szukało pierwszego konia w zakładce "Inne"
time.sleep(randint(1, 5))
# browser.get("https://www.howrse.pl/elevage/chevaux/?elevage=all-horses") # link do zakładki. Defaultowo jest to zakładka "Inne"
# doKonika1 = browser.find_element_by_class_name("horsename").click()

# Jesteśmy u pierwszego konia. Czas na sittering
# kolejny = browser.find_element_by_id("nav-next")  # przycisk "kolejny"
# poprzedni = browser.find_element_by_id("nav-previous")  # przycisk "poprzedni"

while True:
    print("Oporzadzanie konia: ",i)
    try:  # sprawdzamy czy nie rodzi
        browser.find_element_by_id("boutonVeterinaire")
        rodzi = True
    except NoSuchElementException:
        rodzi = False
    if rodzi:
        current_url = browser.current_url
        browser.find_element_by_id("boutonVeterinaire").click()
        time.sleep(randint(2, 5))
        imie_zreba = browser.find_element_by_class_name("input")
        imie_zreba.send_keys("Krezus Junior")
        browser.find_element_by_xpath("//span[text()='Kontynuuj']").click()
        browser.get(current_url)
        time.sleep(randint(1, 5))
    try:  # sprawdzamy czy koń oporzadzony
        browser.find_element_by_xpath("//a[contains(@class, 'panser') and contains(@class, 'action-disabled')]")
        oporzadzony = True
    except NoSuchElementException:
        oporzadzony = False

    try:  # sprawdzamy czy koń to źreb
        browser.find_element_by_id("boutonAllaiter")
        zreb = True
    except NoSuchElementException:
        zreb = False
    if zreb:  # jeśli koń to źreb
        if not oporzadzony:
            butla = browser.find_element_by_id("boutonAllaiter").click()
            time.sleep(randint(0, 5))
            spanko = browser.find_element_by_id("boutonCoucher").click()
            time.sleep(randint(0, 5))
            czesanko = browser.find_element_by_id("boutonPanser").click()
        else:
                kolejny = browser.find_element_by_id("nav-next").click()
    else:
        try:  # sprawdzamy czy koń jest w ośrodku
            browser.find_element_by_xpath("//span[text()=' w ośrodku jeździeckim, aby położyć go spać już teraz!']")
            pozaOsrodkiem = True
        except NoSuchElementException:
            pozaOsrodkiem = False
        if pozaOsrodkiem:
                time.sleep(randint(2, 5))
                rejestracja = browser.find_element_by_xpath("//a[text()='Zarejestruj swojego konia']").click()
                time.sleep(randint(3, 5))
                dni60 = browser.find_element_by_xpath("//a[text()='60 dni']").click()
                time.sleep(randint(5, 6))
                eq1200 = browser.find_element_by_xpath("//strong[text()='1 200']").click()
                time.sleep(randint(2, 5))
        if not oporzadzony:
            spanko = browser.find_element_by_id("boutonCoucher").click()
            time.sleep(randint(0, 5))
            czesanko = browser.find_element_by_id("boutonPanser").click()
            time.sleep(randint(2, 5))
            siano = browser.find_element_by_id("boutonNourrir").click()
            time.sleep(randint(0, 5))
            nakarm = browser.find_element_by_id("feed-button")
            try:
                browser.find_element_by_xpath("//span[text()='Uwaga: Twoja klacz ma niedowagę, musisz jej podać następującą ilość paszy: 20, aby wróciła do formy!'] | //span[text()='Uwaga: jeden z Twoich koni ma niedowagę, musisz mu podać następującą ilość paszy: 20, aby wrócił do formy!'] ")
                uwagaChudy = True
            except NoSuchElementException:
                    uwagaChudy = False
            try:
                browser.find_element_by_xpath("//span[text()='Twoja klacz jest zbyt gruba. Nie karm jej dziś, aby mogła powrócić do normalnej wagi!'] | //span[text()='Twój koń jest zbyt gruby. Nie karm go dziś, aby mógł powrócić do normalnej wagi!']")
                uwagaGruby = True
            except NoSuchElementException:
                uwagaGruby = False
            if uwagaChudy:  # warunkowe karmienia gruby/chudy/normalny
                pasza20 = browser.find_element_by_xpath("//span[text()='20']").click()
                time.sleep(randint(0, 5))
                nakarm.click()
            elif uwagaGruby:
                niekarm = browser.find_element_by_class_name("float-right")
                time.sleep(randint(0, 5))
                niekarm.click()
            else:
                iloscZarcia = browser.find_element_by_class_name("section-fourrage-target")
                x = iloscZarcia.text
                paszaX = browser.find_element_by_xpath("//span[contains(@class, 'slider-number') and contains(text(), %s)]" % x).click()
                # paszaX = browser.find_element_by_xpath("//span[text()=%s]" % x).click()
                time.sleep(randint(0, 5))
                nakarm.click()

        try:  # sprawdzamy czy koń może robić zlecenia
            zlecenie_klik= browser.find_element_by_xpath("//a[contains(@class, 'missionEquus') or contains(@class, 'missionForet')  or contains(@class, 'missionMontagne')]")
            zlecenie1 = True
        except NoSuchElementException:
            zlecenie1 = False

        if zlecenie1:
            zlecenie_klik.click()
            time.sleep(randint(0, 5))
        else:
            kolejny = browser.find_element_by_id("nav-next").click()
            # kolejny = browser.find_element_by_id("nav-previous").click()
    kolejny = browser.find_element_by_id("nav-next").click()
     # kolejny = browser.find_element_by_id("nav-previous").click()
