"""
Swedish Housing Calculator: Buy vs Rent Analysis
Calculates the financial comparison between buying an apartment and renting with investment.
"""

import numpy as np
from typing import Dict, List, Tuple


class HousingCalculator:
    """Main calculator for housing buy vs rent analysis."""

    def __init__(self,
                 apartment_price: float,
                 down_payment_percent: float = 0.15,
                 mortgage_years: int = 30,
                 interest_rate: float = 0.03,
                 avgift: float = 5000,  # Monthly fee in SEK
                 amortering_rate: float = 0.02,  # Annual amortization rate (2%)
                 property_appreciation: float = 0.02,  # Annual %
                 rent_price: float = 15000,  # Monthly rent in SEK
                 investment_return: float = 0.07):  # Annual %

        self.apartment_price = apartment_price
        self.down_payment_percent = down_payment_percent
        self.mortgage_years = mortgage_years
        self.interest_rate = interest_rate
        self.avgift = avgift
        self.amortering_rate = amortering_rate
        self.property_appreciation = property_appreciation
        self.rent_price = rent_price
        self.investment_return = investment_return

        # Derived values
        self.down_payment = apartment_price * down_payment_percent
        self.mortgage_amount = apartment_price - self.down_payment
        self.months = mortgage_years * 12

        # Calculate monthly amortization based on loan amount and amortization rate
        self.monthly_amortering = (self.mortgage_amount * self.amortering_rate) / 12


    def calculate_buying_scenario(self) -> Dict[str, List[float]]:
        """
        Calculate yearly costs and equity for buying scenario.
        Returns dict with keys: costs, equity, property_value, mortgage_balance
        """
        costs = []
        equity = []
        property_values = []
        mortgage_balances = []

        # Initial values
        current_property_value = self.apartment_price
        current_mortgage = self.mortgage_amount
        current_equity = self.down_payment

        monthly_interest_rate = self.interest_rate / 12

        for year in range(self.mortgage_years + 1):
            if year == 0:
                # Initial state
                costs.append(0)
                equity.append(current_equity)
                property_values.append(current_property_value)
                mortgage_balances.append(current_mortgage)
                continue

            # Calculate yearly costs (monthly amortization + interest + avgift)
            yearly_amortization = self.monthly_amortering * 12
            yearly_interest = (current_mortgage * monthly_interest_rate) * 12
            yearly_avgift = self.avgift * 12
            yearly_costs = yearly_amortization + yearly_interest + yearly_avgift
            costs.append(yearly_costs)

            # Update mortgage balance
            current_mortgage -= self.monthly_amortering * 12
            current_mortgage = max(0, current_mortgage)  # Don't go negative

            # Update equity (down payment + paid amortization)
            paid_amortization = min(self.mortgage_amount - current_mortgage,
                                   self.monthly_amortering * 12 * year)
            current_equity = self.down_payment + paid_amortization

            # Update property value with appreciation
            current_property_value *= (1 + self.property_appreciation)

            equity.append(current_equity)
            property_values.append(current_property_value)
            mortgage_balances.append(current_mortgage)

        return {
            'costs': costs,
            'equity': equity,
            'property_value': property_values,
            'mortgage_balance': mortgage_balances
        }

    def calculate_renting_scenario(self) -> Dict[str, List[float]]:
        """
        Calculate yearly costs and investment growth for renting scenario.
        Returns dict with keys: costs, investment_value, total_capital
        """
        costs = []
        investment_values = []
        total_capitals = []

        # The money saved by not buying (down payment + would-be mortgage payments)
        # For simplicity, we'll invest the down payment + monthly savings
        monthly_savings = self.monthly_amortering + (self.mortgage_amount * self.interest_rate / 12)

        current_investment = self.down_payment  # Start with down payment amount

        for year in range(self.mortgage_years + 1):
            if year == 0:
                costs.append(0)
                investment_values.append(current_investment)
                total_capitals.append(current_investment)
                continue

            # Yearly rent cost
            yearly_costs = self.rent_price * 12
            costs.append(yearly_costs)

            # Add monthly savings to investment throughout the year
            # Simplified: add savings at end of year
            current_investment += monthly_savings * 12
            current_investment *= (1 + self.investment_return)

            investment_values.append(current_investment)
            total_capitals.append(current_investment)

        return {
            'costs': costs,
            'investment_value': investment_values,
            'total_capital': total_capitals
        }

    def get_comparison_summary(self) -> Dict[str, float]:
        """Get summary comparison between buying and renting."""
        buying = self.calculate_buying_scenario()
        renting = self.calculate_renting_scenario()

        total_buying_costs = sum(buying['costs'])
        total_renting_costs = sum(renting['costs'])

        final_buying_equity = buying['equity'][-1] + buying['property_value'][-1] - buying['mortgage_balance'][-1]
        final_renting_capital = renting['total_capital'][-1]

        return {
            'total_buying_costs': total_buying_costs,
            'total_renting_costs': total_renting_costs,
            'cost_difference': total_buying_costs - total_renting_costs,
            'final_buying_net_worth': final_buying_equity,
            'final_renting_net_worth': final_renting_capital,
            'net_worth_difference': final_buying_equity - final_renting_capital
        }


def format_currency(amount: float) -> str:
    """Format amount as Swedish Krona."""
    return f"{amount:,.0f} SEK"


def calculate_monthly_mortgage_payment(principal: float, annual_rate: float, years: int) -> float:
    """Calculate monthly mortgage payment using standard formula."""
    monthly_rate = annual_rate / 12
    num_payments = years * 12

    if monthly_rate == 0:
        return principal / num_payments

    payment = principal * (monthly_rate * (1 + monthly_rate)**num_payments) / ((1 + monthly_rate)**num_payments - 1)
    return payment
