from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from bs4 import BeautifulSoup
from selenium.webdriver.chrome.service import Service
from datetime import datetime, timedelta

# region Константы
LINKS = {'INDEX_LINK': 'http://127.0.0.1:5000/', 'LOGIN_LINK': 'login', 'REGISTRATION_LINK': 'register',
         'NEW_APPOINTMENT_LINK': 'new_appointment', 'EXISTING_APPOINTMENTS_LINK': 'appointment',
         'BILLS_LINK': 'bills', 'MEDICAL_HISTORY_LINK': 'medical_history',
         'COST_ACCOUNTING_LINK': 'cost_accounting', 'ORDERS_LINK': 'orders'}
"""Ссылки веб-сервиса."""

DATE_TIME_FORMAT = '%d.%m.%Y %H:%M'
"""Формат даты и времени."""

TIME_DELTA_DIFF = 3
"""Количество минут для допустимой разницы между объектами datetime при их сравнении."""
# endregion


def check_url(driver, current_url_check):
    """
    Проверяет, находится ли веб-драйвер на указанной странице, если нет, то переходит по этой ссылке.
    :param driver: Веб-драйвер для проверки.
    :param current_url_check: Ссылка для проверки.
    :return: Веб-драйвер.
    """
    if driver.current_url != current_url_check:
        driver.get(current_url_check)

    return driver


def login(driver, telno, password):
    """
    Ввод данных в форму входа.
    :param driver: Веб-драйвер.
    :param telno: Номер телефона.
    :param password: Пароль.
    :return: Содержимое страницы после нажатия на кнопку "Войти".
    """
    driver = check_url(driver, LINKS['INDEX_LINK'] + LINKS['LOGIN_LINK'])

    driver.find_element(By.ID, 'tel_no').send_keys(telno)
    driver.find_element(By.ID, 'password').send_keys(password)

    driver.find_element(By.ID, 'submit').submit()

    return driver.page_source


def registration(driver, surname, name, middle_name, birthday, telno, email, password, password_again):
    """
    Ввод данных в форму регистрации.
    :param driver: Веб-драйвер.
    :param surname: Фамилия.
    :param name: Имя.
    :param middle_name: Отчество.
    :param birthday: Дата рождения.
    :param telno: Номер телефона.
    :param email: Электронная почта.
    :param password: Пароль.
    :param password_again: Повтор пароля.
    :return: Содержимое страницы после нажатия на кнопку "Регистрация"
    """
    driver = check_url(driver, LINKS['INDEX_LINK'] + LINKS['REGISTRATION_LINK'])

    driver.find_element(By.ID, 'surname').send_keys(surname)
    driver.find_element(By.ID, 'user_name').send_keys(name)
    driver.find_element(By.ID, 'middle_name').send_keys(middle_name)
    driver.find_element(By.ID, 'birth_date').send_keys(birthday)
    driver.find_element(By.ID, 'tel_no').send_keys(telno)
    driver.find_element(By.ID, 'email').send_keys(email)
    driver.find_element(By.ID, 'password').send_keys(password)
    driver.find_element(By.ID, 'password2').send_keys(password_again)

    driver.find_element(By.ID, 'submit').submit()

    return driver.page_source


def new_appointment_select_service(driver, service_name):
    """
    Выбор услуги на странице создания новой записи.
    :param driver: Веб-драйвер.
    :param service_name: Название услуги.
    :return: Содержимое страницы после выбора.
    """
    driver = check_url(driver, LINKS['INDEX_LINK'] + LINKS['NEW_APPOINTMENT_LINK'])

    Select(driver.find_element(By.ID, 'select_service')).select_by_visible_text(service_name)
    return driver.page_source


