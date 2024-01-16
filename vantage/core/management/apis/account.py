from typing import Optional
from pydantic import StrictStr  # type: ignore

from vantage.core.base import BaseAPI
from vantage.core.http.api.account_management_api import AccountManagementApi
from vantage.core.http.models import (
    Account,
    AccountModifiable,
    User,
    UserModifiable,
    UserRegistrationFields,
)

import os

__all__ = ["AccountAPI"]


class AccountAPI(BaseAPI):
    def __init__(self, api_key: str, host: str | None):
        super().__init__(api_key, host)
        self.api = AccountManagementApi()

    def account_info(self, account_id: StrictStr) -> Account:
        # TODO: docstring
        return self.api.get_account(account_id)

    def update_account_info(
        self, account_id: StrictStr, account_modifiable: AccountModifiable
    ) -> Account:
        # TODO: docstring
        return self.api.update_account(account_id, account_modifiable)

    def logged_in_user(self) -> User:
        # TODO: docstring
        return self.api.user_me(
            _headers={"authorization": f"Bearer {os.environ['VANTAGE_TOKEN']}"}
        )

    def user_info(self, user_id: StrictStr) -> User:
        # TODO: docstring
        return self.api.get_user(user_id)

    def update_user_info(
        self, user_id: StrictStr, user_modifiable: UserModifiable
    ) -> User:
        # TODO: docstring
        return self.api.update_user(user_id, user_modifiable)

    def register_user(
        self, user_registration_fields: UserRegistrationFields
    ) -> User:
        # TODO: docstring
        return self.api.register_user(user_registration_fields)
