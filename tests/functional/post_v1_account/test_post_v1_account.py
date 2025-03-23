from checkers.http_checkers import check_negative_login_http, check_negative_password_http, check_negative_email_http, check_negative_login_password_email_http
from checkers.post_v1_account import PostV1Account


def test_post_v1_account(account_helper, prepare_user):
    login = prepare_user.login
    password = prepare_user.password
    email = prepare_user.email
    account_helper.register_new_user(login=login, password=password, email=email)
    response = account_helper.user_login(
        login=login, password=password, validate_response=True
    )
    PostV1Account.check_reasponse_values(response)





def test_post_v1_account_negative_check_login(account_helper):
    with check_negative_login_http(400, "Validation failed", "Short"):
        login = 'B'
        password = '123456789'
        email = "Good@mail.ru"
        account_helper.register_new_user(login=login, password=password, email=email)

def test_post_v1_account_negative_check_password(account_helper):
    with check_negative_password_http(400, "Validation failed", "Short"):
        login = 'Bad1234567810'
        password = '12345'
        email = "Bad1234567810@mail.ru"
        account_helper.register_new_user(login=login, password=password, email=email)

def test_post_v1_account_negative_check_email(account_helper):
    with check_negative_email_http(400, "Validation failed", "Invalid"):
        login = 'Bad987654'
        password = '123456789'
        email = "Bad987654mail.ru"
        account_helper.register_new_user(login=login, password=password, email=email)


def test_post_v1_account_negative_check_login_password_email(account_helper):
    with check_negative_login_password_email_http(400, "Validation failed", "Short", "Short", "Invalid"):
        login = 'B'
        password = '12345'
        email = "Bsdskmail.ru"
        account_helper.register_new_user(login=login, password=password, email=email)