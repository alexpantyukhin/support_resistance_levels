import pandas as pd
from scipy.signal import argrelextrema
import numpy as np
from dataclasses import dataclass
from functools import lru_cache
from typing import Optional, Callable, List, Tuple


# Class to store level characteristics
@dataclass
class LevelCharacteristics:
    mins_indexes: List[int]
    maxs_indexes: List[int]
    delta_spread_percentage: float
    percent_abs_value: float
    level_value: float


# Function to find extrema
def _find_extremas(
    stock_prices: pd.DataFrame, order: int
) -> Tuple[List[int], List[int], List[int], List[int]]:
    min_open_close = stock_prices[["close", "open"]].min(axis=1).to_numpy()
    max_open_close = stock_prices[["close", "open"]].max(axis=1).to_numpy()

    min_extrema = argrelextrema(min_open_close, np.less_equal, order=order)
    max_extrema = argrelextrema(max_open_close, np.greater_equal, order=order)

    return (
        min_extrema[0],
        max_extrema[0],
        list(min_open_close[min_extrema[0]]),
        list(max_open_close[max_extrema[0]]),
    )


# Function to find left and right indexes within delta range
def _find_left_right_indexes_in_delta(
    sorted_array: List[float], delta_absolute: float
) -> List[Tuple[int, int]]:
    left_bound = 0
    right_bound = 0
    len_sorted_array = len(sorted_array)

    result = []
    for i in range(len_sorted_array):
        value = sorted_array[i]

        for j in range(left_bound, i + 1):
            if sorted_array[j] >= value - delta_absolute:
                break

        left_bound = j

        for k in range(right_bound, len_sorted_array):
            if sorted_array[k] > value + delta_absolute:
                break

        right_bound = k - 1

        result.append((left_bound, right_bound))

    return result


# Function to get indexes of values
def _get_value_indexes(keys, values):
    dct = {}
    for i in range(len(keys)):
        if values[i] not in dct:
            dct[values[i]] = []

        dct[values[i]].append(keys[i])

    return dct


# Function to get level characteristics
def _get_level_characteristics(
    stocks: pd.DataFrame, order: int, percentage: int
) -> List[LevelCharacteristics]:
    mins, maxs, mins_vals, maxs_vals = _find_extremas(stocks, order)
    extremas = sorted(mins_vals + maxs_vals)
    len_extremas = len(extremas)

    max_value = stocks[["close", "low", "high", "open"]].max(axis=1).to_numpy().max()
    percent_abs_value = max_value * percentage / 100
    left_right_indexes = _find_left_right_indexes_in_delta(extremas, percent_abs_value)

    mins_values_indexes = _get_value_indexes(mins, mins_vals)
    maxs_values_indexes = _get_value_indexes(maxs, maxs_vals)

    result = []
    for i in range(len_extremas):
        level = extremas[i]
        left_index, right_index = left_right_indexes[i]

        mins_full = []
        maxs_full = []
        for i in range(left_index, right_index + 1):
            extrema = extremas[i]

            if extrema in mins_values_indexes:
                mins_full += mins_values_indexes[extrema]

            if extrema in maxs_values_indexes:
                maxs_full += maxs_values_indexes[extrema]

        result.append(
            LevelCharacteristics(
                mins_indexes=mins_full,
                maxs_indexes=maxs_full,
                delta_spread_percentage=percentage,
                percent_abs_value=percent_abs_value,
                level_value=level,
            )
        )

    return result


# Function to get the number of points on a level
def _get_level_points(level: LevelCharacteristics) -> int:
    return len(level.mins_indexes) + len(level.maxs_indexes)


# Function for binary search
def _binary_search(low, high, arr, x):
    while low <= high:
        mid = (high + low) // 2

        if (mid - 1 < 0 or arr[mid - 1] < x) and arr[mid] >= x:
            return mid

        if arr[mid] < x:
            low = mid + 1
        else:
            high = mid - 1

    return len(arr)


