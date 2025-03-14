from api_class_client.class_client import ApiClient

# Выполняем авторизацию
def test_login_user():
    account_api = ApiClient(host='http://5.63.153.31:5051')
    login = 'Siberaia1'
    password = '123456789'

    json_data = {
        'login': login,
        'password': password,
        'rememberMe': True,
    }

    response = account_api.post_v1_account_login(json_data=json_data)
    assert response.status_code == 200, 'Пользователь не смог авторизоваться'