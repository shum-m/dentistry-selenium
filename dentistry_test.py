import datetime

import pytest
from dentistry_selenium import login, registration, new_appointment_select_service, new_appointment_select_doctors, \
    new_appointment_select_date, new_appointment_select_time, new_appointment_submit, cancel_appointment, \
    new_cost_accounting_entry, count_material, find_order, new_medical_history, find_medical_history
from selenium import webdriver
from selenium.webdriver.chrome.service import Service

# region Данные для тестирования.
NEW_PATIENT_REGISTRATION_DATA = {'surname': 'Тестов', 'name': 'Тест', 'middle_name': 'Тестович',
                                 'birthday': '01.01.1970', 'telno': '89000000001', 'email': 'test@test.com',
                                 'password': 'qwerty', 'password_again': 'qwerty'}
"""Данные для регистрации нового пациента."""

DOCTOR_DATA_LOGIN = {'full_name': 'Николаевна Анна Михайловна', 'telno': '89023456781', 'password': 'qwerty'}
"""Данные для входа лечащего врача."""

EXISTING_PATIENT_DATA_LOGIN = {'full_name': 'Тестов Тест Тестович',
                               'telno': '89127658910',
                               'password': 'qwerty'}
"""Данные для входа существующего пользователя."""

# endregion

# region Константы.
CHROME_WEB_DRIVER_PATH = r'C:\\dentistry-selenium\chromedriver-win64\chromedriver.exe'
"""Путь к веб драйверу."""

DRIVER_TIME_WAITING = 10
"""Время ожидания веб-драйвера в секундах."""

LOGOUT_TEXT = 'Выход'
"""Текст кнопки выхода."""

CANCEL_APPOINTMENT_TEXT = 'Отменить запись'
"""Текст отмены записи."""

EMPTY_FIELD_TEXT = 'Это поле обязательно для заполнения'
"""Текст сообщения незаполненных полей."""

WRONG_LOGIN_TEXT = 'Неверный логин или пароль'
"""Текст сообщения неверных данных для входа."""

WRONG_DATE_APPOINTMENT_TEXT = 'Дата записи должна быть позже сегодняшней'
"""Текст сообщения неверной даты при создании новой записи."""

WRONG_COUNT_MATERIAL_ORDER_TEXT = '0 &lt; количество &lt;= максимальное значение в таблице'
"""Текст сообщения неверного количества материалоя для создания записи учета материалов."""

SERVICE_INSPECTION = 'Осмотр'
"""Название медицинского осмотра при записи."""

SERVICE_VENEER = 'Винир'
"""Название услуги для установки винира при записи."""

DOCTORS_SERVICE_INSPECTIONS = ['Николаевна Анна Михайловна', 'Михайлов Станислав Александрович',
                               'Сергеев Сергей Андреевич', 'Иванов Николай Александрович']
"""Список врачей для медицинского осмотра."""

DOCTORS_SERVICE_VENEER = ['Михайлов Станислав Александрович']
"""Список врачей для установки винира."""

DATE_TEST_APPOINTMENT_GOOD = '01.01.2025'
"""Дата записи для корректного результата тестирования."""

TIME_TEST_APPOINTMENT_GOOD = '8:00'
"""Время записи для корректного результата тестирования."""

DATE_TEST_APPOINTMENT_BAD = '01.01.0001'
"""Дата записи для некорректного результата тестирования"""

TIME_TEST_CANCEL_APPOINTMENT = TIME_TEST_APPOINTMENT_GOOD if len(TIME_TEST_APPOINTMENT_GOOD) == 5 else \
    '0' + TIME_TEST_APPOINTMENT_GOOD
"""Время отмены записи."""

MATERIAL_TEST_NAME = 'Иглы'
"""Название материала для тестирования."""

MATERIAL_COUNT_GOOD_TEST = 1
"""Количество материала для корректного результата тестирования."""

MATERIAL_COUNT_BAD_TEST = 10 ** 10
"""Количество для тестирования для некорректного результата тестирования."""

DIAGNOSIS_MEDICAL_HISTORY = 'Тестовый диагноз.'
"""Текст диагноза медицинской истории."""

# endregion


@pytest.fixture
def setup_chrome_driver_fixture():
    """
    Установка настроек Chrome веб-драйвера.
    :return: Веб-драйвер.
    """
    driver = webdriver.Chrome(service=Service(CHROME_WEB_DRIVER_PATH))
    driver.implicitly_wait(DRIVER_TIME_WAITING)
    return driver