# Function to merge levels
def _merge_levels_best_way(
    levels: List[LevelCharacteristics],
    max_levels: Optional[int] = None,
    level_point: Callable[[LevelCharacteristics], float] = None,
) -> Tuple[int, List[LevelCharacteristics]]:
    len_levels = len(levels)
    levels_values = list(map(lambda x: x.level_value, levels))
    if level_point is None:
        level_point = _get_level_points

    @lru_cache(maxsize=None)
    def get_best_dp(index: int, left_levels: Optional[int]):
        if index >= len_levels or left_levels == 0:
            return (0, None)

        level = levels[index]
        next_level_index = _binary_search(
            index,
            len_levels - 1,
            levels_values,
            level.level_value + level.percent_abs_value,
        )

        # 1. Skip the current level and find the best variant without the current one.
        without_curr_level_points, without_curr_level_result = get_best_dp(
            index + 1, left_levels
        )

        # 2. Check the current level and find the best variant with the current one.
        next_left_levels = None if left_levels is None else left_levels - 1
        with_curr_level_point, with_curr_level_result = get_best_dp(
            next_level_index, next_left_levels
        )

        curr_level_points = level_point(level)
        if curr_level_points + with_curr_level_point > without_curr_level_points:
            return (
                curr_level_points + with_curr_level_point,
                [level, with_curr_level_result],
            )

        return (without_curr_level_points, without_curr_level_result)

    points, unwraped_levels = get_best_dp(0, max_levels)

    res_levels = []

    def unwrap_levels(inner_levels_struct):
        if inner_levels_struct is None:
            return

        res_levels.append(inner_levels_struct[0])
        unwrap_levels(inner_levels_struct[1])

    unwrap_levels(unwraped_levels)

    return points, res_levels


def __validate_stock_price_dataframe(stock_price: pd.DataFrame):
    expected_columns = {
        "close": ["float64", "float32"],
        "high": ["float64", "float32"],
        "low": ["float64", "float32"],
        "open": ["float64", "float32"],
        "volume": ["int8", "int16", "int32", "int64"],
    }

    missing_columns = [
        col for col in expected_columns if col not in stock_price.columns
    ]
    mismatched_columns = [
        col
        for col in expected_columns
        if stock_price[col].dtype.name not in expected_columns[col]
    ]

    if len(missing_columns) > 0:
        raise ValueError(f"Missing columns: {missing_columns}")

    if len(mismatched_columns) > 0:
        raise ValueError(f"Columns with type mismatches: {mismatched_columns}")


# Main function to calculate support and resistance levels
def get_support_resistance_levels(
    stock_price: pd.DataFrame,
    order: int,
    level_merge_percentage: float,
    max_level_number: Optional[int] = None,
    level_point: Callable[[LevelCharacteristics], float] = None,
) -> Tuple[int, List[LevelCharacteristics]]:
    """
    Calculate support and resistance levels based on input stock price data.

    Args:
        stock_price (pd.DataFrame): A DataFrame containing stock price data.
        order (int): The order for detecting extrema in the data.
        level_merge_percentage (float): The percentage used for merging similar levels.
        max_level_number (Optional[int], optional):
            The maximum number of levels to return. Defaults to None.
        level_point (Callable[[LevelCharacteristics], float], optional):
            A custom function to calculate the points for each level.
            If not provided, a default point calculation function is used.

    Returns:
        Tuple[int, List[LevelCharacteristics]]:
            A tuple containing the total points of support and resistance levels and a
            List of LevelCharacteristics objects representing the detected levels.
    """

    __validate_stock_price_dataframe(stock_price)

    if not isinstance(order, int) or order <= 0:
        raise ValueError("The order parameter should a positive int.")

    if (
        not (
            isinstance(level_merge_percentage, float)
            or isinstance(level_merge_percentage, int)
        )
        or level_merge_percentage <= 0
    ):
        raise ValueError(
            "The level_merge_percentage parameter should be a positive float."
        )

    if max_level_number is not None and (
        not isinstance(max_level_number, int) or max_level_number <= 0
    ):
        raise ValueError(
            "The max_level_number parameter should be a None or positive int."
        )

    levels = _get_level_characteristics(stock_price, order, level_merge_percentage)

    _, best_levels = _merge_levels_best_way(levels, max_level_number, level_point)
    return best_levels
