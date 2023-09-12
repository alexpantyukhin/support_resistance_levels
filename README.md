# Support Resistance Levels

## Description

The "Support Resistance Levels" project is a tool designed to identify support and resistance levels in time series financial data, such as stock prices. Support and resistance levels are key price levels where a financial asset's price tends to stop and reverse its direction. This tool analyzes historical price data to detect these levels, helping traders and investors make informed decisions.

## Algorithm Overview

The algorithm works by:

 - Finding extrema (high and low points) in the financial data using a specified order parameter.
 - Calculating the percentage-based delta value to identify the range within which levels are considered significant.
 - Identifying left and right indexes within this delta range for each extremum.
 - Grouping extrema based on their values and indexes.
 - Generating level characteristics, including the indexes of associated minima and maxima, delta spread percentage, percent absolute value, and level value.
 - Merging similar levels to provide a concise representation of support and resistance.
 

## Usage Example

```python

import support_resistance_levels as srl

levels = srl.get_support_resistance_levels(self.stock_prices, 2, 5, None)

```

## Example pics:

![pic1](https://github.com/alexpantyukhin/support_resistance_levels/blob/main/pic1.jpg?raw=true)

![pic2](https://github.com/alexpantyukhin/support_resistance_levels/blob/main/pic2.jpg?raw=true)

## Development

Contribution is welcome.

## License

This project is licensed under the terms of the [MIT License](https://github.com/alexpantyukhin/support_resistance_levels/blob/main/LICENSE) .

## Authors

    Alexander Pantyukhin - https://github.com/alexpantyukhin