def test_registration_good_data(setup_chrome_driver_fixture):
    """
    Тестирование регистрации нового пользователя.
    :param setup_chrome_driver_fixture: Веб драйвер.
    :return: Результат тестирования.
    """
    registration(setup_chrome_driver_fixture,
                 NEW_PATIENT_REGISTRATION_DATA['surname'],
                 NEW_PATIENT_REGISTRATION_DATA['name'],
                 NEW_PATIENT_REGISTRATION_DATA['middle_name'],
                 NEW_PATIENT_REGISTRATION_DATA['birthday'],
                 NEW_PATIENT_REGISTRATION_DATA['telno'],
                 NEW_PATIENT_REGISTRATION_DATA['email'],
                 NEW_PATIENT_REGISTRATION_DATA['password'],
                 NEW_PATIENT_REGISTRATION_DATA['password_again'])

    assert LOGOUT_TEXT in login(setup_chrome_driver_fixture,
                                NEW_PATIENT_REGISTRATION_DATA['telno'],
                                NEW_PATIENT_REGISTRATION_DATA['password'],)


def test_login_good_data(setup_chrome_driver_fixture):
    """
    Тестирование входа существующего пользователя с хорошими данными.
    :param setup_chrome_driver_fixture: Веб-драйвер.
    :return: Результат тестирования.
    """
    assert LOGOUT_TEXT in login(setup_chrome_driver_fixture,
                                EXISTING_PATIENT_DATA_LOGIN['telno'],
                                EXISTING_PATIENT_DATA_LOGIN['password'])


def test_login_empty_data(setup_chrome_driver_fixture):
    """
    Тестирование входа с незаполненными данными.
    :param setup_chrome_driver_fixture: Веб-драйвер.
    :return: Результат тестирования.
    """
    assert login(setup_chrome_driver_fixture, '', '').count(EMPTY_FIELD_TEXT) == 2


def test_login_wrong_data(setup_chrome_driver_fixture):
    """
    Тестирования входа с неверными данными входа.
    :param setup_chrome_driver_fixture: Веб-драйвер.
    :return: Результат тестирования.
    """
    assert WRONG_LOGIN_TEXT in login(setup_chrome_driver_fixture,
                                     EXISTING_PATIENT_DATA_LOGIN['telno'],
                                     EXISTING_PATIENT_DATA_LOGIN['password'] +
                                     NEW_PATIENT_REGISTRATION_DATA['password'])


def test_new_appointment_good_data(setup_chrome_driver_fixture):
    """
    Тестирование создания новой записи на прием с корректными данными.
    :param setup_chrome_driver_fixture: Веб-драйвер.
    :return: Результат тестирования.
    """
    login(setup_chrome_driver_fixture, EXISTING_PATIENT_DATA_LOGIN['telno'], EXISTING_PATIENT_DATA_LOGIN['password'])
    new_appointment_select_service(setup_chrome_driver_fixture, SERVICE_INSPECTION)
    new_appointment_select_doctors(setup_chrome_driver_fixture, DOCTORS_SERVICE_INSPECTIONS[0])
    new_appointment_select_date(setup_chrome_driver_fixture, DATE_TEST_APPOINTMENT_GOOD)

    new_appointment_select_time(setup_chrome_driver_fixture, TIME_TEST_APPOINTMENT_GOOD)
    created_appointment = new_appointment_submit(setup_chrome_driver_fixture)

    cancel_appointment(setup_chrome_driver_fixture, DATE_TEST_APPOINTMENT_GOOD + ' ' + TIME_TEST_CANCEL_APPOINTMENT,
                       EXISTING_PATIENT_DATA_LOGIN['full_name'])

    assert SERVICE_INSPECTION in created_appointment \
           and DOCTORS_SERVICE_INSPECTIONS[0] in created_appointment \
           and DATE_TEST_APPOINTMENT_GOOD in created_appointment \
           and TIME_TEST_APPOINTMENT_GOOD in created_appointment \
           and CANCEL_APPOINTMENT_TEXT in created_appointment


def test_new_appointment_wrong_data(setup_chrome_driver_fixture):
    """
    Тестирование создания новой записи на прием с неверными данными.
    :param setup_chrome_driver_fixture: Веб-драйвер.
    :return: Результат тестирования.
    """
    login(setup_chrome_driver_fixture, EXISTING_PATIENT_DATA_LOGIN['telno'], EXISTING_PATIENT_DATA_LOGIN['password'])

    new_appointment_select_service(setup_chrome_driver_fixture, SERVICE_INSPECTION)
    new_appointment_select_doctors(setup_chrome_driver_fixture, DOCTORS_SERVICE_INSPECTIONS[0])
    new_appointment_select_date(setup_chrome_driver_fixture, DATE_TEST_APPOINTMENT_BAD)

    assert WRONG_DATE_APPOINTMENT_TEXT in new_appointment_submit(setup_chrome_driver_fixture)


