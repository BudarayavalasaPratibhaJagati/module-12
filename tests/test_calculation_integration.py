from pydantic import ValidationError
from sqlalchemy.orm import Session

from app import models, schemas
from app.crud_calculation import create_calculation


def test_create_calculation_stores_in_db(db_session: Session):
    calc_in = schemas.CalculationCreate(a=3, b=7, type="add")

    db_calc = create_calculation(db_session, calc_in)

    assert db_calc.id is not None
    assert db_calc.a == 3
    assert db_calc.b == 7
    assert db_calc.type == "add"
    assert db_calc.result == 10

    calc_from_db = db_session.query(models.Calculation).filter_by(id=db_calc.id).first()
    assert calc_from_db is not None
    assert calc_from_db.result == 10


def test_create_calculation_divide_by_zero_fails_before_db(db_session: Session):
    # Pydantic should reject this before DB insertion
    try:
        schemas.CalculationCreate(a=5, b=0, type="divide")
        assert False, "Expected ValidationError"
    except ValidationError:
        assert True
