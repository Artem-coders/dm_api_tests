import pytest

@pytest.fixture(scope='module')
def login_data():
    login = 'TestUser127'  # <-- Задаём логин
    password = '123456789'
    email = f'{login}@mail.ru'
    return {'login': login, 'password': password, 'email': email}
