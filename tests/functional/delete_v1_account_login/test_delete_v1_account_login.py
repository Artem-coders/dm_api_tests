def test_delete_v1_account_login(account_helper, prepare_user):
    # Регистрация пользователя
    login = prepare_user.login
    password = prepare_user.password
    email = prepare_user.email
    account_helper.register_new_user(login=login, password=password, email=email)
    response = account_helper.user_login(login=login, password=password)
    x_dm_auth_token = response.headers.get("x-dm-auth-token")
    account_helper.delete_user(x_dm_auth_token=x_dm_auth_token)
