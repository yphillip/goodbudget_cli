# goodbudget_cli

Command line tool to enter transactions into your [Goodbudget](https://goodbudget.com/) account.

## Installation
### Dependencies
- Selenium Chrome Webdriver ([example of installation instructions](https://cloudbytes.dev/snippets/run-selenium-and-chrome-on-wsl2))

### Clone and install
```
$ git clone git@github.com:yphillip/goodbudget_cli.git
$ pipx install ./goodbudget_cli
```
### Initialize and edit the configuration file
1. Run `gb` to initially create a `~/.config/goodbudget_cli/config.json` file.
2. Edit the `config.json` file to set the `webdriver_path` to the location of your Chrome webdriver.
3. Edit the `config.json` file to set the `Envelopes` using the name of your Goodbudget envelopes using the format of `{ENVELOPE_NAME: [LIST OF ALIASES]}`.
## Usage
```
$ gb {Goodbudget household username or email}
```

## Demo
```
$ gb foo@bar.com
Enter your Goodbudget password:
Logging in. Please wait...
Logged in.

Date of transaction (today / yesterday / mm/dd/yyyy): today
Payee: QFC
Amount: $40.00
Envelope (or type in 'remind'): groceries
Notes (optional):

        Summary of your transcation:

            Date: 01/20/2023
            Payee: QFC
            Amount: $40.00
            Envelope: Groceries (based on your alias of 'groceries')
            Notes: <none>

Is everything correct? (Y/n) Y
Success! Your transaction was entered into Goodbudget.

Do you want to enter another transaction? (Y/n) n

Thank you for using goodbudget_cli! See you next time!
```