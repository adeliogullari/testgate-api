from typing import Any


class FieldValidation:

    def __init__(self):
        pass

    @staticmethod
    def is_field_exist(field: Any, error: Any):
        if not field:
            raise error
        return field
