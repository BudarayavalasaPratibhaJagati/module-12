from abc import ABC, abstractmethod


class Operation(ABC):
    @abstractmethod
    def calculate(self, a: float, b: float) -> float:
        ...


class AddOperation(Operation):
    def calculate(self, a: float, b: float) -> float:
        return a + b


class SubOperation(Operation):
    def calculate(self, a: float, b: float) -> float:
        return a - b


class MultiplyOperation(Operation):
    def calculate(self, a: float, b: float) -> float:
        return a * b


class DivideOperation(Operation):
    def calculate(self, a: float, b: float) -> float:
        return a / b


class CalculationFactory:
    @staticmethod
    def get_operation(calc_type: str) -> Operation:
        calc_type = calc_type.lower()
        if calc_type == "add":
            return AddOperation()
        if calc_type == "sub":
            return SubOperation()
        if calc_type == "multiply":
            return MultiplyOperation()
        if calc_type == "divide":
            return DivideOperation()
        raise ValueError(f"Unknown calculation type: {calc_type}")
