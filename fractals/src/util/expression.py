from abc import ABC


class Expression(ABC):
    def evaluate(self, x: float, y: float) -> float:
        raise NotImplementedError("Subclass must implement.")
