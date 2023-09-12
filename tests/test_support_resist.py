import unittest
from support_resistance import get_support_resistance_levels, LevelCharacteristics
import pandas as pd


class TestSupportResistanceLevels(unittest.TestCase):
	 
    def setUp(self):
        # Create sample stock price data
        self.stock_prices = pd.DataFrame({
            'high': [238.5, 241.6, 243.5, 243.3, 242.8, 239.6, 242.8, 234.4, 239.7, 238.8, 238.4, 244.8, 257.9, 253.7, 248.8, 249.0, 249.2, 249.5, 249.0, 247.5],
            'low': [235.8, 236.0, 237.8, 240.2, 230.2, 218.8, 225.1, 227.5, 231.3, 235.7, 235.8, 233.3, 241.0, 240.6, 242.2, 243.0, 243.1, 246.5, 240.0, 244.1],
            'open': [236.9, 238.0, 237.8, 242.4, 240.8, 230.9, 237.7, 231.6, 234.1, 235.9, 236.0, 237.4, 244.1, 250.9, 246.2, 248.9, 244.2, 249.0, 240.0, 244.1], 
            'close': [237.5, 238.8, 242.3, 241.2, 232.5, 238.2, 231.0, 230.7, 236.9, 238.0, 238.1, 243.9, 248.7, 246.3, 246.1, 245.2, 246.9, 249.0, 247.7, 246.4], 
            'volume': [28330, 72827, 2415, 1439, 82025, 125453, 123675, 26170, 92570, 1065, 561, 133279, 567614, 122666, 36814, 52672, 1990, 1372, 48253, 41202],
        })


    def test_get_support_resistance_levels(self):
        levels = get_support_resistance_levels(self.stock_prices, 2, 5, None)
    
        self.assertEqual(len(levels), 2)
        self.assertIsInstance(levels[0], LevelCharacteristics)
        self.assertIsInstance(levels[1], LevelCharacteristics)


    def test_get_support_resistance_levels_order_is_negative(self):
        with self.assertRaises(ValueError):
            get_support_resistance_levels(self.stock_prices, -2, 5, None)

    def test_get_support_resistance_levels_order_is_not_int(self):
        with self.assertRaises(ValueError):
            get_support_resistance_levels(self.stock_prices, '-2', 5, None)


    def test_get_support_resistance_levels_level_merge_percentage_is_negative(self):
        with self.assertRaises(ValueError):
            get_support_resistance_levels(self.stock_prices, 2, -5, None)

    def test_get_support_resistance_levels_level_merge_percentage_is_not_int(self):
        with self.assertRaises(ValueError):
            get_support_resistance_levels(self.stock_prices, 2, -5, None)
    
    # def test_get_support_resistance_levels_no_max_levels(self):
    #     """
    #     Test the get_support_resistance_levels function without specifying max_level_number.
    
    #     Scenario:
    #     - Test with sample stock price data.
    #     - Order = 2
    #     - Level merge percentage = 10%
    
    #     Expected Result:
    #     - Total points of support and resistance levels: 4
    #     - List of LevelCharacteristics objects representing the detected levels.
    #     """
    #     levels = get_support_resistance_levels(self.stock_prices, 2, 10)
    
    #     self.assertEqual(levels[0], 4)
    #     self.assertEqual(len(levels[1]), 3)
    #     self.assertIsInstance(levels[1][0], LevelCharacteristics)
    #     self.assertIsInstance(levels[1][1], LevelCharacteristics)
    #     self.assertIsInstance(levels[1][2], LevelCharacteristics)
    
    # def test_get_support_resistance_levels_custom_level_point(self):
    #     """
    #     Test the get_support_resistance_levels function with a custom level_point function.
    
    #     Scenario:
    #     - Test with sample stock price data.
    #     - Order = 2
    #     - Level merge percentage = 10%
    #     - Max level number = 1
    #     - Custom level_point function that returns the level value.
    
    #     Expected Result:
    #     - Total points of support and resistance levels: 1
    #     - List of LevelCharacteristics objects representing the detected levels.
    #     """
    #     def custom_level_point(level: LevelCharacteristics) -> float:
    #         return level.level_value
    
    #     levels = get_support_resistance_levels(self.stock_prices, 2, 10, 1, custom_level_point)
    
    #     self.assertEqual(levels[0], 1)
    #     self.assertEqual(len(levels[1]), 1)
    #     self.assertIsInstance(levels[1][0], LevelCharacteristics)
    
    # def test_get_support_resistance_levels_empty_stock_prices(self):
    #     """
    #     Test the get_support_resistance_levels function with empty stock_prices.
    
    #     Scenario:
    #     - Test with empty DataFrame for stock_prices.
    #     - Order = 2
    #     - Level merge percentage = 10%
    #     - Max level number = 2
    
    #     Expected Result:
    #     - Total points of support and resistance levels: 0
    #     - Empty list of LevelCharacteristics objects.
    #     """
    #     empty_stock_prices = pd.DataFrame()
    
    #     levels = get_support_resistance_levels(empty_stock_prices, 2, 10, 2)
    
    #     self.assertEqual(levels[0], 0)
    #     self.assertEqual(len(levels[1]), 0)
    
    # def test_get_support_resistance_levels_negative_order(self):
    #     """
    #     Test the get_support_resistance_levels function with negative order.
    
    #     Scenario:
    #     - Test with sample stock price data.
    #     - Order = -1
    #     - Level merge percentage = 10%
    #     - Max level number = 2
    
    #     Expected Result:
    #     - Total points of support and resistance levels: 0
    #     - Empty list of LevelCharacteristics objects.
    #     """
    #     levels = get_support_resistance_levels(self.stock_prices, -1, 10, 2)
    
    #     self.assertEqual(levels[0], 0)
    #     self.assertEqual(len(levels[1]), 0)
    
    # def test_get_support_resistance_levels_negative_level_merge_percentage(self):
    #     """
    #     Test the get_support_resistance_levels function with negative level_merge_percentage.
    
    #     Scenario:
    #     - Test with sample stock price data.
    #     - Order = 2
    #     - Level merge percentage = -10%
    #     - Max level number = 2
    
    #     Expected Result:
    #     - Total points of support and resistance levels: 0
    #     - Empty list of LevelCharacteristics objects.
    #     """
    #     levels = get_support_resistance_levels(self.stock_prices, 2, -10, 2)
    
    #     self.assertEqual(levels[0], 0)
    #     self.assertEqual(len(levels[1]), 0)
    
    # def test_get_support_resistance_levels_invalid_max_level_number(self):
    #     """
    #     Test the get_support_resistance_levels function with invalid max_level_number.
    
    #     Scenario:
    #     - Test with sample stock price data.
    #     - Order = 2
    #     - Level merge percentage = 10%
    #     - Max level number = -1
    
    #     Expected Result:
    #     - Total points of support and resistance levels: 0
    #     - Empty list of LevelCharacteristics objects.
    #     """
    #     levels = get_support_resistance_levels(self.stock_prices, 2, 10, -1)
    
    #     self.assertEqual(levels[0], 0)
    #     self.assertEqual(len(levels[1]), 0)

if __name__ == '__main__':
    unittest.main()