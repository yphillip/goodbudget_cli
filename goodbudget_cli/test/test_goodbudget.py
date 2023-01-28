import os
from datetime import datetime

import pytest

from ..utils.driver import GbSeleniumDriver
from ..utils.util import format_date, get_envelope_from_alias, parse_config


@pytest.fixture(scope="session")
def gb_driver():
    """Fixture for instantiated GbSeleniumDriver class"""
    driver = GbSeleniumDriver(parse_config()["webdriver_path"])
    # Set this in your shell with export gbemail=<login email>
    user = os.getenv("gbemail")
    # Set this in your shell with export gbpw=<login password>
    password = os.getenv("gbpw")
    driver.log_in(user, password)
    yield driver
    driver.exit_driver()


def test_add_transaction(gb_driver):
    """Test of adding a transaction"""
    now = datetime.now()
    date_time = now.strftime("%H:%M:%S")

    gb_driver.enter_transaction(
        in_date=format_date("today"),
        in_payee=f"TEST_PAYEE {date_time}",
        in_amount="99.99",
        in_envelope=get_envelope_from_alias("pure fun"),
        in_notes="TEST_NOTE",
    )
