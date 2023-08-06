from qttp.tools.filter import filter_spec
from qttp.tools.data_preprocessing import shift_data

import numpy as np

class BackTest_01:
    '''
    This backtest is ror that is indicator value
    '''
    def __init__(self, args):

        # dataframe date filter
        self.df = args['df']
        self.start_date = args['start_date']µ
        self.end_date = args['end_date']

        # buy conditions attributes
        self.buy_features = args['buy_features']
        self.buy_min = args['buy_min']
        self.buy_max = args['buy_max']

        # sell conditions attributes
        self.sell_features = args['sell_features']
        self.sell_min = args['sell_min']
        self.sell_max = args['sell_max']

        # ror information
        self.fee = args['fee']


    def run(self, chart=False, csv_save=False):
        df = self.__preprocessing(self.df)
        df = self.__min_max(df)
        df = self.__ror_hpr(df)
        if csv_save:
            df.to_csv('abc.csv')


    def __preprocessing(self, df):

        df = df.loc[self.start_date:self.end_date, :].copy()

        df = filter_spec(df, self.buy_features, self.buy_min, self.buy_max,
                         'buy_signal', 1)

        df = filter_spec(df, self.sell_features, self.sell_min, self.sell_max,
                         'sell_signal', 1)

        return df

    def __min_max(self, df):
        take_day = []
        turn = 0
        try:
            for i in range(df.shape[0]):
                buy_signal = df.loc[df.index[i], 'buy_signal']
                sell_signal = df.loc[df.index[i], 'sell_signal']
                order = df.index[i]

                if turn == 0 and buy_signal == 1:
                    df.loc[order, 'buy'] = 1
                    buy_price = df.loc[order, 'open']
                    turn = 1

                if turn == 1 and buy_signal == 1:
                    df.loc[df.index[i+1], 'buy'] = np.nan

                if turn == 1 and sell_signal == 1:
                    df.loc[order, 'sell'] = 1
                    df.loc[order, 'ror'] = df.loc[order, 'close']/buy_price-self.fee
                    turn = 0
        except:
            pass

        return df

    def __ror_hpr(self, df):
        df['ror'].fillna(1, inplace=True)
        df.loc[:, 'hpr'] = df['ror'].cumprod()
        hpr = round(df.iloc[-1, -1], 2)
        trading_count = df.loc[:, 'buy'].sum()
        total_day = df.shape[0]
        trading_ratio = round(df.loc[:, 'buy'].sum() / df.shape[0]* 100, 2)
        text = (
            f"hpr: {hpr}배, trading_count: {trading_count}개, "
            f"total_day: {total_day}일, trading_ratio: {trading_ratio}%"
        )
        print(text)

        return df

class BackTest_02:
    '''
    This backtest is ror that is designated
    '''
    def __init__(self, args):
        # dataframe date filter
        self.df = args['df']
        self.start_date = args['start_date']
        self.end_date = args['end_date']

        # buy conditions attributes
        self.buy_features = args['buy_features']
        self.buy_min = args['buy_min']
        self.buy_max = args['buy_max']

        # ror information
        self.fee = args['fee']
        self.set_ror = args['set_ror']

    def run(self, chart=False, csv_save=False):
        df = self.__preprocessing(self.df)
        df = self.__designated_ror(df)
        df = self.__ror_hpr(df)
        if csv_save:
            df.to_csv('abc.csv')
            df.to_csv('abc.csv')

    def __preprocessing(self, df):

        df = df.loc[self.start_date:self.end_date, :].copy()

        df = filter_spec(df, self.buy_features, self.buy_min, self.buy_max,
                         'buy_signal', 1)

        return df

    def __designated_ror(self, df):
        take_day = []
        turn = 0
        try:
            for i in range(df.shape[0]):
                buy_signal = df.loc[df.index[i], 'buy_signal']
                order = df.index[i]

                if turn == 0 and buy_signal == 1:
                    df.loc[order, 'buy'] = 1
                    buy_price = df.loc[order, 'open']
                    day = i
                    turn = 1

                if turn == 1 and buy_signal == 1:
                    df.loc[df.index[i+1], 'buy'] = np.nan

                if turn == 1 and df.loc[order, 'high'] / buy_price > self.set_ror:
                    df.loc[order, 'sell'] = 1
                    df.loc[order, 'ror'] = self.set_ror - self.fee
                    take_day.append(i - day)
                    turn = 0

                if df.loc[order, 'low'] / buy_price < 0.5 and turn == 1:
                    df.loc[order, 'danger'] = 1

        except:
            pass
        print(take_day)
        print(len(take_day))

        return df

    def __ror_hpr(self, df):
        df['ror'].fillna(1, inplace=True)
        df.loc[:, 'hpr'] = df['ror'].cumprod()
        hpr = round(df.iloc[-1, -1], 2)
        trading_count = df.loc[:, 'buy'].sum()
        total_day = df.shape[0]
        trading_ratio = round(df.loc[:, 'buy'].sum() / df.shape[0]* 100, 2)
        text = (
            f"hpr: {hpr}배, trading_count: {trading_count}개, "
            f"total_day: {total_day}일, trading_ratio: {trading_ratio}%"
        )
        print(text)

        return df
