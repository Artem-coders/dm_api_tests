from json import loads
from dm_api_account.apis.account_api import AccountApi
from dm_api_account.apis.login_api import LoginApi
from api_mailhog.apis.mailhog_api import MailhogApi
from restclient.configuration import Configuration as MailhogConfiguration
from restclient.configuration import Configuration as DmApiConfiguration
import structlog


structlog.configure(
    processors=[
        structlog.processors.JSONRenderer(indent=4,
                                          ensure_ascii=True,
                                          # sort_keys=True
                                          )
    ]
)

def test_post_v1_account():
    # Регистрация пользователя
    mailhog_configuration = MailhogConfiguration(host='http://5.63.153.31:5025')
    dm_api_configuration = DmApiConfiguration(host='http://5.63.153.31:5051', disable_log=False)

    account_api = AccountApi(configuration=dm_api_configuration)
    login_api = LoginApi(configuration=dm_api_configuration)
    mailhog_api = MailhogApi(configuration=mailhog_configuration)

    login = 'GOOD_4'
    password = '123456789'
    email = f'{login}@mail.ru'

    # Регистрация пользователя
    response = account_api.post_v1_account(
        json={
            'login': login,
            'email': email,
            'password': password,
        }
    )
    assert response.status_code == 201, f'Пользователь не был создан {response.json()}'

    # Получить письма из почтового сервера
    response = mailhog_api.get_api_v2_messages()
    assert response.status_code == 200, 'Письма не были получены'

    # Получить активационный токен
    token = get_activation_token_by_login(login, response)
    assert token is not None, f"Токен для пользователя {login} не был получен"

    # Активация пользователя
    response = account_api.put_v1_account_token(
        token=token,
        headers={
            'accept': 'text/plain',
        }
    )
    assert response.status_code == 200, 'Пользователь не был активирован'

    # Авторизоваться
    response = login_api.post_v1_account_login(
        json={
            'login': login,
            'password': password,
            'rememberMe': True,
        }
    )
    assert response.status_code == 200, 'Пользователь не смог авторизоваться'

def get_activation_token_by_login(login, response):
    token = None
    for item in response.json()['items']:
        body = item['Content']['Body']

        # Пытаемся распарсить тело как JSON, но если не получится — ищем вручную
        try:
            user_data = loads(body)
            user_login = user_data.get('Login')
            if user_login == login:
                token = user_data['ConfirmationLinkUrl'].split('/')[-1]
                break
        except ValueError:
            # Письмо не в формате JSON — ищем ссылку вручную
            for line in body.splitlines():
                if 'ConfirmationLinkUrl' in line:
                    token = line.split('/')[-1].strip()
                    break

    if not token:
        raise ValueError(f'❌ Не удалось найти токен активации для пользователя {login}')

    return token

# def get_activation_token_by_login(login, response):
#     token = None
#     for item in response.json()['items']:
#         user_data = loads(item['Content']['Body'])
#         user_login = user_data['Login']
#         if user_login == login:
#             token = user_data['ConfirmationLinkUrl'].split('/')[-1]
#     return token