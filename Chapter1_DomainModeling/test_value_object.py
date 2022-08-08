import pytest
from value_object import Money, Name, Person

fiver = Money('usd', 5)
tenner = Money('usd', 10)

def test_equality() -> None:
    assert Money('usd', 10) == Money('usd', 10)

def can_add_money_values_for_the_same_currency():
    assert fiver + fiver == tenner

def adding_different_currencies_fails():
    with pytest.raises(ValueError):
        assert Money('gbp', 10) + Money('usd', 10)


# This is a value object, 
def test_name_equality():
    assert Name("Harry", "Percival") != Name("Barry", "Percival")


def test_barry_is_harry():
    harry = Person(Name("Harry", "Percival"))
    barry = harry

    barry.name = Name("Barry", "Percival")

    assert harry is barry and barry is harry