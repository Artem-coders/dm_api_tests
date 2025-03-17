def test_delete_v1_account_login(account_helper, prepare_user):
    # Регистрация пользователя
    login = prepare_user.login
    password = prepare_user.password
    email = prepare_user.email
    account_helper.register_new_user(login=login, password=password, email=email)
    # Разлогин пользователя
    account_helper.delete_user(login=login, password=password)