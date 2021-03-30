# type: ignore
from decimal import Decimal

import unittest
from money.currency import Currency
from money.exceptions import (
    CurrencyMismatchError,
    InvalidAmountError,
    InvalidOperandError,
)
from money.money import Money


class TestMoney(unittest.TestCase):
    """Money tests"""

    def test_construction_from_float(self):
        money = Money(3.95)
        self.assertEqual(Decimal("3.95"), money.amount)
        self.assertEqual(Currency.USD, money.currency)

        money = Money(192.325, Currency.KWD)
        self.assertEqual(Decimal("192.325"), money.amount)
        self.assertEqual(Currency.KWD, money.currency)

        with self.assertRaises(InvalidAmountError):
            Money(3.956, Currency.USD)

        with self.assertRaises(InvalidAmountError):
            # nonfractional currency
            Money(10.2, Currency.KRW)

    def test_construction_from_int(self):
        money = Money(1, Currency.USD)
        self.assertEqual(Decimal("1"), money.amount)
        self.assertEqual(Currency.USD, money.currency)

        money = Money(199, Currency.JPY)
        self.assertEqual(Decimal("199"), money.amount)
        self.assertEqual(Currency.JPY, money.currency)

    def test_construction_from_decimal(self):
        money = Money(Decimal("3.95"))
        self.assertEqual(Decimal("3.95"), money.amount)
        self.assertEqual(Currency.USD, money.currency)

        money = Money(Decimal(1), Currency.USD)
        self.assertEqual(Decimal("1"), money.amount)
        self.assertEqual(Currency.USD, money.currency)

        money = Money(Decimal(199), Currency.JPY)
        self.assertEqual(Decimal("199"), money.amount)
        self.assertEqual(Currency.JPY, money.currency)

        money = Money(Decimal("192.325"), Currency.KWD)
        self.assertEqual(Decimal("192.325"), money.amount)
        self.assertEqual(Currency.KWD, money.currency)

        with self.assertRaises(InvalidAmountError):
            Money(Decimal("3.956"), Currency.USD)

        with self.assertRaises(InvalidAmountError):
            # nonfractional currency
            Money(Decimal("10.2"), Currency.KRW)

    def test_constrction_from_string(self):
        money = Money("3.95")
        self.assertEqual(Decimal("3.95"), money.amount)
        self.assertEqual(Currency.USD, money.currency)

        money = Money("1", Currency.USD)
        self.assertEqual(Decimal("1"), money.amount)
        self.assertEqual(Currency.USD, money.currency)

        money = Money("199", Currency.JPY)
        self.assertEqual(Decimal("199"), money.amount)
        self.assertEqual(Currency.JPY, money.currency)

        money = Money("192.325", Currency.KWD)
        self.assertEqual(Decimal("192.325"), money.amount)
        self.assertEqual(Currency.KWD, money.currency)

        with self.assertRaises(InvalidAmountError):
            Money("3.956", Currency.USD)

        with self.assertRaises(InvalidAmountError):
            # nonfractional currency
            Money("10.2", Currency.KRW)

    def test_constrction_with_round_flag(self):
        money = Money("3.956", round=True)
        self.assertEqual(Decimal("3.96"), money.amount)
        self.assertEqual(Currency.USD, money.currency)

        # nonfractional currencies
        money = Money("10.2", Currency.KRW, round=True)
        self.assertEqual(Decimal("10"), money.amount)
        self.assertEqual(Currency.KRW, money.currency)

        money = Money("5.5", Currency.JPY, round=True)
        self.assertEqual(Decimal("6"), money.amount)
        self.assertEqual(Currency.JPY, money.currency)

    def test_from_sub_units(self):
        money = Money.from_sub_units(101, Currency.USD)
        self.assertEqual(Money(1.01, Currency.USD), money)

        money = Money.from_sub_units(5, Currency.JPY)
        self.assertEqual(Money(5, Currency.JPY), money)

    def test_sub_units(self):
        money = Money(1.01, Currency.USD)
        self.assertEqual(101, money.sub_units)

    def test_hash(self):
        self.assertEqual(hash(Money(1.2, Currency.USD)), hash(Money(1.2)))
        self.assertNotEqual(hash(Money(9.3)), hash(Money(1.5)))
        self.assertNotEqual(
            hash(Money(99.3, Currency.USD)), hash(Money(99.3, Currency.CHF))
        )

    def test_tostring(self):
        self.assertEqual("USD 1.20", str(Money(1.2)))
        self.assertEqual("CHF 3.60", str(Money(3.6, Currency.CHF)))
        self.assertEqual("JPY 88", str(Money(88, Currency.JPY)))
        self.assertEqual("CAD 1.00", str(Money(1, Currency.CAD)))
        self.assertEqual("KWD 192.325", str(Money(192.325, Currency.KWD)))

    def test_less_than(self):
        self.assertLess(Money(1.2), Money(3.5))
        self.assertFalse(Money(104.2) < Money(5.13))
        self.assertFalse(Money(2.2) < Money(2.2))

        with self.assertRaises(CurrencyMismatchError):
            Money(1.2, Currency.GBP) < Money(3.5, Currency.EUR)

        with self.assertRaises(InvalidOperandError):
            1.2 < Money(3.5)

    def test_less_than_or_equal(self):
        self.assertLessEqual(Money(1.2), Money(3.5))
        self.assertFalse(Money(104.2) <= Money(5.13))
        self.assertLessEqual(Money(2.2), Money(2.2))

        with self.assertRaises(CurrencyMismatchError):
            Money(1.2, Currency.GBP) <= Money(3.5, Currency.EUR)

        with self.assertRaises(InvalidOperandError):
            1.2 <= Money(3.5)

    def test_greater_than(self):
        self.assertGreater(Money(3.5), Money(1.2))
        self.assertFalse(Money(5.13) > Money(104.2))
        self.assertFalse(Money(2.2) > Money(2.2))

        with self.assertRaises(CurrencyMismatchError):
            Money(3.5, Currency.EUR) > Money(1.2, Currency.GBP)

        with self.assertRaises(InvalidOperandError):
            Money(3.5) > 1.2

    def test_greater_than_or_equal(self):
        self.assertGreaterEqual(Money(3.5), Money(1.2))
        self.assertFalse(Money(5.13) >= Money(104.2))
        self.assertGreaterEqual(Money(2.2), Money(2.2))

        with self.assertRaises(CurrencyMismatchError):
            Money(3.5, Currency.EUR) >= Money(1.2, Currency.GBP)

        with self.assertRaises(InvalidOperandError):
            Money(3.5) >= 1.2

    def test_equal(self):
        self.assertEqual(Money(3.5), Money(3.5))
        self.assertEqual(Money(4.0, Currency.GBP), Money(4.0, Currency.GBP))

        with self.assertRaises(CurrencyMismatchError):
            Money(3.5, Currency.EUR) == Money(3.5, Currency.GBP)

        with self.assertRaises(InvalidOperandError):
            Money(5.5) == 5.5

    def test_not_equal(self):
        self.assertNotEqual(Money(46.44), Money(3.5))
        self.assertNotEqual(Money(12.01, Currency.GBP), Money(4.0, Currency.GBP))

        with self.assertRaises(CurrencyMismatchError):
            Money(3.5, Currency.EUR) != Money(23, Currency.GBP)

        with self.assertRaises(InvalidOperandError):
            Money(5.5) != 666.32

    def test_bool(self):
        self.assertEqual(True, bool(Money(3.62)))
        self.assertEqual(False, bool(Money(0.00)))

    def test_add(self):
        self.assertEqual(Money(4.75), Money(3.5) + Money(1.25))

        with self.assertRaises(CurrencyMismatchError):
            Money(3.5, Currency.EUR) + Money(23, Currency.GBP)

        with self.assertRaises(InvalidOperandError):
            Money(5.5) + 666.32

        with self.assertRaises(InvalidOperandError):
            666.32 + Money(5.5)

    def test_subtract(self):
        self.assertEqual(Money(2.25), Money(3.5) - Money(1.25))
        self.assertEqual(Money(-1.5), Money(4) - Money(5.5))

        with self.assertRaises(CurrencyMismatchError):
            Money(3.5, Currency.EUR) - Money(1.8, Currency.GBP)

        with self.assertRaises(InvalidOperandError):
            Money(5.5) - 6.32

        with self.assertRaises(InvalidOperandError):
            666.32 - Money(5.5)

    def test_multiply(self):
        self.assertEqual(Money(9.6), Money(3.2) * 3)
        self.assertEqual(Money(9.6, Currency.EUR), 3 * Money(3.2, Currency.EUR))
        self.assertEqual(Money(1.49), Money(9.95) * 0.15)
        self.assertEqual(Money(1, Currency.JPY), Money(3, Currency.JPY) * 0.2)
        self.assertEqual(Money(5, Currency.KRW), Money(3, Currency.KRW) * 1.5)

        # since GNF has different subunits than JPY, the results are different even though
        # they have the same final decimal precision. hopefully this behavior is correct...
        self.assertEqual(Money(4, Currency.JPY), Money(3, Currency.JPY) * 1.4995)
        self.assertEqual(Money(5, Currency.GNF), Money(3, Currency.GNF) * 1.4995)

        with self.assertRaises(InvalidOperandError):
            Money(5.5) * Money(1.2)

    def test_divide(self):
        self.assertEqual(Money(1.1), Money(3.3) / 3)
        self.assertEqual(Money(41.46), Money(9.95) / 0.24)
        self.assertEqual(Money(2, Currency.JPY), Money(3, Currency.JPY) / 1.6)
        self.assertEqual(1.44, Money(3.6) / Money(2.5))

        with self.assertRaises(TypeError):
            3 / Money(5.5)

        with self.assertRaises(ZeroDivisionError):
            Money(3) / 0

        with self.assertRaises(ZeroDivisionError):
            Money(3.3) / 0.0

        with self.assertRaises(ZeroDivisionError):
            Money(3.3) / Money(0)

        with self.assertRaises(CurrencyMismatchError):
            Money(3.5, Currency.EUR) / Money(1.8, Currency.GBP)

    def test_floor_divide(self):
        self.assertEqual(Money(1), Money(3.3) // 3)
        self.assertEqual(Money(41), Money(9.95) // 0.24)
        self.assertEqual(Money(1, Currency.JPY), Money(3, Currency.JPY) // 1.6)
        self.assertEqual(1, Money(3.6) // Money(2.5))

        with self.assertRaises(TypeError):
            3 // Money(5.5)

        with self.assertRaises(ZeroDivisionError):
            Money(3) // 0

        with self.assertRaises(ZeroDivisionError):
            Money(3.3) // 0.0

        with self.assertRaises(ZeroDivisionError):
            Money(3.3) // Money(0)

        with self.assertRaises(CurrencyMismatchError):
            Money(3.5, Currency.EUR) // Money(1.8, Currency.GBP)

    def test_mod(self):
        self.assertEqual(Money(0.3), Money(3.3) % 3)
        self.assertEqual(Money(1, Currency.JPY), Money(3, Currency.JPY) % 2)
        self.assertEqual(1, Money(3) % Money(2))

        with self.assertRaises(TypeError):
            3 % Money(5.5)

        with self.assertRaises(ZeroDivisionError):
            Money(3.3) % 0

        with self.assertRaises(ZeroDivisionError):
            Money(3.3) % 0.0

        with self.assertRaises(CurrencyMismatchError):
            Money(3.5, Currency.EUR) % Money(1.8, Currency.GBP)

    def test_neg(self):
        self.assertEqual(Money(-5.23), -Money(5.23))
        self.assertEqual(Money(1.35), -Money(-1.35))

    def test_pos(self):
        self.assertEqual(Money(5.23), +Money(5.23))
        self.assertEqual(Money(-1.35), +Money(-1.35))

    def test_abs(self):
        self.assertEqual(Money(5.23), abs(Money(5.23)))
        self.assertEqual(Money(1.35), abs(Money(-1.35)))

    def test_format_default(self):
        self.assertEqual("$3.24", Money(3.24).format())
        self.assertEqual("¥10", Money(10, Currency.JPY).format())
        self.assertEqual("KWD192.325", Money(192.325, Currency.KWD).format())

    def test_format_locale(self):
        self.assertEqual("5,56 €", Money(5.56, Currency.EUR).format("fr_FR"))
        self.assertEqual("￥94", Money(94, Currency.JPY).format("ja_JP"))
        self.assertEqual("د.ك.‏ 192.325", Money(192.325, Currency.KWD).format("ar_KW"))

    def test_format_name(self):
        self.assertEqual("3.24 US dollars", Money(3.24).format(format_type="name"))
        self.assertEqual(
            "10 Japanese yen", Money(10, Currency.JPY).format(format_type="name")
        )
        self.assertEqual(
            "192.325 Kuwaiti dinars",
            Money(192.325, Currency.KWD).format(format_type="name"),
        )

    def test_format_locale_and_name(self):
        self.assertEqual(
            "5,56 euros", Money(5.56, Currency.EUR).format("fr_FR", format_type="name")
        )
        self.assertEqual(
            "94円", Money(94, Currency.JPY).format("ja_JP", format_type="name")
        )
        self.assertEqual(
            "192.325 دينار كويتي",
            Money(192.325, Currency.KWD).format("ar_KW", format_type="name"),
        )

    def test_format_currency_code(self):
        self.assertEqual("USD 3.24", Money(3.24).format(format="¤¤ "))
        self.assertEqual(
            "JPY 94", Money(94, Currency.JPY).format("ja_JP", format="¤¤ ")
        )
        self.assertEqual(
            "KWD 192.325", Money(192.325, Currency.KWD).format("ar_KW", format="¤¤ ")
        )

    def test_format_currency_symbol(self):
        self.assertEqual("$3.24", Money(3.24).format(format="¤"))
        self.assertEqual("€5,56", Money(5.56, Currency.EUR).format("fr_FR", format="¤"))
        self.assertEqual("¥10", Money(10, Currency.JPY).format(format="¤"))
        self.assertEqual("￥94", Money(94, Currency.JPY).format("ja_JP", format="¤"))
        self.assertEqual("KWD192.325", Money(192.325, Currency.KWD).format(format="¤"))
        self.assertEqual(
            "د.ك.‏192.325", Money(192.325, Currency.KWD).format("ar_KW", format="¤")
        )

    def test_format_custom(self):
        self.assertEqual("$3.24 USD", Money(3.24).format(format="¤#,##0.00 ¤¤"))
        self.assertEqual(
            "€5,56 EUR",
            Money(5.56, Currency.EUR).format("fr_FR", format="¤#,##0.00 ¤¤"),
        )
        self.assertEqual(
            "¥10 JPY Japanese yen",
            Money(10, Currency.JPY).format(format="¤#,##0.00 ¤¤", format_type="name"),
        )
        self.assertEqual(
            "94￥ JPY円",
            Money(94, Currency.JPY).format(
                "ja_JP", format="#,##0.00¤ ¤¤", format_type="name"
            ),
        )
        self.assertEqual(
            "KWD192.325 KWD", Money(192.325, Currency.KWD).format(format="¤#,##0.00 ¤¤")
        )
        self.assertEqual(
            "د.ك.‏192.325 KWD",
            Money(192.325, Currency.KWD).format("ar_KW", format="¤#,##0.00 ¤¤"),
        )
