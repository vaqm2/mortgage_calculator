import streamlit as st
import numpy_financial as npf


class MortgageCalculatorApp:
    def __init__(self):
        pass

    def run(self):
        self.user_inputs = self._get_user_inputs()
        if self.user_inputs:
            self._calculate()

    def _get_user_inputs(self) -> dict:
        user_inputs = {}
        user_inputs["app_mode"] = st.selectbox(
            options=[
                "Apartment price calculator",
                "Monthly payment calculator",
            ],
            label="Mode",
        )
        with st.form(user_inputs["app_mode"]):
            if user_inputs["app_mode"] == "Apartment price calculator":
                user_inputs["monthly_payment"] = st.number_input(
                    "Desired monthly payment (DKK)", min_value=1, value=None
                )
                user_inputs["monthly_maintenance_fee"] = st.number_input(
                    "Monthly maintenance fee (DKK)", min_value=1, value=None
                )
            elif user_inputs["app_mode"] == "Monthly payment calculator":
                user_inputs["apartment_price"] = st.number_input(
                    "Apartment price (DKK)", min_value=1, value=None
                )
            user_inputs["downpayment"] = st.number_input(
                "Your downpayment", min_value=1, value=None
            )
            user_inputs["apy_realkredit"] = st.slider(
                "Annual interest rate on realkredit loan (%)",
                min_value=0.0,
                max_value=10.0,
                value=0.0,
                step=0.05,
            )
            user_inputs["apy_bankloan"] = st.slider(
                "Annual interest rate on bank loan (%)",
                min_value=0.0,
                max_value=10.0,
                value=0.0,
                step=0.05,
            )
            user_inputs["loan_years"] = st.slider(
                "Loan period (Years)", min_value=1, max_value=30, value=30, step=1
            )
            calculate_button = st.form_submit_button(
                "Calculate", disabled=not self._validate_user_inputs(user_inputs)
            )

            if calculate_button:
                return user_inputs

    def _validate_user_inputs(self, input_dict: dict) -> bool:
        """
        For a dictionary of user inputs, this function runs some sanity checks
        to ensure expected conditions are met and throws warning messages,
        returning False for inputs that are either invalid or defy Danish
        mortgage rules.
        """
        if input_dict["app_mode"] == "Apartment price calculator":
            if not input_dict["monthly_payment"]:
                st.warning("Please enter your desired monthly payment!")
                return False
            if not input_dict["monthly_maintenance_fee"]:
                st.warning("Please enter your desired monthly payment amount!")
                return False
            if not input_dict["downpayment"]:
                st.warning(
                    "Please enter a downpayment that is atleast 5% of apartment price!"
                )
        elif input_dict["app_mode"] == "Monthly payment calculator":
            if not input_dict["apartment_price"]:
                st.warning("Please enter the apartment price!")
                return False
            if not input_dict["monthly_maintenance_fee"]:
                st.error("Please enter the monthly association fee!")
                return False
            if (
                not input_dict["downpayment"]
                or input_dict["downpayment"] < 0.05 * input_dict["apartment_price"]
            ):
                st.warning(
                    "Please enter a downpayment that is atleast 5% of apartment price!"
                )
                return False
        return True

    def _calculate(self):
        """
        Write doc_string here
        """
        if self.user_inputs["app_mode"] == "Monthly payment calculator":
            if (
                self.user_inputs["downpayment"]
                < 0.2 * self.user_inputs["apartment_price"]
            ):
                rk_loan = 0.2 * self.user_inputs["apartment_price"]
                bank_loan = self.user_inputs["apartment_price"] - rk_loan
            else:
                bank_loan = 0
                rk_loan = self.user_inputs["price"] - self.user_inputs["downpayment"]
            if bank_loan > 0:
                monthly_payment_bank = self._calculate_monthly_payment(
                    bank_loan,
                    self.user_inputs["apy_bankloan"],
                    self.user_inputs["loan_years"],
                )
            else:
                monthly_payment_bank = 0
            if rk_loan > 0:
                monthly_payment_rk = self._calculate_monthly_payment(
                    rk_loan,
                    self.user_inputs["apy_realkredit"],
                    self.user_input["loan_years"],
                )
            else:
                monthly_payment_rk = 0

            net_monthly_payment = (
                -monthly_payment_bank
                - monthly_payment_rk
                + self.user_inputs["monthly_maintenance_fee"]
            )
            st.success(f"Your monthly fee will be: {net_monthly_payment} DKK")

        elif self.user_inputs["app_mode"] == "Apartment price calculator":
            max_loan_rk = self._calculate_price(
                self.user_inputs["monthly_payment"],
                self.user_inputs["apy_realkredit"],
                self.user_inputs["loan_years"],
            )
            max_price_no_bank_loan = max_loan_rk + self.user_inputs["downpayment"]

            st.success(
                f"Your maximum budget without a bank loan is: {max_price_no_bank_loan} DKK"
            )

    def _calculate_price(
        self, monthly_payment: float, annual_interest_rate: float, loan_years: int
    ) -> float:
        return npf.pv(
            rate=annual_interest_rate / 12 / 100,
            nper=loan_years * 12,
            pmt=-1 * monthly_payment,
            fv=0,
        )

    def _calculate_monthly_payment(
        self, loan_amount: float, annual_interest_rate: float, loan_years: int
    ) -> float:
        return npf.pmt(
            rate=annual_interest_rate / 12 / 100,
            nper=loan_years * 12,
            pv=loan_amount,
            fv=0,
        )


def main():
    """
    The main function initiates a new calculator object and runs the app.
    """
    app = MortgageCalculatorApp()
    app.run()


if __name__ == "__main__":
    main()
