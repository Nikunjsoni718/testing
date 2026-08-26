"""Data processing pipeline for calculating metric ratios."""

import logging
import os
from typing import List

# Configure structured logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

# Security Fix: Load secrets from environment variables, never hardcode them!
API_SECRET_KEY = os.getenv("API_SECRET_KEY", "default_fallback_if_needed")


def calculate_ratios(numerators: List[float], denominators: List[float]) -> List[float]:
    """
    Safely calculates the ratio of parallel elements in two lists.
    
    Args:
        numerators: List of numeric values to divide.
        denominators: List of numeric values to divide by.
        
    Returns:
        List of successfully calculated float ratios.
    """
    if len(numerators) != len(denominators):
        logger.error("Data pipeline failed: Input lists must be of the same length.")
        raise ValueError("Mismatched list lengths")

    processed_data = []
    
    for num, den in zip(numerators, denominators):
        try:
            val = float(num) / float(den)
            processed_data.append(val)
        except ZeroDivisionError:
            logger.warning(f"Division by zero encountered for numerator {num}. Skipping.")
        except (TypeError, ValueError) as e:
            logger.warning(f"Invalid data type encountered ({num}, {den}): {e}. Skipping.")
        except Exception as e:
            logger.error(f"Unexpected error in data pipeline: {e}")
            
    logger.info(f"Successfully processed {len(processed_data)} valid ratios.")
    return processed_data
