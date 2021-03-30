"""Custom exceptions for money operations"""


class InvalidAmountError(ValueError):
    def __init__(self, amount, currency):
        super().__init__(f"'{amount}' is an invalid amount for currency {currency}")


class CurrencyMismatchError(ValueError):
    def __init__(self):
        super().__init__("Currencies must match")


class InvalidOperandError(ValueError):
    def __init__(self):
        super().__init__("Invalid operand types for operation")
