"""
Streamlit UI for Swedish Housing Buy vs Rent Calculator
Interactive tool to compare buying vs renting costs and returns in Sweden.
"""

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from housing_calculator import HousingCalculator, format_currency

# Set page config
st.set_page_config(
    page_title="Swedish Housing Calculator",
    page_icon="🏠",
    layout="wide"
)

# Title and description
st.title("🏠 Swedish Housing: Buy vs Rent Calculator")
st.markdown("""
Compare the costs and potential returns of buying an apartment versus renting and investing the difference.
This calculator includes Swedish-specific factors like *avgift* (monthly housing association fee) and automatic *amortering* calculation based on loan amount.
""")

# Sidebar with input parameters
st.sidebar.header("📊 Input Parameters")

# Basic apartment details
st.sidebar.subheader("🏢 Apartment Details")
apartment_price = st.sidebar.number_input(
    "Apartment Price (SEK)",
    min_value=100000,
    max_value=10000000,
    value=6000000,
    step=50000,
    format="%d"
)

down_payment_percent = st.sidebar.slider(
    "Down Payment (%)",
    min_value=5,
    max_value=50,
    value=15,
    step=1
)

mortgage_years = st.sidebar.slider(
    "Mortgage Length (years)",
    min_value=10,
    max_value=50,
    value=50,
    step=5
)

# Financial parameters
st.sidebar.subheader("💰 Financial Parameters")
interest_rate = st.sidebar.slider(
    "Interest Rate (%)",
    min_value=0.0,
    max_value=10.0,
    value=3.0,
    step=0.1
) / 100

avgift = st.sidebar.number_input(
    "Monthly Avgift (SEK)",
    min_value=0,
    max_value=20000,
    value=5000,
    step=500
)

# Amortization rate input
amortering_rate = st.sidebar.slider(
    "Annual Amortization Rate (%)",
    min_value=1.0,
    max_value=5.0,
    value=2.0,
    step=0.5
) / 100

# Market expectations
st.sidebar.subheader("📈 Market Expectations")
property_appreciation = st.sidebar.slider(
    "Expected Annual Property Appreciation (%)",
    min_value=-5.0,
    max_value=15.0,
    value=2.0,
    step=0.5
) / 100

rent_price = st.sidebar.number_input(
    "Monthly Rent (SEK)",
    min_value=5000,
    max_value=50000,
    value=18000,
    step=1000
)

investment_return = st.sidebar.slider(
    "Expected Annual Investment Return (%)",
    min_value=0.0,
    max_value=15.0,
    value=5.0,
    step=0.5
) / 100

