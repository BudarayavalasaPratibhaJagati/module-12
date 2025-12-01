from typing import Optional
from sqlalchemy.orm import Session

from . import models, schemas
from .calculation_factory import CalculationFactory


def create_calculation(
    db: Session,
    calc_in: schemas.CalculationCreate,
    user_id: Optional[int] = None,
) -> models.Calculation:
    op = CalculationFactory.get_operation(calc_in.type)
    result = op.calculate(calc_in.a, calc_in.b)

    db_calc = models.Calculation(
        a=calc_in.a,
        b=calc_in.b,
        type=calc_in.type,
        result=result,
        user_id=user_id,
    )

    db.add(db_calc)
    db.commit()
    db.refresh(db_calc)
    return db_calc
