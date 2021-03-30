# py-money

Money class for Python 3 that enforces that all monetary amounts are represented with the correct number of decimal places for the currency, and is immutable when it comes to mathematical operations.

Forked from [vimeo/pymoney](https://github.com/vimeo/py-money), adapted for use by AlphaLayer.

## Installation

Install the latest release with either:

```bash
pip install git+https://622eb2d8292b2d17e2e1dd90dbc77a6ba0836f13@github.com/alpha-layer/py-money
```
or
```bash
poetry add git+https://622eb2d8292b2d17e2e1dd90dbc77a6ba0836f13@github.com/alpha-layer/py-money
```

## Usage

A Money object can be created with an amount (as int, float, string, or Decimal) and a currency from the Currency class:

```python
>>> from money.money import Money
>>> from money.currency import Currency
>>> m = Money(9.95, Currency.USD)
>>> m
USD $9.95
>>> m = Money(1, Currency.CAD)
>>> m
CAD $1.00
>>> m = Money("10.99", Currency.GBP)
>>> m
GBP £10.99
```

If no Currency is provided, the default is USD:

```python
>>> m = Money(10.99)
>>> m
USD $10.99
```

> :eight_spoked_asterisk: **NOTE:** Money will throw an error if you try to construct it with an invalid amount (precision) for the currency:
> ```python
> >>> m = Money(3.678)
> money.exceptions.InvalidAmountError: '3.678' is an invalid amount for currency Currency.USD
> >>> m = Money(5.5, Currency.JPY)
> money.exceptions.InvalidAmountError: '5.5' is an invalid amount for currency Currency.JPY
> ```
> You can override this behaviour and round by default with the `round` flag:
> ```python
> >>> m = Money(5.5, Currency.JPY, round=True)
> >>> m
> JPY ¥6
> ```

> :warning: **WARNING**: Passing in a Decimal created with a float argument has unknown precision which is probably not what you want:
> ```python
> >>> m = Money(Decimal(3.95))
> money.exceptions.InvalidAmountError: '3.95000000000000017763568394002504646778106689453125' is an invalid amount for currency Currency.USD
> ```
> Use a string argument when creating the Decimal, pass the float to Money directly instead, or use the `round` flag:
> ```python
> >>> m = Money(Decimal("3.95"))
> >>> m
> USD $3.95
> >>> m = Money(3.95)
> >>> m
> USD $3.95
> >>> m = Money(Decimal(3.95), round=True)
> >>> m
> USD $3.95
> ```

Money objects can also be created from and converted to sub units:

```python
>>> m = Money.from_sub_units(499, Currency.USD)
>>> m
USD $4.99
>>> m.sub_units
499
```

## Mathematical Operations
Money is immutable and supports most mathematical and logical operators:

```python
>>> m = Money(10.00, Currency.USD)
>>> m / 2
USD $5.00
>>> m + Money(3.00, Currency.USD)
USD $8.00
>>> m > Money(5.55, Currency.USD)
True
```

Money will automatically round to the correct number of decimal places for the currency:

```python
>>> m = Money(9.95, Currency.EUR)
>>> m * 0.15
EUR €9.95
>>> m = Money(10, Currency.JPY)
>>> m / 3
JPY ¥3
```

> :eight_spoked_asterisk: **NOTE:** Mathetmatical and logical operations between two money objects are only allowed if both objects are of the same currency. Otherwise, an error will be thrown. Money does not support conversion between currencies.

> :warning: **WARNING:** Rounding is performed after each multiplication or division operation. While this is exactly what you want when computing something like a sales tax, it may cause confusion if you're not expecting it.
> ```python
> >>> m = Money(9.95, Currency.USD)
> >>> m * 0.5 * 2
> USD $9.96
> >>> m * (0.5 * 2)
> USD $9.95
> ```
> To avoid confusion, be sure to simplify your expressions.

For more examples, check out the tests file.

## Formatting

Money can be formatted for different locales (defaults to `"en_US"`):

```python
>>> Money(3.24, Currency.USD).format("en_US")
'$3.24'
>>> Money(9.95, Currency.EUR).format("en_UK")
'€5.56'
>>> Money(94, Currency.JPY).format()
'￥94'
```

## Is this the money library for me?

If you're just trying to do simple mathematical operations on money in different currencies, and correct rounding is important, this library is probably perfect for you:

```python
>>> subtotal = Money(9.95, Currency.USD)
>>> tax = subtotal * 0.07
>>> total = tax + subtotal
>>> subtotal.format()
'$9.95'
>>> tax.format()
'$0.70'
>>> total.format()
'$10.65'
```

If you're doing complicated money operations that require many digits of precision for some reason, this library is not for you.

## Future improvements

- Additional options for `.format()`
- Improved mathematical operations with various numeric types
- Settable default currency
- Settable default rounding behaviour (on constructor)

## Contributing

Pull requests are welcome! Please include tests. You can install everything needed for development with:

```bash
pip install poetry
poetry install
pre-commit install
```

## Acknowledgements

Forked from [vimeo/pymoney](https://github.com/vimeo/py-money). Much of the code is borrowed from [carlospalol/pymoney](https://github.com/carlospalol/money). Much of the logic for handling foreign currencies is taken from [sebastianbergmann/money](https://github.com/sebastianbergmann/money). Money formatting is powered by [Babel](http://babel.pocoo.org/).
