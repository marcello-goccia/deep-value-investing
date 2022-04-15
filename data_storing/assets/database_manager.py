from utilities.common_methods import getDebugInfo

from data_storing.assets import tables
from data_storing.assets.database_connection import db_engine

from sqlalchemy.orm import sessionmaker
from utilities import log

dbSession = sessionmaker(bind=db_engine)
session = dbSession()


class DatabaseManager:
    def __init__(self):
        pass

    @staticmethod
    def commit_to_database():
        try:
            session.commit()
        except Exception as e:
            log.error(f"There is a problem in the code!: {e}\n{getDebugInfo()}")

    @staticmethod
    def add_to_database(item):
        try:
            session.add(item)
            session.commit()
        except Exception as e:
            log.error(f"There is a problem in the code!: {e}\n{getDebugInfo()}")

    @classmethod
    def insert_equity_into_asset(cls, **kwargs):
        try:
            manager = cls()

            symbol_1 = kwargs.get(u'symbol_1')
            exchange = kwargs.get(u'exchange', '')
            # query first if not exist, create otherwise.
            equity = manager.query_equity_by_symbol_1_and_exchange(symbol_1=symbol_1, exchange=exchange)
            if not equity:
                equity = tables.Equity(**kwargs)
                DatabaseManager.add_to_database(equity)
                manager.insert_fundamentals_into_asset(**kwargs)
                manager.insert_overview_into_asset(**kwargs)
            else:
                DatabaseManager.update_equity(equity, **kwargs)
            return equity

        except Exception as e:
            log.error(f"There is a problem in the code!: {e}\n{getDebugInfo()}")

    @staticmethod
    def update_equity(equity, **kwargs):
        try:
            equity.name = kwargs.get(u'name')
            equity.weblink_1 = kwargs.get(u'weblink_1')
            equity.sector = kwargs.get(u'sector')
            equity.industry = kwargs.get(u'industry')
            DatabaseManager.commit_to_database()
        except Exception as e:
            log.error(f"There is a problem in the code!: {e}\n{getDebugInfo()}")

    @classmethod
    def insert_overview_into_asset(cls, **kwargs):
        try:
            manager = cls()

            symbol_1 = kwargs.get(u'symbol_1')
            exchange = kwargs.get(u'exchange', '')

            equity = manager.query_equity_by_symbol_1_and_exchange(symbol_1=symbol_1, exchange=exchange)
            overview_entity = manager.add_overview_if_not_exists(equity)
            return overview_entity

        except Exception as e:
            log.error(f"There is a problem in the code!: {e}\n{getDebugInfo()}")

    @classmethod
    def insert_fundamentals_into_asset(cls, **kwargs):
        try:
            manager = cls()

            symbol_1 = kwargs.get(u'symbol_1')
            exchange = kwargs.get(u'exchange', '')

            equity = manager.query_equity_by_symbol_1_and_exchange(symbol_1=symbol_1, exchange=exchange)
            fundamentals_entity = manager.add_fundamentals_if_not_exists(equity)
            return fundamentals_entity

        except Exception as e:
            log.error(f"There is a problem in the code!: {e}\n{getDebugInfo()}")

    # @classmethod
    # def generate_fundamentals_for_equity(cls, equity, **kwargs):
    #     try:
    #         manager = cls()
    #
    #
    #         for field, value in kwargs.items():
    #             tables.fundamentals.add_single_element(fundamentals_entity, field, value)
    #
    #     except Exception as e:
    #         log.error(f"There is a problem in the code!: {e}\n{getDebugInfo()}")

    # ###### BALANCE SHEET STUFF
    @classmethod
    def create_balance_sheet_if_not_exists(cls, equity_id, **kwargs):
        try:
            manager = cls()

            equity = manager.query_equity_by_id(equity_id=equity_id)
            cls.add_fundamentals_if_not_exists(equity)

            # look if the balance sheet with period_length period_ending is present. if not do not add.
            balance_sheet = session.query(tables.BalanceSheet).filter_by(equity_id=equity_id,
                                                                         period_length=kwargs.get(u'period_length'),
                                                                         period_ending=kwargs.get(u'period_ending')
                                                                         ).one_or_none()

            if not balance_sheet:
                balance_sheet = tables.BalanceSheet(equity_id=equity.id, fundamentals_id=equity.fundamentals.id,
                                                    **kwargs)
                equity.fundamentals.balance_sheet.append(balance_sheet)
                return balance_sheet
            else:
                return False

        except Exception as e:
            log.error(f"There is a problem in the code!: {e}\n{getDebugInfo()}")

    @classmethod
    def insert_balance_sheet_into_asset(cls, equity_id, **kwargs):
        try:
            balance_sheet = cls.create_balance_sheet_if_not_exists(equity_id, **kwargs)
            if balance_sheet:
                session.commit()
            return balance_sheet
        except Exception as e:
            log.error(f"There is a problem in the code!: {e}\n{getDebugInfo()}")

    # ###### INCOME STATEMTENT STUFF
    @classmethod
    def create_income_statement_if_not_exists(cls, equity_id, **kwargs):
        try:
            manager = cls()

            equity = manager.query_equity_by_id(equity_id=equity_id)
            cls.add_fundamentals_if_not_exists(equity)

            # look if the income statement with period_length period_ending is present. if not do not add.
            income_statement = \
                session.query(
                    tables.IncomeStatement).filter_by(equity_id=equity_id,
                                                      period_length=kwargs.get(u'period_length'),
                                                      period_ending=kwargs.get(u'period_ending')).one_or_none()
            if not income_statement:
                income_statement = tables.IncomeStatement(equity_id=equity.id, fundamentals_id=equity.fundamentals.id,
                                                          **kwargs)
                equity.fundamentals.income_statement.append(income_statement)
                return income_statement
            else:
                return False

        except Exception as e:
            log.error(f"There is a problem in the code!: {e}\n{getDebugInfo()}")

    @classmethod
    def insert_income_statement_into_asset(cls, equity_id, **kwargs):
        try:
            income_statement = cls.create_income_statement_if_not_exists(equity_id, **kwargs)
            if income_statement:
                session.commit()
            return income_statement
        except Exception as e:
            log.error(f"There is a problem in the code!: {e}\n{getDebugInfo()}")

    # ###### CLASH FLOW STUFF
    @classmethod
    def create_cash_flow_if_not_exists(cls, equity_id, **kwargs):
        try:
            manager = cls()

            equity = manager.query_equity_by_id(equity_id=equity_id)
            cls.add_fundamentals_if_not_exists(equity)

            # look if the cash flow with period_length period_ending is present. if not do not add.
            cash_flow = session.query(tables.CashFlow).filter_by(equity_id=equity_id,
                                                                 period_length=kwargs.get(u'period_length'),
                                                                 period_ending=kwargs.get(u'period_ending')
                                                                 ).one_or_none()
            if not cash_flow:
                cash_flow = tables.CashFlow(equity_id=equity.id, fundamentals_id=equity.fundamentals.id, **kwargs)
                equity.fundamentals.cash_flow.append(cash_flow)
                return cash_flow
            else:
                return False

        except Exception as e:
            log.error(f"There is a problem in the code!: {e}\n{getDebugInfo()}")

    @classmethod
    def insert_cash_flow_into_asset(cls, equity_id, **kwargs):
        try:
            cash_flow = cls.create_cash_flow_if_not_exists(equity_id, **kwargs)
            if cash_flow:
                session.commit()
            return cash_flow
        except Exception as e:
            log.error(f"There is a problem in the code!: {e}\n{getDebugInfo()}")

    # ###### RATIOS STUFF
    @classmethod
    def create_ratios_if_not_exists(cls, equity_id, **kwargs):
        try:
            manager = cls()

            equity = manager.query_equity_by_id(equity_id=equity_id)
            cls.add_fundamentals_if_not_exists(equity)

            # look if the cash flow with period_length period_ending is present. if not do not add.
            ratios = session.query(tables.Ratios).filter_by(equity_id=equity_id,
                                                            current_period=kwargs.get(u'current_period'),
                                                            benchmark=kwargs.get(u'benchmark')).one_or_none()
            if not ratios:
                ratios = tables.Ratios(equity_id=equity.id, fundamentals_id=equity.fundamentals.id, **kwargs)
                equity.fundamentals.ratios.append(ratios)
            return ratios

        except Exception as e:
            log.error(f"There is a problem in the code!: {e}\n{getDebugInfo()}")

    @classmethod
    def insert_ratios_into_asset(cls, equity_id, **kwargs):
        try:
            ratios = cls.create_ratios_if_not_exists(equity_id, **kwargs)
            session.commit()
            return ratios
        except Exception as e:
            log.error(f"There is a problem in the code!: {e}\n{getDebugInfo()}")

    # ###### DIVIDEND STUFF
    @classmethod
    def create_dividend_if_not_exists(cls, equity_id, **kwargs):
        try:
            manager = cls()

            equity = manager.query_equity_by_id(equity_id=equity_id)
            cls.add_fundamentals_if_not_exists(equity)

            # look if the divident with ex dividend date is present. if it does, do not add.
            dividend = \
                session.query(
                    tables.Dividends).filter_by(equity_id=equity_id,
                                                ex_dividend_date=kwargs.get(u'ex_dividend_date')).one_or_none()
            if not dividend:
                dividend = tables.Dividends(equity_id=equity.id, fundamentals_id=equity.fundamentals.id, **kwargs)
                equity.fundamentals.dividends.append(dividend)
            else:
                return False
            return dividend

        except Exception as e:
            log.error(f"There is a problem in the code!: {e}\n{getDebugInfo()}")

    @classmethod
    def insert_dividend_into_asset(cls, equity_id, **kwargs):
        try:
            dividend = cls.create_dividend_if_not_exists(equity_id, **kwargs)
            if not dividend:
                return False
            session.commit()
            return dividend
        except Exception as e:
            log.error(f"There is a problem in the code!: {e}\n{getDebugInfo()}")

    # ###### earning STUFF
    @classmethod
    def create_earning_if_not_exists(cls, equity_id, **kwargs):
        try:
            manager = cls()

            equity = manager.query_equity_by_id(equity_id=equity_id)
            cls.add_fundamentals_if_not_exists(equity)

            # look if the earning with release date is present. if it does, do not add.
            earning = session.query(tables.Earnings).filter_by(equity_id=equity_id,
                                                               release_date=kwargs.get(u'release_date')
                                                               ).one_or_none()
            if not earning:
                earning = tables.Earnings(equity_id=equity.id, fundamentals_id=equity.fundamentals.id, **kwargs)
                equity.fundamentals.earnings.append(earning)
                return earning
            elif earning.eps is None or earning.revenue is None:
                earning.eps = kwargs.get(u'eps')
                earning.revenue = kwargs.get(u'revenue')
                return earning
            else:
                return False

        except Exception as e:
            log.error(f"There is a problem in the code!: {e}\n{getDebugInfo()}")

    @classmethod
    def insert_earning_into_asset(cls, equity_id, **kwargs):
        try:
            earning = cls.create_earning_if_not_exists(equity_id, **kwargs)
            if not earning:
                return False
            session.commit()
            return earning
        except Exception as e:
            log.error(f"There is a problem in the code!: {e}\n{getDebugInfo()}")

    # ###### price (historical data) STUFF
    @classmethod
    def create_price_if_not_exists(cls, equity_id, **kwargs):
        try:
            manager = cls()

            equity = manager.query_equity_by_id(equity_id=equity_id)
            cls.add_fundamentals_if_not_exists(equity)

            price = session.query(tables.Prices).filter_by(equity_id=equity_id, day=kwargs.get(u'day')).one_or_none()

            if not price:
                price = tables.Prices(equity_id=equity.id, **kwargs)
                equity.prices.append(price)
            return price

        except Exception as e:
            log.error(f"There is a problem in the code!: {e}\n{getDebugInfo()}")

    @classmethod
    def insert_price_into_asset(cls, equity_id, **kwargs):
        try:
            price = cls.create_price_if_not_exists(equity_id, **kwargs)
            session.commit()
            return price
        except Exception as e:
            log.error(f"There is a problem in the code!: {e}\n{getDebugInfo()}")

    # ###### OVERVIEW EQUITY
    @staticmethod
    def add_overview_if_not_exists(equity):
        try:
            if equity.overview is None:
                overview = tables.Overview(equity_id=equity.id)
                equity.overview = overview
                session.commit()
                return overview
            else:
                return None
        except Exception as e:
            log.error(f"There is a problem in the code!: {e}\n{getDebugInfo()}")

    # ###### FUNDAMENTAL DATA STUFF
    @staticmethod
    def add_fundamentals_if_not_exists(equity):
        try:
            if equity.fundamentals is None:
                fundamentals = tables.Fundamentals(equity_id=equity.id)
                equity.fundamentals = fundamentals
                session.commit()
                return fundamentals
            else:
                return None
        except Exception as e:
            log.error(f"There is a problem in the code!: {e}\n{getDebugInfo()}")

    @staticmethod
    def query_all_equities():
        try:
            return session.query(tables.Equity).all()
        except Exception as e:
            log.error(f"There is a problem in the code!: {e}\n{getDebugInfo()}")

    @staticmethod
    def query_all_equities_by(**kwargs):
        try:
            return session.query(tables.Equity).filter_by(**kwargs).all()
        except Exception as e:
            log.error(f"There is a problem in the code!: {e}\n{getDebugInfo()}")

    @staticmethod
    def query_equity_by_sector(sector):
        try:
            return session.query(tables.Equity).filter_by(sector=sector).all()
        except Exception as e:
            log.error(f"There is a problem in the code!: {e}\n{getDebugInfo()}")

    @staticmethod
    def query_equity_by_symbol_1_and_exchange(symbol_1, exchange):
        """
        @function query_equity_by_symbol_1_and_exchange
        To get the correct equity need to query from database by using the symbol and the stock exchange name.
        :param symbol_1:
        :param exchange:
        """
        try:
            return session.query(tables.Equity).filter_by(symbol_1=symbol_1, exchange=exchange).one_or_none()
        except Exception as e:
            log.error(f"There is a problem in the code!: {e}\n{getDebugInfo()}")

    @staticmethod
    def query_equity_by_symbol_2_and_exchange(symbol_2, exchange):
        """
        @function query_equity_by_symbol_2_and_exchange
        To get the correct equity need to query from database by using the symbol and the stock exchange name.
        :param symbol_2:
        :param exchange:
        """
        try:
            return session.query(tables.Equity).filter_by(symbol_2=symbol_2, exchange=exchange).one_or_none()
        except Exception as e:
            log.error(f"There is a problem in the code!: {e}\n{getDebugInfo()}")

    @staticmethod
    def query_equity_by_id(equity_id):
        """
        @function query_equity_by_symbol
        To get the correct equity need to query from database by using the database id of the equity
        @param equity_id the id of the equity
        """
        try:
            return session.query(tables.Equity).filter_by(id=equity_id).one_or_none()
        except Exception as e:
            log.error(f"There is a problem in the code!: {e}\n{getDebugInfo()}")

    @staticmethod
    def query_equity_by_valuable_company():
        """
        @function query_equity_by_valuable_company
        Returns all the equities that are marked as valuable companies
        """
        try:
            valuable_companies = session.query(tables.Overview).filter_by(valuable_company=1).all()
            companies = []
            for company in valuable_companies:
                companies.append(session.query(tables.Equity).filter_by(id=company.equity_id).one_or_none())
            return companies

        except Exception as e:
            log.error(f"There is a problem in the code!: {e}\n{getDebugInfo()}")

    @staticmethod
    def delete_equity_from_database(symbol):
        try:
            item = session.query(tables.Equity).filter_by(symbol_1=symbol).one_or_none()
            if item is not None:
                session.delete(item)
                session.commit()
        except Exception as e:
            log.error(f"There is a problem in the code!: {e}\n{getDebugInfo()}")

    @staticmethod
    def delete_equity_by(**kwargs):
        try:
            item = session.query(tables.Equity).filter_by(**kwargs).one_or_none()
            if item is not None:
                session.delete(item)
                session.commit()
        except Exception as e:
            log.error(f"There is a problem in the code!: {e}\n{getDebugInfo()}")

    @staticmethod
    def delete_list_of_items(items):
        try:
            if items:
                for item in items:
                    session.delete(item)
                session.commit()
        except Exception as e:
            log.error(f"There is a problem in the code!: {e}\n{getDebugInfo()}")

    @staticmethod
    def delete_item(item):
        try:
            session.delete(item)
            session.commit()
        except Exception as e:
            log.error(f"There is a problem in the code!: {e}\n{getDebugInfo()}")

    @staticmethod
    def print_all_data(table='', query=''):
        try:
            query = query if query != '' else f"SELECT * FROM '{table}';"
            print(query)
            with db_engine.connect() as connection:
                try:
                    result = connection.execute(query)
                except Exception as e:
                    print(e)
                else:
                    for row in result:
                        print(row)  # print(row[0], row[1], row[2])
                    result.close()
            print("\n")

        except Exception as e:
            log.error(f"There is a problem in the code!: {e}\n{getDebugInfo()}")

    @staticmethod
    def add_not_found_page_to_equity(equity):
        item = tables.ItemEquity(equity_id=equity.id, field='link_problems', type='string', value_str='True')
        equity.item_equity.append(item)
        session.commit()
