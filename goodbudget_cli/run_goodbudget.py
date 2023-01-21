import argparse
import getpass

from .utils.util import format_date, get_envelope_from_alias, parse_config
from .utils.driver import GbSeleniumDriver


def main():
    # Parser for login email
    parser = argparse.ArgumentParser()
    parser.add_argument("username", help="Username for Goodbudget", action="store")
    parser.add_argument("-g", "--use-gui", help="show the browser", action="store_true")
    args = parser.parse_args()

    # Get password
    gb_password = getpass.getpass(prompt="Enter your Goodbudget password: ")

    print("Logging in. Please wait...")

    gb_driver = GbSeleniumDriver(parse_config()["webdriver_path"], args.use_gui)
    gb_driver.log_in(args.username, gb_password)

    more_transactions = True
    while more_transactions:
        input_date = input("Date of transaction (today / yesterday / mm/dd/yyyy): ")
        formatted_date = format_date(input_date)
        input_payee = input("Payee: ")
        input_amount = input("Amount: ")
        input_envelope = input("Envelope: ")
        found_envelope = get_envelope_from_alias(input_envelope)
        input_notes = input("Notes (optional): ")

        summary_of_transaction = f"""
        Summary of your transcation:

            Date: {formatted_date}
            Payee: {input_payee}
            Amount: ${input_amount}
            Envelope: {found_envelope} (based on your alias of '{input_envelope}')
            Notes: {input_notes if input_notes else "<none>"}
        """
        print(summary_of_transaction)
        input_confirmation = input("Is everything correct? (Y/n) ")
        if input_confirmation.lower() not in ["y", "yes"]:
            print("Exiting the program.")
            quit()

        gb_driver.enter_transaction(
            formatted_date, input_payee, input_amount, found_envelope, input_notes
        )

        input_more_transactions = input(
            "Do you want to enter another transaction? (Y/n) "
        )
        if input_more_transactions.lower() not in ["y", "yes"]:
            more_transactions = False

    gb_driver.exit_driver()