def new_appointment_select_doctors(driver, doctor_name):
    """
    Выбор лечащего врача на странице создания новой записи.
    :param driver: Веб-драйвер.
    :param doctor_name: Полное имя врача.
    :return: Содержимое страницы после выбора.
    """
    driver = check_url(driver, LINKS['INDEX_LINK'] + LINKS['NEW_APPOINTMENT_LINK'])

    Select(driver.find_element(By.ID, 'select_doctors')).select_by_visible_text(doctor_name)

    return driver.page_source


def new_appointment_select_date(driver, date):
    """
    Выбор даты записи на странице создания новой записи.
    :param driver: Веб-драйвер.
    :param date: Дата записи.
    :return: Содержимое страницы после выбора.
    """
    driver = check_url(driver, LINKS['INDEX_LINK'] + LINKS['NEW_APPOINTMENT_LINK'])

    driver.find_element(By.ID, 'appointment_date').send_keys(date)

    return driver.page_source


def new_appointment_select_time(driver, time):
    """
    Выбор времени записи на странице создания новой записи.
    :param driver: Веб-драйвер.
    :param time: Время записи.
    :return: Содержимое страницы после выбора.
    """
    driver = check_url(driver, LINKS['INDEX_LINK'] + LINKS['NEW_APPOINTMENT_LINK'])

    Select(driver.find_element(By.ID, 'select_time')).select_by_visible_text(time)

    return driver.page_source


def new_appointment_select_patient(driver, patient_name):
    """
    Выбор пациента для записи на странице записи на прием.
    :param driver: Веб-драйвер.
    :param patient_name: Полное имя пациента.
    :return: Содержимое страницы после выбора.
    """
    driver = check_url(driver, LINKS['INDEX_LINK'] + LINKS['NEW_APPOINTMENT_LINK'])

    Select(driver.find_element(By.ID, 'select_patient')).select_by_visible_text(patient_name)

    return driver.page_source


def new_appointment_submit(driver):
    """
    Нажатие на кнопку "Создать запись" на странице создания новой записи.
    :param driver: Веб-драйвер.
    :return: Содержимое страницы после нажатия на кнопку "Создать запись".
    """
    driver = check_url(driver, LINKS['INDEX_LINK'] + LINKS['NEW_APPOINTMENT_LINK'])

    driver.find_element(By.ID, 'submit').submit()
    return driver.page_source


def cancel_appointment(driver, date, full_name):
    """
    Отмена записи по ее дате и имени пациента.
    :param driver: Веб-драйвер.
    :param date: Дата записи.
    :param full_name: Имя пациента.
    :return: Содержимое страницы после отмены записи.
    """
    driver = check_url(driver, LINKS['INDEX_LINK'] + LINKS['EXISTING_APPOINTMENTS_LINK'])

    rows = driver.find_elements(By.XPATH, '//table/tbody/tr')

    for row in rows:
        name_cell = row.find_element(By.XPATH, './td[3]')
        name_text = name_cell.text

        date_cell = row.find_element(By.XPATH, './td[2]')
        date_text = date_cell.text

        if name_text == full_name and date.count(date_text) != 0:
            button = row.find_element(By.XPATH, './td[last()]/form/input')
            button.submit()
            break

    return driver.page_source


def new_bill(driver, patient_name, appointment_date, service_name):
    """
    Создание нового счета на оплату.
    :param driver: Веб-драйвер.
    :param patient_name: Имя пациента.
    :param appointment_date: Дата записи.
    :param service_name: Наименование услуги.
    :return: Содержимое страницы после создания счета.
    """
    driver = check_url(driver, LINKS['INDEX_LINK'] + LINKS['BILLS_LINK'])

    select = Select(driver.find_element(By.ID, 'select_appointments'))

    for option in select.options:
        if patient_name in option.text and appointment_date in option.text and service_name in option.text:
            option.click()
            break

    driver.find_element(By.ID, 'submit').submit()

    return driver.page_source


