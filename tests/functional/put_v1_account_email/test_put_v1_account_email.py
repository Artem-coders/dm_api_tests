from api_class_client.class_client import ApiClient

# Попытка авторизации нового пользователя без активации email
def test_change_email(prepare_user):
    account_api = ApiClient(host='http://5.63.153.31:5051')
    login = prepare_user.login
    password = prepare_user.password
    email = prepare_user.email

    # Регистрация нового пользователя без активации
    json_data = {
        'login': login,
        'email': email,
        'password': password,
    }

    response = account_api.post_v1_account(json_data=json_data)
    assert response.status_code == 201, f'Пользователь не был создан {response.json()}'

    # Попытка авторизации нового пользователя без активации
    json_data = {'login': login, 'password': password}
    response = account_api.post_v1_account_login(json_data=json_data)
    assert response.status_code == 403, 'Ожидался статус 403 Forbidden при попытке входа с email не прошедшим активацию'

