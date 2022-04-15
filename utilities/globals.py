import os
dir_path = os.path.dirname(os.path.realpath(__file__))
parent_path = os.path.realpath(os.path.join(dir_path, '..'))
root_folder_all_code = f"{os.path.basename(parent_path)}/"


def generate_folders_if_not_exists(path_to_generate):
    if not os.path.exists(path_to_generate):
        os.makedirs(path_to_generate)


class websites:
    investing_dot_com = "https://www.investing.com"
    investing_title = "Investing.com"
    investing_screener = investing_dot_com + "/stock-screener"
    equities_website = investing_dot_com + u'/equities'
    yahoo = 'https://finance.yahoo.com/quote/'


class files:
    cookies = "cookies.pkl"
    historical_data_csv = "historial_data.csv"
    log = "status.log"


class folders:
    root_all_code = root_folder_all_code
    website_scraping = "website_scraping"
    investing_dot_com = "investing_dot_com"
    downloads = "downloads"
    backtesting_root = "backtesting"
    backtesting_data = "data_testing"
    etf_data = "etf_data"
    log = "logs"


class paths:
    _temp_current = os.path.dirname(os.path.realpath(__file__))
    dir_root = _temp_current.split(folders.root_all_code, 1)[0]
    code_root = os.path.join(dir_root, folders.root_all_code)

    downloads = os.path.join(code_root, folders.downloads)
    generate_folders_if_not_exists(downloads)

    _backtesting_root = os.path.join(code_root, folders.backtesting_root)
    backtesting_etf = os.path.join(_backtesting_root, folders.etf_data)

    _backtesting_data = os.path.join(_backtesting_root, folders.backtesting_data)
    generate_folders_if_not_exists(_backtesting_data)
    historical_data_csv = os.path.join(_backtesting_data, files.historical_data_csv)

    _log = os.path.join(code_root, folders.log)
    generate_folders_if_not_exists(_log)
    log = os.path.join(_log, files.log)

    website_scraping_path = os.path.join(code_root, folders.website_scraping)
    cookies = os.path.join(website_scraping_path, folders.investing_dot_com, files.cookies)