def new_medical_history(driver, patient_name, diagnosis):
    """
    Создание новой записи медицинской истории.
    :param driver: Веб-драйвер.
    :param patient_name: Имя пациента.
    :param diagnosis: Запись истории.
    :return: Содержимое страницы после создания записи.
    """
    driver = check_url(driver, LINKS['INDEX_LINK'] + LINKS['MEDICAL_HISTORY_LINK'])

    Select(driver.find_element(By.ID, 'select_patient')).select_by_visible_text(patient_name)
    driver.find_element(By.ID, 'history_text').send_keys(diagnosis)
    driver.find_element(By.ID, 'submit').submit()

    return driver.page_source


def new_cost_accounting_entry(driver, material_name, amount):
    """
    Создание новой записи учета расходных материалов.
    :param driver: Веб-драйвер.
    :param material_name: Наименование расходного материала.
    :param amount: Количество.
    :return: Содержимое страницы создания записи учета до создания записи, содержимое страницы после создания записи,
    содержимое страницы счетов.
    """
    driver = check_url(driver, LINKS['INDEX_LINK'] + LINKS['COST_ACCOUNTING_LINK'])

    before_test = driver.page_source

    Select(driver.find_element(By.ID, 'select_material')).select_by_visible_text(material_name)
    driver.find_element(By.ID, 'amount').send_keys(amount)

    driver.find_element(By.ID, 'submit').submit()
    after_test = driver.page_source

    driver.get(LINKS['INDEX_LINK'] + LINKS['ORDERS_LINK'])
    orders = driver.page_source

    return {'before_test': before_test, 'after_test': after_test, 'orders': orders}


def count_material(html_text, material_name):
    """
    Возвращает количество указанного материала для страницы учета расходов.
    :param html_text: Текст html документа.
    :param material_name: Название материала.
    :return: Количество материала.
    """
    parser = BeautifulSoup(html_text, 'html.parser')

    for row in parser.find_all('tr')[1:]:
        current_row = []
        for col in row.find_all('td'):
            current_row.append(col.text)
        if current_row[1].count(material_name) != 0:
            return int(current_row[2])

    return 0


def find_order(html_text, author, date_order, material_name, count):
    """
    Поиск записи счета по автору счета, дате, материалу и количеству материала на странице счетов.
    :param html_text: Текст html документа.
    :param author: Автор счета.
    :param date_order: Дата счета.
    :param material_name: Название материала.
    :param count: Количество материала.
    :return: Была ли найдена запись.
    """
    parser = BeautifulSoup(html_text, 'html.parser')

    for row in parser.find_all('tr')[1:]:
        current_row = []
        for col in row.find_all('td'):
            current_row.append(col.text)
        if current_row[1].count(author) != 0 and current_row[2].count(material_name) != 0 \
                and current_row[3].count(str(count)) != 0 \
                and abs(datetime.strptime(current_row[4].strip(), DATE_TIME_FORMAT) - date_order) \
                <= timedelta(minutes=TIME_DELTA_DIFF):
            return True

    return False


def find_medical_history(html_text, author, patient, diagnosis, date_history):
    """
    Поиск записи медицинской истории по автору записи, пациенту, тексту диагноза, дате создания записи.
    :param html_text: Текст html документа.
    :param author: Автор записи.
    :param patient: Полное имя пациента.
    :param diagnosis: Текст записи медицинской истории.
    :param date_history: Дата создания записи.
    :return: Была ли найдена запись.
    """
    parser = BeautifulSoup(html_text, 'html.parser')

    for row in parser.find_all('tr')[1:]:
        current_row = []
        for col in row.find_all('td'):
            current_row.append(col.text)
        if current_row[0].count(author) != 0 and current_row[1].count(patient) != 0 \
                and current_row[3].count(diagnosis) != 0 \
                and abs(datetime.strptime(current_row[2].strip(), DATE_TIME_FORMAT) - date_history) \
                <= timedelta(minutes=TIME_DELTA_DIFF):
            return True

    return False

