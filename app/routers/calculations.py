from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app import models, schemas

router = APIRouter(
    prefix="/calculations",
    tags=["calculations"],
)


def compute_result(a: float, b: float, calc_type: str) -> float:
    if calc_type == "Add":
        return a + b
    elif calc_type == "Sub":
        return a - b
    elif calc_type == "Multiply":
        return a * b
    elif calc_type == "Divide":
        if b == 0:
            # This is a second line of defense; usually Pydantic catches it first
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Cannot divide by zero",
            )
        return a / b
    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid calculation type; use Add, Sub, Multiply, Divide",
        )


@router.get("/", response_model=list[schemas.CalculationRead])
def list_calculations(db: Session = Depends(get_db)):
    return db.query(models.Calculation).all()


@router.get("/{calc_id}", response_model=schemas.CalculationRead)
def get_calculation(calc_id: int, db: Session = Depends(get_db)):
    calc = db.query(models.Calculation).filter(models.Calculation.id == calc_id).first()
    if not calc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Calculation not found")
    return calc


@router.post("/", response_model=schemas.CalculationRead, status_code=status.HTTP_201_CREATED)
def create_calculation(calc_in: schemas.CalculationCreate, db: Session = Depends(get_db)):
    result = compute_result(calc_in.a, calc_in.b, calc_in.type)
    calc = models.Calculation(
        a=calc_in.a,
        b=calc_in.b,
        type=calc_in.type,
        result=result,
        user_id=calc_in.user_id,
    )
    db.add(calc)
    db.commit()
    db.refresh(calc)
    return calc


@router.put("/{calc_id}", response_model=schemas.CalculationRead)
def update_calculation(calc_id: int, calc_in: schemas.CalculationCreate, db: Session = Depends(get_db)):
    calc = db.query(models.Calculation).filter(models.Calculation.id == calc_id).first()
    if not calc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Calculation not found")

    calc.a = calc_in.a
    calc.b = calc_in.b
    calc.type = calc_in.type
    calc.result = compute_result(calc_in.a, calc_in.b, calc_in.type)
    calc.user_id = calc_in.user_id

    db.commit()
    db.refresh(calc)
    return calc


@router.delete("/{calc_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_calculation(calc_id: int, db: Session = Depends(get_db)):
    calc = db.query(models.Calculation).filter(models.Calculation.id == calc_id).first()
    if not calc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Calculation not found")

    db.delete(calc)
    db.commit()
    return
