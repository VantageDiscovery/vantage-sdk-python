from vantage.core.http.api.account_management_api import AccountManagementApi
from vantage.core.http.models import (
    Account,
    AccountModifiable,
    User,
    UserModifiable,
    UserRegistrationFields,
)
from vantage.core.base import BaseAPI
from pydantic import StrictStr

__all__ = ["AccountAPI"]


class AccountAPI(BaseAPI):
    def account_info(self, account_id: StrictStr) -> Account:
        # TODO: docstring
        return AccountManagementApi.get_account(account_id)

    def update_account_info(
        self, account_id: StrictStr, account_modifiable: AccountModifiable
    ) -> Account:
        # TODO: docstring
        return AccountManagementApi.update_account(
            account_id, account_modifiable
        )

    def logged_in_user(self) -> User:
        # TODO: docstring
        return AccountManagementApi.user_me()

    def user_info(self, user_id: StrictStr) -> User:
        # TODO: docstring
        return AccountManagementApi.get_user(user_id)

    def update_user_info(
        self, user_id: StrictStr, user_modifiable: UserModifiable
    ) -> User:
        # TODO: docstring
        return AccountManagementApi.update_user(user_id, user_modifiable)

    def register_user(
        self, user_registration_fields: UserRegistrationFields
    ) -> User:
        # TODO: docstring
        return AccountManagementApi.register_user(user_registration_fields)
