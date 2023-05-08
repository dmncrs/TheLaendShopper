import logging
from time import sleep

from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.common.exceptions import TimeoutException
import json

logging.basicConfig()
logger = logging.getLogger('TheLaendShopper')
logger.setLevel(logging.DEBUG)
options = webdriver.ChromeOptions()

options.add_experimental_option('excludeSwitches', ['enable-logging'])



def main():
    driver = webdriver.Chrome(
        service= Service('D:\\Programmierung\\thelaend\\chromedriver.exe'), 
        options=options,
        desired_capabilities= {
            "resolution": "1920x1080"
        }
    )
    driver.get('https://shop.thelaend.de/sticker-set-nett-hier.html')
    logger.debug('Try to get sold out info')
    try:
        sold_out_elements: list[WebElement] = WebDriverWait(driver, 5).until(lambda d: d.find_elements(By.CLASS_NAME, 'ribbon-sold-out'))
    except TimeoutException:
        sold_out_elements = []

    if len(sold_out_elements) > 0:
        logger.info('Element sold out. Waiting for next turn :(')
        exit(0)
    
    logger.info('Item available try to order.')

    with open('buyer.json') as json_file:
        buyerData = json.load(json_file)
        logger.debug('Opened buyer file')
        for buyer in buyerData:
            if buyer['needed']:
                logger.info(f'Order TheLÄND Stickers for {buyer["name"]} {buyer["surname"]}')

                if driver is None:
                    driver = webdriver.Chrome(
                                service= Service('D:\\Programmierung\\thelaend\\chromedriver.exe'), 
                                options=options,
                                desired_capabilities= {
                                    "resolution": "1920x1080"
                                }
                            )
                driver.get('https://shop.thelaend.de/sticker-set-nett-hier.html')

                logger.debug('Accepting cookies...')

                cookieButton: WebElement = WebDriverWait(driver, 5).until(lambda d: d.find_element(By.CLASS_NAME, "as-oil__btn-optin"))
                cookieButton.click()

                logger.debug('Add elements to cart')

                buy_button: WebElement = WebDriverWait(driver, 5).until(lambda d: d.find_element(By.NAME, 'btn-add-to-cart'))
                buy_button.click()
                sleep(5)

                logger.debug('Change quantity to 5')

                driver.get('https://shop.thelaend.de/shopping_cart.php')

                qty_el: WebElement = WebDriverWait(driver, 5).until(lambda d: d.find_element(By.NAME, 'cart_quantity[]'))
                driver.execute_script("document.getElementsByName('cart_quantity[]')[0].setAttribute('value', 5)")

                logger.debug('Refresh site')

                refreshButton: WebElement = WebDriverWait(driver, 5).until(lambda d: d.find_element(By.CLASS_NAME, 'button-refresh'))
                refreshButton.click()
                sleep(5)

                logger.debug('Get to site to choose manual adress')

                driver.get('https://shop.thelaend.de/checkout_shipping.php')
                WebDriverWait(driver, 5).until(lambda d: d.find_element(By.CLASS_NAME, 'login-buttons'))

                logger.debug('Get to address information site')

                driver.get('https://shop.thelaend.de/shop.php?do=CreateRegistree&checkout_started=1')

                logger.debug('Fill form')

                genderButton: WebElement = WebDriverWait(driver, 5).until(lambda d: d.find_element(By.ID, 'gender-m'))
                genderButton.click()

                driver.execute_script(f"document.getElementById('firstname').value = '{buyer['name']}'")
                driver.execute_script(f"document.getElementById('lastname').value = '{buyer['surname']}'")    
                driver.execute_script(f"document.getElementById('email_address').value = '{buyer['email']}'")    
                driver.execute_script(f"document.getElementById('email_address_confirm').value = '{buyer['email']}'")
                driver.execute_script(f"document.getElementById('street_address').value = '{buyer['street']}'")
                driver.execute_script(f"document.getElementById('house_number').value = '{buyer['num']}'")
                driver.execute_script(f"document.getElementById('postcode').value = '{buyer['plz']}'")
                driver.execute_script(f"document.getElementById('city').value = '{buyer['city']}'")

                userButton: WebElement = WebDriverWait(driver, 5).until(lambda d: d.find_element(By.NAME, 'password-option'))
                userButton.click()

                privacyButton: WebElement = WebDriverWait(driver, 5).until(lambda d: d.find_element(By.ID, 'privacy_accepted'))
                privacyButton.click()
                sleep(5)
                
                nextBtnList: list[WebElement] = WebDriverWait(driver, 5).until(lambda d: d.find_elements(By.CLASS_NAME, 'btn.btn-primary.btn-block'))

                for nextBtn in nextBtnList:
                    if 'WEITER' in nextBtn.text.upper():
                        nextBtn.click()

                logger.debug('Next #2')
                sleep(5)
                
                nextBtnList: list[WebElement] = WebDriverWait(driver, 5).until(lambda d: d.find_elements(By.CLASS_NAME, 'btn.btn-primary.btn-block'))
                
                for nextBtn in nextBtnList:
                    if nextBtn.get_attribute('value') is None:
                        continue
                    if 'WEITER' in nextBtn.get_attribute('value').upper():
                        nextBtn.click()

                logger.debug('Next #3')
                sleep(5)

                nextBtnList: list[WebElement] = WebDriverWait(driver, 5).until(lambda d: d.find_elements(By.CLASS_NAME, 'btn.btn-primary.btn-block'))
                
                for nextBtn in nextBtnList:
                    if nextBtn.get_attribute('value') is None:
                        continue
                    if 'WEITER' in nextBtn.get_attribute('value').upper():
                        nextBtn.click()

                logger.debug('Checkout site reached. Checking out...')

                checkoutBtn: WebElement = WebDriverWait(driver, 5).until(lambda d: d.find_element(By.CLASS_NAME, 'checkout-confirmation-submit'))
                checkoutBtn.click()

                logger.info('Successfully checked out. See your TheLÄND stickers soon :D')
                driver.quit()
                driver = None

if __name__ == '__main__':
    main()
