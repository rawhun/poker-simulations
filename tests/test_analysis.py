import unittest
from poker.analysis import calculate_equity

class TestAnalysis(unittest.TestCase):
    def test_equity_vs_pair(self):
        eq = calculate_equity('AhKh', 'QdQc', iterations=100)
        self.assertTrue(0.0 <= eq <= 1.0)

    def test_equity_vs_range(self):
        eq = calculate_equity('AKs', 'QQ', iterations=100)
        self.assertTrue(0.0 <= eq <= 1.0)

if __name__ == '__main__':
    unittest.main() 