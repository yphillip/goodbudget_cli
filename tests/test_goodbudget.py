import os
from datetime import datetime

import pytest

from goodbudget_cli.utils.driver import GbSeleniumDriver
from goodbudget_cli.utils.util import format_date, get_envelope_from_alias, parse_config


@pytest.fixture(scope="session")
def gb_driver():
    """Fixture for instantiated GbSeleniumDriver class"""
    driver = GbSeleniumDriver(parse_config()["webdriver_path"])
    user = os.getenv("gbemail")
    assert user, "Please set in your shell: export gbemail=<login email>"
    password = os.getenv("gbpw")
    assert password, "Please set in your shell: export gbpw=<login password>"
    driver.log_in(user, password)
    yield driver
    driver.exit_driver()


def test_add_expense(capsys, gb_driver):
    """Test of adding an expense"""
    now = datetime.now()
    date_time = now.strftime("%H:%M:%S")

    gb_driver.enter_expense(
        in_date=format_date("today"),
        in_payee=f"TEST_PAYEE {date_time}",
        in_amount="99.99",
        in_envelope=get_envelope_from_alias("pure fun"),
        in_notes="TEST_NOTE",
    )
    captured = capsys.readouterr()
    assert "Entering expense. Please wait..." in captured.out
    assert "Success! Your transaction was entered into Goodbudget." in captured.out


def test_add_income(capsys, gb_driver):
    """Test of adding an income"""
    now = datetime.now()
    date_time = now.strftime("%H:%M:%S")

    gb_driver.enter_income(
        in_date=format_date("today"),
        in_payer=f"TEST_PAYER {date_time}",
        in_amount="44.44",
        in_notes="TEST_NOTE",
    )
    captured = capsys.readouterr()
    assert "Entering income. Please wait..." in captured.out
    assert "Success! Your transaction was entered into Goodbudget." in captured.out
