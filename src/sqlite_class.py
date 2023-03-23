import sqlite3
import os.path

class SQLConfig(object):
    obj = None
    connection = None
    cursor = None
    flag_sql_chenged = False
    def __new__(cls, *args, **kwargs):
        if cls.obj is None:
            cls.obj = object.__new__(cls, *args, **kwargs)
        return cls.obj

    def __del__(self):
        self.cursor.close()
        if (self.connection):
            self.connection.close()
            print("Соединение с SQLite закрыто")

    def get_secret_key(self):
        self.cursor.execute("SELECT Value FROM config WHERE ID = 'API secret key';")
        secret_key = self.cursor.fetchone()[0]
        return str(secret_key)
    
    def get_public_key(self):
        self.cursor.execute("SELECT Value FROM config WHERE ID = 'API key';")
        pub_key = self.cursor.fetchone()[0]
        return str(pub_key)

    def create_connection(self, path):
        if not os.path.exists(path):
            file = open("path", "a")
            file.close()
        try:
            self.connection = sqlite3.connect(path)
            self.cursor = self.connection.cursor()
            print("Connection to SQLite DB successful")
        except sqlite3.Error as e:
            print(f"The error '{e}' occurred")

    def fill_db(self):
        self.cursor.execute("CREATE TABLE IF NOT EXISTS config(ID TEXT, Value TEXT);")
        self.cursor.execute("SELECT count(*) FROM config;")
        if self.cursor.fetchone()[0] == 0:
            self.cursor.execute("INSERT INTO config(ID, Value) VALUES ('API secret key', 'NONE'),('API key', 'NONE'), ('Language', 'ru');")

    def view_table(self, table_name):
        self.cursor.execute(f"SELECT * FROM '{table_name}'")
        result_view = self.cursor.fetchall()
        for item in result_view:
            print(item[0], "\t", item[1])

    def update_data(self, table_name, id, value):
        self.cursor.execute(f"UPDATE '{table_name}' SET Value = '{value}' WHERE ID = '{id}';")
    
    def menu_db(self):
        self.flag_sql_chenged = False
        while(True):
            print("__________CONFIG MENU__________")
            print("1) Просмотр таблицы")
            print("2) Задать закрытй API ключ")
            print("3) Задать API ключ")
            print("4) Выйти в главное меню")
            menu_config_num = int(
                input("Введите номер команды из меню: "))
            if menu_config_num == 1:
                self.view_table("config")
            elif menu_config_num == 2:
                secret_key_new = input("Введите новый закрытый API ключ: ")
                self.update_data('config', 'API secret key',  secret_key_new)
                self.flag_sql_chenged = True
            elif menu_config_num == 3:
                key_new = input("Введите новый API ключ: ")
                self.update_data('config', 'API key', key_new)
                self.flag_sql_chenged = True
            elif menu_config_num == 4:
                if self.flag_sql_chenged:
                    save_flag = input(
                        "Сохранить изменения в таблицу config (y/n)? ")
                    if save_flag == "y":
                        self.connection.commit()
                    elif save_flag == "n":
                        break
                    else:
                        print("Введен неверный знак")
                break
            else:
                print("Указанной команды нет в меню")
                continue
