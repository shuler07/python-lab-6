from typing import Any, get_args


class ValidatedLiteral:

    def __init__(self, literal_type: Any, default: str) -> None:
        self._allowed = get_args(literal_type)
        self._default = default
        self._attr = ''

    def __set_name__(self, owner, name):
        self._attr = f'_{name}'

    def __get__(self, instance, owner):
        if instance is None:
            return self
        return getattr(instance, self._attr, self._default)

    def __set__(self, instance, value):
        if value not in self._allowed:
            raise ValueError(f"{instance.__class__.__name__} {self._attr.lstrip('_')} must be in {self._allowed}, got {value}")
        setattr(instance, self._attr, value)
