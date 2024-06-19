import unittest
from data_analysis import TimeSeriesAnalysis


class TestTimeSeriesAnalysis(unittest.TestCase):
    def setUp(self):
        pass

    def test_read_data(self):
        self.assertIsInstance(self.analysis, TimeSeriesAnalysis)

    def test_method1(self):
        result = self.analysis.method1()
        expected_result = "Expected Result"
        self.assertEqual(result, expected_result)

    def test_method2(self):
        result = self.analysis.method2()
        expected_result = "Expected Result"
        self.assertEqual(result, expected_result)


if __name__ == '__main__':
    unittest.main()