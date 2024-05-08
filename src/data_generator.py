import pandas as pd
import numpy as np
import MetaTrader5 as mt5

from enum import Enum
from src.json_reader import JsonReader
from src.context_mt5 import ContextMT5

from datetime import datetime
from datetime import timedelta
from datetime import timezone

class DataGenerator():

    json_settings: JsonReader
    credentials: JsonReader
    symbol: str
    timeframe: str
    context_mt5: ContextMT5
    num_candlesticks: int
    num_ticks: int
    begin_timestamp: int
    end_timestamp: int
    candlesticks: pd.DataFrame
    

    def __init__(self, account_settings: str, credentials: str) -> None:
        self.json_settings = JsonReader(account_settings)
        self.credentials = JsonReader(credentials)
        self.symbol = self.json_settings.get_symbol()
        self.timeframe = self.json_settings.get_timeframe()
        self.context_mt5 = ContextMT5(self.credentials.get_json_data())

    def connect(self) -> bool:
        self.context_mt5.connect()
        return True
    
    def create_data_from_quantity(self, num_candlesticks: int) -> bool:
        candlesticks_df = self.get_candlesticks(num_candlesticks)
        ticks_df = self.get_ticks_from_candlesticks()
        self.create_candlesticks_csv(candlesticks_df)
        self.create_ticks_from_timestamp_csv(ticks_df)
        return True

    def create_data_from_timestamp(self, begin_timestamp: int, end_timestamp: int) -> bool:
        candlesticks_df = self.get_candlesticks_from_timestamp(begin_timestamp,end_timestamp)
        ticks_df = self.get_ticks_from_candlesticks()
        self.create_candlesticks_from_timestamp_csv(candlesticks_df)
        self.create_ticks_from_timestamp_csv(ticks_df)
        return True

    def get_candlesticks(self, num_candlesticks: int) -> pd.DataFrame:
        self.num_candlesticks = num_candlesticks
        mt5_timeframe = self.get_mt5_timeframe(self.timeframe)
        candlesticks = mt5.copy_rates_from_pos(self.symbol, mt5_timeframe, 0, num_candlesticks)
        self.candlesticks = pd.DataFrame(candlesticks)
        return self.candlesticks
    
    def get_candlesticks_from_timestamp(self, begin_timestamp, end_timestamp) -> pd.DataFrame:
        self.begin_timestamp = begin_timestamp
        self.end_timestamp = end_timestamp
        mt5_timeframe = self.get_mt5_timeframe(self.timeframe)
        candlesticks = mt5.copy_rates_range(self.symbol, mt5_timeframe,self.begin_timestamp, self.end_timestamp)
        self.candlesticks = pd.DataFrame(candlesticks)
        return self.candlesticks
    
    def get_ticks_from_candlesticks(self) -> pd.DataFrame:
        self.begin_timestamp = int(round(self.candlesticks.iloc[0]['time']))
        self.end_timestamp = int(round(self.candlesticks.iloc[-1]['time']))
        ticks = self.get_ticks_from_timestamp(self.begin_timestamp,self.end_timestamp)
        return ticks
    
    def get_ticks_from_timestamp(self, begin_timestamp, end_timestamp) -> pd.DataFrame:
        self.begin_timestamp = begin_timestamp
        self.end_timestamp = end_timestamp
        ticks = mt5.copy_ticks_range(self.symbol,self.begin_timestamp, self.end_timestamp, mt5.COPY_TICKS_ALL)
        return pd.DataFrame(ticks)
    
    def create_candlesticks_csv(self, df: pd.DataFrame) -> bool:
        path = f"mock/candlesticks_{self.symbol}_{self.num_candlesticks}_{self.get_date_time_now()}.csv"
        pd.DataFrame.to_csv(df, path)
        print(f"{path} has been created!")
        return True
    
    def create_candlesticks_from_timestamp_csv(self, df: pd.DataFrame) -> bool:
        path = f"mock/candlesticks_{self.symbol}_from_{self.begin_timestamp}_to_{self.end_timestamp}.csv"
        pd.DataFrame.to_csv(df, path)
        print(f"{path} has been created!")
        return True
    
    def create_ticks_from_timestamp_csv(self, df: pd.DataFrame) -> bool:
        path = f"mock/ticks_from_{self.symbol}_{self.begin_timestamp}_to_{self.end_timestamp}.csv"
        pd.DataFrame.to_csv(df, path)
        print(f"{path} has been created!")
        return True
        
    def get_date_time_now(self) -> str:
        offset = timedelta(hours=2.0)
        tz_UTC_offset = timezone(offset,'GMT')
        dt = datetime.now(tz_UTC_offset)
        format = '%Y-%m-%d-%H-%M-%S'
        dt_string = dt.strftime(format)
        return dt_string

    def get_mt5_timeframe(self, timeframe) -> str:
        try:
            return Timeframe[timeframe].value
        except KeyError as e:
            print(f"{timeframe} is not a legal timeframe. {e}")

    def get_context_mt5(self) -> ContextMT5:
        return self.context_mt5

class Timeframe(Enum):
    one_minute  = mt5.TIMEFRAME_M1
    two_minutes  = mt5.TIMEFRAME_M2
    three_minutes  = mt5.TIMEFRAME_M3
    four_minutes  = mt5.TIMEFRAME_M4
    five_minutes  = mt5.TIMEFRAME_M5
    six_minutes  = mt5.TIMEFRAME_M6
    ten_minutes = mt5.TIMEFRAME_M10
    twelve_minutes = mt5.TIMEFRAME_M12
    fifteen_minutes = mt5.TIMEFRAME_M15
    twenty_minutes = mt5.TIMEFRAME_M20
    thirty_minutes = mt5.TIMEFRAME_M30
    one_month = mt5.TIMEFRAME_MN1
    one_hour  = mt5.TIMEFRAME_H1
    two_hours  = mt5.TIMEFRAME_H2
    three_hours  = mt5.TIMEFRAME_H3
    four_hours  = mt5.TIMEFRAME_H4
    six_hours  = mt5.TIMEFRAME_H6
    eight_hours  = mt5.TIMEFRAME_H8
    one_day  = mt5.TIMEFRAME_D1


