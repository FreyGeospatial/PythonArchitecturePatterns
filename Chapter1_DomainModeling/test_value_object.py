import pytest
from value_object import Money

fiver = Money('usd', 5)
tenner = Money('usd', 10)

def test_equality() -> None:
    assert Money('usd', 10) == Money('usd', 10)

def can_add_money_values_for_the_same_currency():
    assert fiver + fiver == tenner

def adding_different_currencies_fails():
    with pytest.raises(ValueError):
        assert Money('gbp', 10) + Money('usd', 10)