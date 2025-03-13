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


def test_registration_with_empty_lastname(driver):
    driver.get("https://party.videomost.com/service/welcome")

    # Открытие страницы регистрации посредством клика по ссылке
    WebDriverWait(driver, 15).until(
        EC.element_to_be_clickable((By.XPATH, "//p[@class='link' and text()='Зарегистрироваться']"))
    ).click()

    # Ожидаем форму регистрации
    WebDriverWait(driver, 15).until(EC.visibility_of_element_located((By.NAME, "email")))

    # Заполнение полей формы регистрации
    driver.find_element(By.NAME, "email").send_keys("104@example.ru")
    driver.find_element(By.NAME, "firstname").send_keys("Victor")
    # Поле "Фамилия" оставляем пустым
    driver.find_element(By.NAME, "password").send_keys("qwerty1234")
    driver.find_element(By.NAME, "cpassword").send_keys("qwerty1234")

    # Клик по кнопке регистрации
    WebDriverWait(driver, 15).until(
        EC.element_to_be_clickable((By.CLASS_NAME, "button-ok"))
    ).click()

    # Проверка на наличие сообщения "Заполните это поле" для поля "Фамилия"
    try:
        error_message = WebDriverWait(driver, 30).until(
            EC.visibility_of_element_located((By.XPATH, "//input[@name='lastname' and @required='']"))
        )
        assert error_message.get_attribute("validationMessage") == "Заполните это поле.", "Сообщение не совпадает."
        print("Тест завершён успешно: сообщение 'Заполните это поле.' отображено для поля 'Фамилия'.")
    except TimeoutException:
        pytest.fail("Ошибка: сообщение 'Заполните это поле.' для поля 'Фамилия' не отображено.")