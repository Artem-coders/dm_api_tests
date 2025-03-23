from api_class_client.class_client import ApiClient, get_activation_token_by_login

# Получаем письмо и активируем пользователя
def test_activate_user():
    account_api = ApiClient(host='http://5.63.153.31:5051')
    mailhog_api = ApiClient(host='http://5.63.153.31:5025')
    login = 'Siberaia1'

    response = mailhog_api.get_api_v2_messages()
    assert response.status_code == 200, 'Письма не были получены'

    token = get_activation_token_by_login(login, response)
    assert token is not None, f"Токен для пользователя {login} не был получен"

    response = account_api.put_v1_account_token(token=token)
    assert response.status_code == 200, 'Пользователь не был активирован'