# Calculate button
if st.sidebar.button("🔍 Run Analysis", type="primary"):
    # Create calculator instance
    calculator = HousingCalculator(
        apartment_price=apartment_price,
        down_payment_percent=down_payment_percent / 100,
        mortgage_years=mortgage_years,
        interest_rate=interest_rate,
        avgift=avgift,
        amortering_rate=amortering_rate,
        property_appreciation=property_appreciation,
        rent_price=rent_price,
        investment_return=investment_return
    )

    # Display calculated amortization details
    calculated_rate = calculator.amortering_rate
    loan_amount = calculator.mortgage_amount
    monthly_amortization = calculator.monthly_amortering
    ltv_ratio = loan_amount / apartment_price

    # Get calculations
    buying_data = calculator.calculate_buying_scenario()
    renting_data = calculator.calculate_renting_scenario()
    summary = calculator.get_comparison_summary()

    # Display loan and amortization details
    st.sidebar.markdown("---")
    st.sidebar.markdown("**📊 Loan & Amortization Details:**")

    st.sidebar.write(f"**Loan Amount:** {format_currency(loan_amount)}")
    st.sidebar.write(f"**Amortization Rate:** {calculated_rate*100:.1f}% annually")
    st.sidebar.write(f"**Monthly Amortization:** {format_currency(monthly_amortization)}")

    # Display results
    st.header("📊 Analysis Results")

    # Summary metrics
    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "Total Buying Costs",
            format_currency(summary['total_buying_costs']),
            help="Total payments over the mortgage period"
        )

    with col2:
        st.metric(
            "Total Renting Costs",
            format_currency(summary['total_renting_costs']),
            help="Total rent payments over the period"
        )

    with col3:
        cost_diff = summary['cost_difference']
        st.metric(
            "Cost Difference",
            format_currency(abs(cost_diff)),
            delta=f"{'Renting' if cost_diff > 0 else 'Buying'} is cheaper",
            help="Positive = Buying costs more, Negative = Renting costs more"
        )

    # Net worth comparison
    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "Final Buying Net Worth",
            format_currency(summary['final_buying_net_worth']),
            help="Property value + equity - mortgage balance"
        )

    with col2:
        st.metric(
            "Final Renting Net Worth",
            format_currency(summary['final_renting_net_worth']),
            help="Investment portfolio value"
        )

    with col3:
        worth_diff = summary['net_worth_difference']
        st.metric(
            "Net Worth Difference",
            format_currency(abs(worth_diff)),
            delta=f"{'Renting' if worth_diff < 0 else 'Buying'} builds more wealth",
            help="Positive = Buying builds more wealth, Negative = Renting builds more wealth"
        )

    # Charts section
    st.header("📈 Detailed Analysis")

    # Prepare data for charts
    years = list(range(mortgage_years + 1))
    chart_data = pd.DataFrame({
        'Year': years,
        'Buying Costs': buying_data['costs'],
        'Renting Costs': renting_data['costs'],
        'Buying Equity': buying_data['equity'],
        'Property Value': buying_data['property_value'],
        'Investment Value': renting_data['investment_value']
    })

    # Cost comparison chart
    st.subheader("💸 Yearly Costs Comparison")
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.plot(chart_data['Year'], chart_data['Buying Costs'], label='Buying Costs', color='red', linewidth=2)
    ax.plot(chart_data['Year'], chart_data['Renting Costs'], label='Renting Costs', color='blue', linewidth=2)
    ax.set_xlabel('Year')
    ax.set_ylabel('Cost (SEK)')
    ax.set_title('Yearly Housing Costs: Buying vs Renting')
    ax.legend()
    ax.grid(True, alpha=0.3)
    st.pyplot(fig)

    # Wealth accumulation chart
    st.subheader("🏦 Wealth Accumulation")
    fig, ax = plt.subplots(figsize=(10, 6))
    buying_net_worth = [buying_data['property_value'][i] - buying_data['mortgage_balance'][i]
                       for i in range(len(years))]
    ax.plot(chart_data['Year'], buying_net_worth, label='Buying Net Worth', color='green', linewidth=2)
    ax.plot(chart_data['Year'], chart_data['Investment Value'], label='Renting Investment', color='orange', linewidth=2)
    ax.set_xlabel('Year')
    ax.set_ylabel('Value (SEK)')
    ax.set_title('Net Worth Over Time: Buying vs Renting')
    ax.legend()
    ax.grid(True, alpha=0.3)
    st.pyplot(fig)

    # Detailed breakdown
    st.header("📋 Detailed Breakdown")

    # Buying scenario details
    with st.expander("🏠 Buying Scenario Details"):
        st.write("**Yearly Costs Breakdown:**")
        buying_breakdown = pd.DataFrame({
            'Year': years,
            'Total Costs': buying_data['costs'],
            'Equity Built': buying_data['equity'],
            'Property Value': buying_data['property_value'],
            'Mortgage Balance': buying_data['mortgage_balance']
        })
        st.dataframe(buying_breakdown.style.format({
            'Total Costs': '{:,.0f} SEK',
            'Equity Built': '{:,.0f} SEK',
            'Property Value': '{:,.0f} SEK',
            'Mortgage Balance': '{:,.0f} SEK'
        }))

    # Renting scenario details
    with st.expander("🏢 Renting Scenario Details"):
        st.write("**Yearly Costs Breakdown:**")
        renting_breakdown = pd.DataFrame({
            'Year': years,
            'Total Costs': renting_data['costs'],
            'Investment Value': renting_data['investment_value']
        })
        st.dataframe(renting_breakdown.style.format({
            'Total Costs': '{:,.0f} SEK',
            'Investment Value': '{:,.0f} SEK'
        }))

else:
    # Welcome message when no analysis has been run
    st.info("👈 Adjust the parameters in the sidebar and click 'Run Analysis' to see the comparison.")

    # Default example
    st.header("💡 How It Works")
    st.markdown("""
    This calculator compares two scenarios:

    **Buying Scenario:**
    - Pay mortgage (interest + amortization)
    - Pay monthly avgift
    - Build equity through amortization
    - Benefit from property appreciation
    - End up with property ownership

    **Renting Scenario:**
    - Pay monthly rent
    - Invest the money you would have used for down payment and mortgage payments
    - Benefit from investment returns
    - End up with investment portfolio

    **Key Swedish Factors:**
    - **Avgift**: Monthly fee to the housing association (bostadsrättsförening)
    - **Amortering**: Required amortization payments (can be 1-3% of loan amount per year)
    - Property prices and interest rates specific to Swedish market
    """)

# Footer
st.markdown("---")
st.markdown("*Note: This is a simplified model for educational purposes. Consult a financial advisor for personal financial decisions.*")
