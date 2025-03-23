
from hamcrest import (
    assert_that,
    has_properties,
    starts_with,
    all_of,
    has_property,
    equal_to,
    contains_inanyorder,
)

class GetV1Account:

    @classmethod
    def check_response_value_get_v1_account(cls, response):
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