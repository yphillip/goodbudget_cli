import datetime
import json
import os
import pprint
import shutil
from pathlib import Path
from typing import Dict


def parse_config() -> Dict:
    """Parse the config.json, returns as dictionary."""
    config_json = Path("~/.config/goodbudget_cli/config.json").expanduser()
    f = open(config_json)
    data = json.load(f)
    return data


def check_config_json() -> None:
    """Create a config.json in ~/.config/goodbudget_cli if it doesn't exist"""
    config_json = Path("~/.config/goodbudget_cli/config.json").expanduser()
    if not os.path.exists(config_json):
        os.makedirs(config_json.parent, exist_ok=True)
        source = Path(__file__).parent.parent / "config.json"
        shutil.copyfile(source, config_json)
        print(f"WARNING! {config_json} was not found.")
        print("Don't worry, we made one for you.")
        print(
            f"Please go edit {config_json} to set your configuration settings,\n"
            "and then run `gb` again."
        )
        quit()


def format_date(input_date: str) -> str:
    """Format input date as mm/dd/yyyy."""
    if input_date.lower() == "today":
        current_day = datetime.date.today()
        formatted_date = datetime.date.strftime(current_day, "%m/%d/%Y")
    elif input_date.lower() == "yesterday":
        yesterday = datetime.date.today() - datetime.timedelta(days=1)
        formatted_date = datetime.date.strftime(yesterday, "%m/%d/%Y")
    else:
        assert input_date.count("/") == 2, "Format must be mm/dd/yyyy!"
        month, day, year = input_date.split("/")

        assert len(month) in [1, 2]
        if len(month) == 1:
            month = "0" + month
        assert len(day) in [1, 2]
        if len(day) == 1:
            day = "0" + day
        assert len(year) in [2, 4]
        if len(year) == 4:
            assert year.startswith("20")  # assuming it's 20XX
        if len(year) == 2:
            year = "20" + year

        formatted_date = "/".join([month, day, year])

    return formatted_date


def get_envelope_from_alias() -> str:
    """Determine the correct envelope given a alias."""
    envelopes_data = parse_config()["Envelopes"]

    input_phrase = input("Envelope (or type in 'remind'): ")

    if input_phrase.lower() == "remind":
        print("These are your available envelopes and their aliases:\n")
        pprint.pprint(envelopes_data, indent=4)
        print("\n")
        found_envelope = get_envelope_from_alias()
    else:
        # Match alias to envelope
        input_phrase = input_phrase.lower()
        found = False
        for envelope_name, aliases in envelopes_data.items():
            if input_phrase in aliases:
                found_envelope = envelope_name
                found = True
                break
        if not found:
            print(f"Could not determine which envelope {input_phrase} belongs to!")
            print("Please try again.\n")
            found_envelope = get_envelope_from_alias()

    return found_envelope
