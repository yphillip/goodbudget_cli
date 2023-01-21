import argparse
import getpass

from .utils.driver import GbSeleniumDriver
from .utils.util import format_date, get_envelope_from_alias, parse_config


def main():
    # Parser for login email
    parser = argparse.ArgumentParser()
    parser.add_argument("username", help="Username for Goodbudget", action="store")
    parser.add_argument("-g", "--use-gui", help="show the browser", action="store_true")
    args = parser.parse_args()

    # Get password
    gb_password = getpass.getpass(prompt="Enter your Goodbudget password: ")

    # Log in
    print("Logging in. Please wait...")
    gb_driver = GbSeleniumDriver(parse_config()["webdriver_path"], args.use_gui)
    gb_driver.log_in(args.username, gb_password)

    # Allow user to keep adding new transactions until they're done
    more_transactions = True
    while more_transactions:
        input_date = format_date(
            input("Date of transaction (today / yesterday / mm/dd/yyyy): ")
        )
        input_payee = input("Payee: ")
        input_amount = input("Amount: ")
        # TODO: allow user to see what envelopes/aliases are available
        input_envelope = get_envelope_from_alias(input("Envelope: "))
        input_notes = input("Notes (optional): ")

        summary_of_transaction = f"""
        Summary of your transcation:

            Date: {input_date}
            Payee: {input_payee}
            Amount: ${input_amount}
            Envelope: {input_envelope} (based on your alias of '{input_envelope}')
            Notes: {input_notes if input_notes else "<none>"}
        """
        print(summary_of_transaction)
        input_confirmation = input("Is everything correct? (Y/n) ")
        if input_confirmation.lower() not in ["y", "yes"]:
            print("Exiting the program.")
            quit()

        gb_driver.enter_transaction(
            input_date, input_payee, input_amount, input_envelope, input_notes
        )

        input_more_transactions = input(
            "Do you want to enter another transaction? (Y/n) "
        )
        if input_more_transactions.lower() not in ["y", "yes"]:
            more_transactions = False

    gb_driver.exit_driver()
