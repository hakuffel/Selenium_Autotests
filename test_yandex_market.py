"""
Набор тестов для yandex маркета
"""
import pytest
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.keys import Keys


@pytest.fixture
def browser():
    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
    driver.implicitly_wait(5)
    yield driver
    driver.quit()

def click_popup_offset(browser):
    """
    Ожидание popup сообщения для неавторизованного пользователя
    """
    wait = WebDriverWait(browser, 10)
    popup = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "._2veCe")))
    action = ActionChains(browser)
    action.move_to_element_with_offset(popup, 200, 300).click().perform()


def test_url(browser):
    """
    Проверка нужного раздела в url
    """
    browser.get("https://market.yandex.ru/")
    click_popup_offset(browser)
    button_catalog = browser.find_element(By.CSS_SELECTOR, ".cia-vs > :nth-child(1) > ._30-fz")
    button_catalog.click()
    button_hover = browser.find_element(By.CSS_SELECTOR, ":nth-child(9) > ._3yHCR")
    actions = ActionChains(browser)
    actions.move_to_element(button_hover).perform()
    button_coffee = browser.find_element(By.CSS_SELECTOR, ":nth-child(1) > :nth-child(1) > .aCbqK > :nth-child(1) > div > ._2re3U")
    button_coffee.click()
    url = browser.current_url
    assert "https://market.yandex.ru/catalog--kofe" in url, "url не соответствует ожидаемому"

def test_buy_without_auth(browser):
    """
    Проверка добавления товара в корзину без авторизации
    """
    browser.get("https://market.yandex.ru/")
    click_popup_offset(browser)
    search = browser.find_element(By.ID, "header-search")
    search.send_keys("Растворимый кофе MacCoffee Latte al Caramello, в пакетиках, 20 уп.")
    search.send_keys(Keys.ENTER)
    product = browser.find_element(By.XPATH, "//span[text()='Растворимый кофе MacCoffee Latte al Caramello, в пакетиках, 20 уп., ']")
    product.click()
    browser.switch_to.window(browser.window_handles[-1])
    buy_button = browser.find_element(By.CSS_SELECTOR, "._23gJ9 > ._1MOwX > :nth-child(2) > :nth-child(1) > ._1h7OY > ._30-fz")
    buy_button.click()
    wait = WebDriverWait(browser, 5)
    popup_message = wait.until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, "._3Iu-H.cia-vs"))
    )
    # print(f"Full popup text:\n{popup_message.text}")
    assert "Войдите в аккаунт" in popup_message.text, "Текст в popup не найден"


def test_copy_product_link(browser):
    """
    Проверка копирования ссылки продукта
    """
    browser.get("https://market.yandex.ru/card/rastvorimyy-kofe-maccoffee-v-paketikakh-20-up-440-g/103579544192")
    click_popup_offset(browser)
    share_button = browser.find_element(By.CSS_SELECTOR, "[data-zone-name='shareButton'] > ._2AXg-")
    share_button.click()
    wait = WebDriverWait(browser, 5)
    tooltip = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "div._35Xgn[role='tooltip']")))
    assert "Ссылка скопирована" in tooltip.text, "Текст не найден"

