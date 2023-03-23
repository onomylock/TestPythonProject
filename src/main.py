from binance_class import Binance
from sqlite_class import SQLConfig

def menu():
    binance = Binance()
    conf = SQLConfig()
    conf.create_connection("../res/config.db")
    conf.fill_db()
    
    binance.set_pub_key(conf.get_public_key())
    binance.set_secret_key(conf.get_secret_key())
    
    while(True):
        print("__________CONFIG MENU__________")
        print("1) Настройки Binance API")
        print("2) Настройка конфигурации")
        print("3) Выход")
        
        try:
            choise = input("Введите номер команды из меню: ")
            menu_num = int(choise)
            if menu_num == 1:
                binance.create_connection()
                binance.menu_binance()
            elif menu_num == 2:
                conf.flag_sql_chenged = False
                conf.menu_db()
                if conf.flag_sql_chenged:
                    binance.close_connection_client()
                    binance.set_pub_key(conf.get_public_key())
                    binance.set_secret_key(conf.get_secret_key())
                    #binance.create_connection()
            elif menu_num == 3:                
                break
            else:
                print("Указанной команды нет в меню")
                continue
        except ValueError as e:
            print(f"Ошибка {e}")


def main():
    menu()

if __name__ == '__main__':
    main()


