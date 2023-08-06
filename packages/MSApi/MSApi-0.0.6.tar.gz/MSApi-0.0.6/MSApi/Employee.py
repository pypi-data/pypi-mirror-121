from MSApi.ObjectMS import ObjectMS, check_init


class Employee(ObjectMS):
    def __init__(self, json):
        super().__init__(json)

    @check_init
    def get_id(self) -> str:
        return self._json.get('id')

    @check_init
    def get_account_id(self) -> str:
        return self._json.get('accountId')

    @check_init
    def get_owner(self):
        return Employee(self._json.get('owner'))

    @check_init
    def get_shared(self) -> bool:
        return self._json.get('shared')

    @check_init
    def get_name(self) -> str:
        return self._json.get('name')
