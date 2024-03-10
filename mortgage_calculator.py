import streamlit as st
import numpy_financial as npf
import sys

# Set page title
st.title("How much house can I afford?")

# Create input widgets
monthly_payment = st.number_input("Desired monthly mortgage payment, before tax (DKK)")
maintenance_fees = st.number_input("Monthly maintenance fees (DKK)")
downpayment = st.number_input("Personal downpayment (DKK)")
price = st.number_input("Price of the apartment (DKK)")
annual_interest_rate = st.slider(
    "Annual interest rate on realkredit loan (%):",
    min_value=0.0,
    max_value=10.0,
    value=4.0,
    step=0.05,
)
bank_interest_rate = st.slider(
    "Annual interest on bank loan (%)",
    min_value=0.0,
    max_value=10.0,
    value=5.0,
    step=0.05,
)
loan_term_years = st.slider(
    "Mortgage duration (years):", min_value=1, max_value=30, value=30, step=1
)

# Create button to calculate result
calculate_button = st.button("Calculate")

# Calculate result when button is clicked
if calculate_button:
    if not maintenance_fees:
        st.error("ERROR: Please provide monthly maintenance fees!")
    elif not annual_interest_rate:
        st.error("ERROR: Please provide the prevailing interest rate!")
    elif not loan_term_years:
        st.error("ERROR: Please provide your desired mortgage duration!")
    elif not downpayment or downpayment < price * 0.05:
        st.error("ERROR: Please provide a down payment exceeding 5% of price!")
    elif not any([monthly_payment, price]):
        st.error(
            """ERROR: Please provide either your desired monthly mortgage payment 
            or apartment price to calculate the other"""
        )
    else:
        if monthly_payment:
            monthly_costs = monthly_payment + maintenance_fees
            affordable_price = npf.pv(
                rate=annual_interest_rate / 12 / 100,
                nper=loan_term_years * 12,
                pmt=-monthly_costs,
                fv=0,
            )
            st.success(f"You can afford an apartment for {affordable_price:.2f} DKK")
        elif price:
            if downpayment < price * 0.05:
                st.error("ERROR: Your downpayment must exceed 5% of price!")
                sys.exit(0)
            elif downpayment >= price * 0.05:
                if downpayment < price * 0.2:
                    realkredit_loan = price * 0.2
                    bankloan = price - (price * 0.2)
                realkredit_loan = price - downpayment
                bank_loan = 
            monthly_payment_mortgage = npf.pmt(
                rate=annual_interest_rate / 12 / 100,
                nper=loan_term_years * 12,
                pv=price - downpayment,
                fv=0,
            )
            monthly_payment = -1 * monthly_payment + maintenance_fees
            st.success(f"Your monthly costs will be {monthly_payment:.2f} DKK")
