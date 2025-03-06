import requests


def test_post_v1_account():
    # Регистрация пользователя

    login = 'Pakhomov'
    password = '123456789'
    email = f'{login}@mail.ru'
    json_data = {
        'login': login,
        'email': email,
        'password': password,
    }

    response = requests.post('http://5.63.153.31:5051/v1/account', json=json_data)
    print(response.status_code)
    print(response.text)
    # Получить письма из почтового сервера

    params = {
        'limit': '50',
    }

    response = requests.get('http://5.63.153.31:5025/api/v2/messages', params=params, verify=False)
    print(response.status_code)
    print(response.text)
    # Получить активационный токен

    # Активация пользователя
    headers = {
        'accept': 'text/plain',
    }

    response = requests.put('http://5.63.153.31:5051/v1/account/44f1f333-270b-4b41-8f53-cf28a4d5b639', headers=headers)
    print(response.status_code)
    print(response.text)
    # Авторизоваться

    json_data = {
        'login': login,
        'password': password,
        'rememberMe': True,
    }

    response = requests.post('http://5.63.153.31:5051/v1/account/login', json=json_data)
    print(response.status_code)
    print(response.text)
