import argparse
import getpass
import sys

from .utils.driver import GbSeleniumDriver
from .utils.util import (
    check_config_json,
    format_date,
    get_envelope_from_alias,
    parse_config,
)


def main():
    """Main entry point for running goodbudget_cli."""
    # initialize .config/goodbudget_cli/config.json
    check_config_json()

    # Parser for login email
    parser = argparse.ArgumentParser()
    parser.add_argument("username", help="Username for Goodbudget", action="store")
    parser.add_argument("-i", "--income", help="enter income mode", action="store_true")
    parser.add_argument("-g", "--use-gui", help="show the browser", action="store_true")
    parser.add_argument(
        "-s",
        "--screenshot",
        help="save screenshot at the end of the session",
        action="store_true",
    )
    args = parser.parse_args()

    # Three attempts to log in with the correct password
    log_in_successful = False
    gb_driver = None
    for _ in range(3):
        gb_password = getpass.getpass(prompt="Enter your Goodbudget password: ")
        print("Logging in. Please wait...")
        if gb_driver is None:
            gb_driver = GbSeleniumDriver(
                parse_config()["webdriver_path"], args.use_gui, args.screenshot
            )
        if gb_driver.log_in(args.username, gb_password):
            log_in_successful = True
            break
        else:
            print("Incorrect password. Please try again.")

    if not log_in_successful:
        print("Too many incorrect password attempts. Exiting now.")
        gb_driver.exit_driver()
        sys.exit()

    # Allow user to keep adding new transactions until they're done
    more_transactions = True
    while more_transactions:
        input_date = format_date(
            input("Date of transaction (today / yesterday / mm/dd/yyyy): ")
        )
        if not args.income:
            input_payee = input("Payee: ")
        else:
            input_payer = input("Payer: ")
        input_amount = input("Amount: ")
        if not args.income:
            input_envelope = None
            while not input_envelope:
                input_alias = input("Envelope (or type in 'remind'): ")
                input_envelope = get_envelope_from_alias(input_alias)
        input_notes = input("Notes (optional): ")

        if not args.income:
            summary_of_transaction = f"""
        Summary of your expense:

            Date: {input_date}
            Payee: {input_payee}
            Amount: ${input_amount}
            Envelope: {input_envelope} (based on your alias of '{input_alias}')
            Notes: {input_notes if input_notes else "<none>"}
        """
        else:
            summary_of_transaction = f"""
        Summary of your income:

            Date: {input_date}
            Payer: {input_payer}
            Amount: ${input_amount}
            Notes: {input_notes if input_notes else "<none>"}
        """
        print(summary_of_transaction)
        input_confirmation = input("Is everything correct? (Y/n) ")
        if input_confirmation.lower() not in ["y", "yes"]:
            print("Whoops. Please try entering your transaction again.\n")
            continue

        if not args.income:
            gb_driver.enter_expense(
                input_date, input_payee, input_amount, input_envelope, input_notes
            )
        else:
            gb_driver.enter_income(input_date, input_payer, input_amount, input_notes)

        input_more_transactions = input(
            "Do you want to enter another transaction? (Y/n) "
        )
        if input_more_transactions.lower() not in ["y", "yes"]:
            more_transactions = False

    gb_driver.exit_driver()
