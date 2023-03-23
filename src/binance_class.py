from binance.client import Client, BinanceAPIException
import pandas as pd

class Binance(object):
    obj = None
    client = None
    secret_key = None
    pub_key = None
    def __new__(cls, *args, **kwargs):
        if cls.obj is None:
            cls.obj = object.__new__(cls, *args, **kwargs)
        return cls.obj

    def __del__(self):
        try:
            self.client.close_connection()
        except BinanceAPIException as e:
            print(e.status_code)
            print(e.message)
    
    def set_secret_key(self, secret_key):
        self.secret_key = secret_key
        
    def set_pub_key(self, pub_key):
        self.pub_key = pub_key
    
    def create_connection(self):        
        try:
            self.client = Client(self.pub_key, self.secret_key)
        except BinanceAPIException as e:
            print(e.status_code)
            print(e.message)
            
    def get_futures_historical_klines(self, _symbol, _interval, _start_str, _end_str):
        
        try:
            hist = self.client.futures_historical_klines(
                symbol=_symbol,
                interval=_interval,
                start_str=_start_str,
                end_str=_end_str
            )
        except BinanceAPIException as e:
            print(e.status_code)
            print(e.message)
        finally:
            df = pd.DataFrame(hist)
            df = df.iloc[:, :6]
            df.columns = ['date', 'open', 'high', 'low', 'close', 'volume']
            df['date'] = pd.to_datetime(df['date'], unit='ms')
            for col in df.columns[1:]:
                df[col] = pd.to_numeric(df[col])
            print(df)
    
    def menu_binance(self):
        while(True):
            print("__________BINANCE MENU__________")
            print("1) Запустить скрипт")
            print("2) Получить текущии значения ETHUSDT и BTCUSDT")
            print("3) Выход")

            try:
                choise = input("Введите номер команды из меню: ")
                menu_num = int(choise)
                if menu_num == 1:
                    break
                elif menu_num == 2:
                    self.get_futures_historical_klines('BTCUSDT', '1d', '2021-06-01', '2021-06-30')
                    print("**************************************")
                    self.get_futures_historical_klines('ETHUSDT', '1d', '2021-06-01', '2021-06-30')
                elif menu_num == 3:                
                    break
                else:
                    print("Указанной команды нет в меню")
                    continue
            except ValueError as e:
                print(f"Ошибка {e}")
    
    def close_connection_client(self):
        try:
            self.client.close_connection()    
        except BinanceAPIException as e:
            print(e.status_code)
            print(e.message)
        except AttributeError as e:
            print(f"Value error: {e}")
        
