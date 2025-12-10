import pytest
import sys
from pathlib import Path

# Add 2025 directory to path to allow imports
sys.path.insert(0, str(Path(__file__).parent))

from day10 import encode


class TestEncode:
    """Unit tests for encode function."""

    def test_example_1(self):
        """Test first example from docstring."""
        wirings = [(0,), (1, 2), (2, 0)]
        joltage = (5, 10, 5)
        expected_wirings = (1, 1010, 1001)
        expected_joltage = 5105

        result_wirings, result_joltage = encode(wirings, joltage)
        assert result_wirings == expected_wirings
        assert result_joltage == expected_joltage

    def test_example_2(self):
        """Test second example from docstring."""
        wirings = [(1,), (3,), (2, 3)]
        joltage = (1, 10, 4, 7)
        expected_wirings = (10, 10000, 10100)
        expected_joltage = 11047

        result_wirings, result_joltage = encode(wirings, joltage)
        assert result_wirings == expected_wirings
        assert result_joltage == expected_joltage
