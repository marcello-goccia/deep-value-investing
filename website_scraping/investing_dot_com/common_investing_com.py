class InvestingPages:

    # to append to the equity link
    profile = "-company-profile"
    financial = "-financial-summary"
    income_statement = "-income-statement"
    balance_sheet = "-balance-sheet"
    cash_flow = "-cash-flow"
    ratios = "-ratios"
    dividends = "-dividends"
    earnings = "-earnings"

    technical = "-technical"
    prices = "-historical-data"

    financial_locators = [
        {'tag': 'div', 'attrib': 'id', 'name': 'rrtable'},
        {'tag': 'div', 'attrib': 'id', 'name': 'rrTable'},
        {'tag': 'table', 'attrib': 'class', 'name': 'genTbl reportTbl'},
    ]

    ratios_locators = [
        {'tag': 'table', 'attrib': 'id', 'name': 'rrTable'},
        {'tag': 'table', 'attrib': 'class', 'name': 'genTbl reportTbl ratioTable'},
    ]

    dividends_locators = [
        {'tag': 'table', 'attrib': 'id', 'name': 'dividendsHistoryData'},
    ]

    prices_locators = [
        {'tag': 'table', 'attrib': 'id', 'name': 'curr_table'},
        {'tag': 'table', 'attrib': 'class', 'name': 'genTbl closedTbl historicalTbl'},
        {'tag': 'div', 'attrib': 'id', 'name': 'results_box'},
    ]

class Timers:
    page_load_timeout = 5
    times_getting_url = 3

    times_cliking_on_links = 3
    times_clicking_on_button = 5

    waiting = 0.5       # seconds
    waiting_short = 0.2
    waiting_medium = 1
    webdriver_wait = 3  # seconds

    atomical_sleep = 0.1    # units
    times_loop_to_load_page = 40
    times_loop_to_load_page_appears_part_of_text = 20
    times_loop_to_load_page_appears_table = 20

    wait_appears_attribute = 3      # seconds



