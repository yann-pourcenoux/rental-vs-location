# Swedish Housing: Buy vs Rent Calculator

A comprehensive tool to compare the financial implications of buying an apartment versus renting and investing the difference in Sweden.

## Features

- **Swedish-specific calculations**: Includes avgift (housing association fees) and amortering (amortization)
- **Interactive parameters**: Adjust all key variables through the sidebar
- **Visual comparisons**: Charts showing yearly costs and wealth accumulation
- **Detailed breakdowns**: Year-by-year analysis of both scenarios
- **Summary metrics**: Clear comparison of total costs and final net worth

## Installation

1. Clone this repository
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

Run the Streamlit application:
```bash
./run.sh
# or
streamlit run app.py --server.port 3156
```

The application will open in your default web browser at `http://localhost:3156`.

## Input Parameters

### Apartment Details
- **Apartment Price**: Purchase price in SEK (default: 6,000,000 SEK)
- **Down Payment**: Percentage of purchase price (5-50%, default: 15%)
- **Mortgage Length**: Number of years (10-50, default: 50 years)

### Financial Parameters
- **Interest Rate**: Annual mortgage interest rate (default: 3%)
- **Monthly Avgift**: Housing association fee in SEK (default: 5,000 SEK)
- **Annual Amortization Rate**: Annual percentage rate (1-5%)

### Market Expectations
- **Property Appreciation**: Expected annual increase in property value (default: 2%)
- **Monthly Rent**: Cost of equivalent rental in SEK (default: 18,000 SEK)
- **Investment Return**: Expected annual return on investments (default: 5%)

## Swedish Housing Context

This calculator accounts for key aspects of the Swedish housing market:

- **Bostadsrätt**: Most apartments in Sweden are owned through housing associations
- **Avgift**: Monthly fee covering maintenance, common areas, etc.
- **Amortering**: Annual amortization rate that you can set (typically 1-3% annually)
- **Property Taxes**: Not included (complex and varies by municipality)
- **Interest Deductions**: Not included (available in Sweden)

## Important Notes

⚠️ **Disclaimer**: This is a simplified model for educational purposes only. Real financial decisions should consider:
- Personal tax situation
- Inflation
- Transaction costs (broker fees, legal fees)
- Maintenance costs
- Insurance
- Local market conditions
- Personal risk tolerance

Always consult with a qualified financial advisor before making major housing decisions.

## Technical Details

- Built with Python, Streamlit, Pandas, and Matplotlib
- Modular design with separate calculation engine
- Responsive web interface
- Real-time parameter adjustment