def test_new_cost_accounting_good_data(setup_chrome_driver_fixture):
    """
    Тестирование создания новой записи учета расходных материалов с корректными данными.
    :param setup_chrome_driver_fixture: Веб-драйвер.
    :return: Результат тестирования.
    """
    login(setup_chrome_driver_fixture, DOCTOR_DATA_LOGIN['telno'], DOCTOR_DATA_LOGIN['password'])

    new_cost_time = datetime.datetime.now()
    sources = new_cost_accounting_entry(setup_chrome_driver_fixture, MATERIAL_TEST_NAME, MATERIAL_COUNT_GOOD_TEST)

    before_material_count = count_material(sources['before_test'], MATERIAL_TEST_NAME)
    after_test_count = count_material(sources['after_test'], MATERIAL_TEST_NAME)
    exist_order = find_order(sources['orders'], DOCTOR_DATA_LOGIN['full_name'], new_cost_time, MATERIAL_TEST_NAME,
                             MATERIAL_COUNT_GOOD_TEST)

    assert before_material_count - after_test_count == MATERIAL_COUNT_GOOD_TEST and exist_order


def test_new_cost_accounting_wrong_data(setup_chrome_driver_fixture):
    """
    Тестирование создания новой записи учета расходных материалов с некорректными данными.
    :param setup_chrome_driver_fixture: Веб-драйвер.
    :return: Результат тестирования.
    """
    login(setup_chrome_driver_fixture, DOCTOR_DATA_LOGIN['telno'], DOCTOR_DATA_LOGIN['password'])

    new_cost_time = datetime.datetime.now()
    sources = new_cost_accounting_entry(setup_chrome_driver_fixture, MATERIAL_TEST_NAME, MATERIAL_COUNT_BAD_TEST)

    before_material_count = count_material(sources['before_test'], MATERIAL_TEST_NAME)
    after_test_count = count_material(sources['after_test'], MATERIAL_TEST_NAME)
    exist_order = find_order(sources['orders'], DOCTOR_DATA_LOGIN['full_name'], new_cost_time, MATERIAL_TEST_NAME,
                             MATERIAL_COUNT_BAD_TEST)

    assert WRONG_COUNT_MATERIAL_ORDER_TEXT in sources['after_test'] and exist_order is False and \
           before_material_count == after_test_count


def test_new_medical_history_good_data(setup_chrome_driver_fixture):
    """
    Тестирование создания новой записи медицинской истории с корректными данными.
    :param setup_chrome_driver_fixture: Веб-драйвер.
    :return: Результат тестирования.
    """
    login(setup_chrome_driver_fixture, DOCTOR_DATA_LOGIN['telno'], DOCTOR_DATA_LOGIN['password'])

    now_medical_history = datetime.datetime.now()
    new_medical_history(setup_chrome_driver_fixture,
                        EXISTING_PATIENT_DATA_LOGIN['full_name'],
                        DIAGNOSIS_MEDICAL_HISTORY)

    assert find_medical_history(setup_chrome_driver_fixture.page_source,
                                DOCTOR_DATA_LOGIN['full_name'],
                                EXISTING_PATIENT_DATA_LOGIN['full_name'],
                                DIAGNOSIS_MEDICAL_HISTORY,
                                now_medical_history)


def test_new_medical_history_wrong_data(setup_chrome_driver_fixture):
    """
    Тестирование создания новой записи медицинской истории с некорректными данными.
    :param setup_chrome_driver_fixture: Веб-драйвер.
    :return: Результат тестирования.
    """
    login(setup_chrome_driver_fixture, DOCTOR_DATA_LOGIN['telno'], DOCTOR_DATA_LOGIN['password'])

    now_medical_history = datetime.datetime.now()
    new_medical_history(setup_chrome_driver_fixture,
                        EXISTING_PATIENT_DATA_LOGIN['full_name'],
                        '')

    assert find_medical_history(setup_chrome_driver_fixture.page_source,
                                DOCTOR_DATA_LOGIN['full_name'],
                                EXISTING_PATIENT_DATA_LOGIN['full_name'],
                                '',
                                now_medical_history) is False
