def test_put_v1_account_password(account_helper, prepare_user, prepare_password):
    # Регистрация пользователя
    login = prepare_user.login
    password = prepare_user.password
    email = prepare_user.email
    old_password = password
    new_password = prepare_password.password
    account_helper.register_new_user(login=login, password=password, email=email)
    # Вызов метода для сброса пароля
    account_helper.post_password(login=login, password=password, email=email)
    # Вызов метода для смены пароля
    response = account_helper.change_password(login=login, old_password=old_password, new_password=new_password)
    print(response)
    # Повторная авторизация с новым паролем для проверки
    account_helper.user_login(login=login, password=new_password)