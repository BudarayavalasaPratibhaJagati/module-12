import pytest
from pydantic import ValidationError

from app.calculation_factory import CalculationFactory
from app.schemas import CalculationCreate


def test_factory_add_operation():
    op = CalculationFactory.get_operation("add")
    assert op.calculate(2, 3) == 5


def test_factory_divide_operation():
    op = CalculationFactory.get_operation("divide")
    assert op.calculate(10, 2) == 5


def test_factory_invalid_type_raises_value_error():
    with pytest.raises(ValueError):
        CalculationFactory.get_operation("power")


def test_calculation_create_divide_by_zero_raises():
    with pytest.raises(ValidationError):
        CalculationCreate(a=10, b=0, type="divide")


def test_calculation_create_valid_multiply():
    calc = CalculationCreate(a=2, b=4, type="multiply")
    assert calc.a == 2
    assert calc.b == 4
    assert calc.type == "multiply"
