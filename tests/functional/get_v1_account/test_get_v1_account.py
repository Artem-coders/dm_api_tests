from datetime import datetime
from hamcrest import (
    assert_that,
    has_properties,
    starts_with,
    all_of,
    has_property,
    equal_to,
    contains_inanyorder,
)
from checkers.http_checkers import check_status_code_http
from assertpy import assert_that, soft_assertions
from dm_api_account.models.user_envelope import UserRole


def test_get_v1_account_auth(auth_account_helper):
        response = auth_account_helper.dm_account_api.account_api.get_v1_account(
            validate_response=True
        )
        assert_that(
            response,
            all_of(
                has_property("resource", has_property("login", starts_with("Good"))),
                has_property(
                    "resource",
                    has_properties({"roles": contains_inanyorder("Guest", "Player")}),
                ),
                has_property(
                    "resource",
                    has_property(
                        "settings",
                        has_properties(
                            {
                                "colorSchema": equal_to("Modern"),
                                "paging": has_properties(
                                    {
                                        "postsPerPage": equal_to(10),
                                        "commentsPerPage": equal_to(10),
                                        "topicsPerPage": equal_to(10),
                                        "messagesPerPage": equal_to(10),
                                        "entitiesPerPage": equal_to(10),
                                    }
                                ),
                            }
                        ),
                    ),
                ),
                has_property(
                    "resource",
                    has_properties(
                        {
                            "rating": has_properties(
                                {
                                    "enabled": equal_to(True),
                                    "quality": equal_to(0),
                                    "quantity": equal_to(0),
                                }
                            )
                        }
                    ),
                ),
            ),
        )
        with soft_assertions():
            assert_that(response.resource.login).is_equal_to("Good_15_03_2025_22_21%S")
            assert_that(response.resource.roles).contains(UserRole.GUEST, UserRole.PLAYER)



def test_get_v1_account_no_auth(account_helper):
    with check_status_code_http(401, "User must be authenticated"):
        account_helper.dm_account_api.account_api.get_v1_account(
            validate_response=False
        )
