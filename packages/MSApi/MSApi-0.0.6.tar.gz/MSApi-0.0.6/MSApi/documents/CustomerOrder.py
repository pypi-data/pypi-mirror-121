from typing import Optional

from MSApi.ObjectMS import ObjectMS, check_init
from MSApi.MSLowApi import MSLowApi, error_handler
from MSApi.State import State
from MSApi.Organization import Account


class CustomerOrder(ObjectMS):

    @classmethod
    def gen_states(cls):
        response = MSLowApi.auch_get(f"entity/customerorder/metadata")
        error_handler(response)
        for states_json in response.json()["states"]:
            yield State(states_json)

    def __init__(self, json):
        super().__init__(json)

    @check_init
    def get_id(self) -> str:
        return self._json.get('id')

    @check_init
    def get_account_id(self) -> str:
        return self._json.get('accountId')

    @check_init
    def get_name(self) -> str:
        return self._json.get('name')

    @check_init
    def get_description(self) -> Optional[str]:
        return self._json.get('description')

    def get_state(self) -> Optional[State]:
        result = self._json.get('state')
        if result is not None:
            return State(result)
        return None

    def get_organization_account(self) -> Optional[Account]:
        result = self._json.get('organizationAccount')
        if result is not None:
            return Account(result)
        return None
