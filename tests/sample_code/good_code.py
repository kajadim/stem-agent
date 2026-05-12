# tests/sample_code/good_code.py
import logging

logger = logging.getLogger(__name__)

def calculate(a: int, b: int) -> float:
    """Divides a by b and returns the result."""
    if b == 0:
        raise ValueError("Cannot divide by zero")
    
    result = a / b
    logger.info("Calculation complete")
    return result