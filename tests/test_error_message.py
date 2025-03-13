import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException


@pytest.fixture
def driver():
    driver_path = r"C:\chromedriver-win64\chromedriver.exe"
    service = Service(driver_path)
    driver = webdriver.Chrome(service=service)
    yield driver
    driver.quit()


def test_login_already_used(driver):
    driver.get("https://party.videomost.com/service/welcome")

    # Открытие страницы регистрации посредством клика по ссылке
    WebDriverWait(driver, 15).until(
        EC.element_to_be_clickable((By.XPATH, "//p[@class='link' and text()='Зарегистрироваться']"))
    ).click()

    # Ожидаем форму регистрации
    WebDriverWait(driver, 15).until(EC.visibility_of_element_located((By.NAME, "email")))

    # Форма регистрации - заполнение полей данными, которые уже используются
    driver.find_element(By.NAME, "email").send_keys("victor1004@internet.ru")
    driver.find_element(By.NAME, "firstname").send_keys("Victor")
    driver.find_element(By.NAME, "lastname").send_keys("Win 11 Chrome")
    driver.find_element(By.NAME, "password").send_keys("qwerty1234")
    driver.find_element(By.NAME, "cpassword").send_keys("qwerty1234")

    # Клик по кнопке регистрации
    WebDriverWait(driver, 15).until(
        EC.element_to_be_clickable((By.CLASS_NAME, "button-ok"))
    ).click()

    # Проверка на наличие сообщения "Логин уже используется"
    try:
        # Ожидаемый текст сообщения
        error_message_text = 'Логин уже используется'

        # Ожидание появления сообщения на странице
        error_message = WebDriverWait(driver, 30).until(
            EC.visibility_of_element_located((By.XPATH, f"//p[@class='error-text' and contains(text(),'{error_message_text}')]"))
        )

        # Проверка, что сообщение отображается
        assert error_message.is_displayed(), "Ожидаемое сообщение 'Логин уже используется' не отображено."

        # Если сообщение отображается, тест пройден
        print("Тест завершён успешно: сообщение 'Логин уже используется' отображено.")

    except TimeoutException:
        # Если сообщение не найдено в течение 30 секунд, тест не пройден
        pytest.fail("Ошибка: сообщение 'Логин уже используется' не отображено.")