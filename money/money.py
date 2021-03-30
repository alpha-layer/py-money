from __future__ import annotations

from decimal import ROUND_HALF_UP, Decimal
from typing import Union

from babel.numbers import format_currency, get_currency_symbol

from money.currency import Currency, CurrencyHelper
from money.exceptions import (
    CurrencyMismatchError,
    InvalidAmountError,
    InvalidOperandError,
)


class Money:
    """Class representing a monetary amount"""

    def __init__(
        self,
        amount: Union[str, int, Decimal, float],
        currency: Currency = Currency.USD,
        round: bool = False,
    ) -> None:
        if not isinstance(amount, Decimal):
            amount = Decimal(str(amount))

        rounded_amount = self._round(amount, currency)

        self._currency = currency

        if round:
            self._amount = rounded_amount
        else:
            if rounded_amount != amount:
                raise InvalidAmountError(amount, currency)

            self._amount = amount

    @property
    def amount(self) -> Decimal:
        """Returns the numeric amount"""

        return self._amount

    @property
    def currency(self) -> Currency:
        """Returns the currency"""

        return self._currency

    @classmethod
    def from_sub_units(cls, sub_units: int, currency: Currency = Currency.USD) -> Money:
        """Creates a Money instance from sub-units."""
        sub_units_per_unit = CurrencyHelper.sub_unit_for_currency(currency)
        return cls(Decimal(sub_units) / Decimal(sub_units_per_unit), currency)

    @property
    def sub_units(self) -> int:
        """Converts the amount to sub-units"""
        sub_units_per_unit = CurrencyHelper.sub_unit_for_currency(self.currency)
        return int(self.amount * sub_units_per_unit)

    def __hash__(self) -> int:
        return hash((self._amount, self._currency))

    def __repr__(self) -> str:
        # If currency symbol is the same as the name, omit the name.
        if get_currency_symbol(self._currency.name, "en_US") == self._currency.name:
            return self.format()

        return f"{self._currency.name} {self.format()}"

    def __lt__(self, other: Money) -> bool:
        if not isinstance(other, Money):
            raise InvalidOperandError

        self._assert_same_currency(other)
        return self.amount < other.amount

    def __le__(self, other: Money) -> bool:
        if not isinstance(other, Money):
            raise InvalidOperandError

        self._assert_same_currency(other)
        return self.amount <= other.amount

    def __gt__(self, other: Money) -> bool:
        if not isinstance(other, Money):
            raise InvalidOperandError

        self._assert_same_currency(other)
        return self.amount > other.amount

    def __ge__(self, other: Money) -> bool:
        if not isinstance(other, Money):
            raise InvalidOperandError

        self._assert_same_currency(other)
        return self.amount >= other.amount

    def __eq__(self, other: Money) -> bool:
        if not isinstance(other, Money):
            raise InvalidOperandError

        self._assert_same_currency(other)
        return self.amount == other.amount

    def __ne__(self, other: Money) -> bool:
        return not self == other

    def __bool__(self):
        return bool(self._amount)

    def __add__(self, other: Union[float, int, Decimal, Money]) -> Money:
        if not isinstance(other, Money):
            raise InvalidOperandError

        self._assert_same_currency(other)
        return self.__class__(self.amount + other.amount, self.currency)

    def __radd__(self, other: Money) -> Money:
        return self.__add__(other)

    def __sub__(self, other: Money) -> Money:
        if not isinstance(other, Money):
            raise InvalidOperandError

        self._assert_same_currency(other)
        return self.__class__(self.amount - other.amount, self.currency)

    def __rsub__(self, other: Money) -> Money:
        return self.__sub__(other)

    def __mul__(self, other: float) -> Money:
        if isinstance(other, Money):
            raise InvalidOperandError

        amount = self._round(self._amount * Decimal(other), self._currency)
        return self.__class__(amount, self._currency)

    def __rmul__(self, other: float) -> Money:
        return self.__mul__(other)

    def __div__(self, other: float) -> Money:
        return self.__truediv__(other)  # type: ignore

    def __truediv__(self, other: Union[Money, float]) -> Union[Money, float]:
        if isinstance(other, Money):
            self._assert_same_currency(other)
            if other.amount == Decimal("0"):
                raise ZeroDivisionError
            return float(self.amount / other.amount)

        else:
            if other == 0:
                raise ZeroDivisionError
            amount = self._round(self._amount / Decimal(other), self._currency)
            return self.__class__(amount, self._currency)

    def __floordiv__(self, other: Union[Money, float]) -> Union[Money, float]:
        if isinstance(other, Money):
            self._assert_same_currency(other)
            if other.amount == Decimal("0"):
                raise ZeroDivisionError
            return float(self.amount // other.amount)

        else:
            if other == 0:
                raise ZeroDivisionError
            amount = self._round(self._amount // Decimal(other), self._currency)
            return self.__class__(amount, self._currency)

    def __mod__(self, other: Union[Money, float]) -> Union[Money, float]:
        if isinstance(other, Money):
            self._assert_same_currency(other)
            if other.amount == Decimal("0"):
                raise ZeroDivisionError
            return float(self.amount % other.amount)

        else:
            if other == 0:
                raise ZeroDivisionError
            amount = self._round(self._amount % Decimal(other), self._currency)
            return self.__class__(amount, self._currency)

    def __neg__(self) -> Money:
        return self.__class__(-self._amount, self._currency)

    def __pos__(self) -> Money:
        return self.__class__(+self._amount, self._currency)

    def __abs__(self) -> Money:
        return self.__class__(abs(self._amount), self._currency)

    def format(self, locale: str = "en_US") -> str:
        """Returns a string of the currency formatted for the specified locale"""

        return format_currency(self.amount, self.currency.name, locale=locale)

    def _assert_same_currency(self, other: Money) -> None:
        if self.currency != other.currency:
            raise CurrencyMismatchError

    @staticmethod
    def _round(amount: Decimal, currency: Currency) -> Decimal:
        sub_units = CurrencyHelper.sub_unit_for_currency(currency)
        # rstrip is necessary because quantize treats 1. differently from 1.0
        rounded_to_subunits = amount.quantize(
            Decimal(str(1 / sub_units).rstrip("0")), rounding=ROUND_HALF_UP
        )
        decimal_precision = CurrencyHelper.decimal_precision_for_currency(currency)
        return rounded_to_subunits.quantize(
            Decimal(str(1 / (10 ** decimal_precision)).rstrip("0")),
            rounding=ROUND_HALF_UP,
        )
