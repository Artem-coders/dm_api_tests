
def test_get_v1_account_auth(auth_account_helper):
    auth_account_helper.dm_account_api.account_api.get_v1_account()


def test_get_v1_account_no_auth(account_helper):
    account_helper.dm_account_api.account_api.get_v1_account()


def test_get_v1_account_auth_information_user(account_helper):
    account_helper.dm_account_api.account_api.get_v1_account(headers={"X-Dm-Auth-Token": 'IQJh+zgzF5CpXuV4YvhMOINFI9f/7tw9zC5gv171Ib/0sf4Pd6CNH1fcw6SjiuvEqSQLO+au44Vgcbcid6G+9rEZnMr6r08hBxgvmgf+X1JxtVh31GrtqegJ86SAjMBtWe70XccJ3Zg='})

