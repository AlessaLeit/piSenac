import mysql.connector
from mysql.connector import Error

class DBConnection:
    def __init__(self, host, database, user, password):
        self.host = host
        self.database = database
        self.user = user
        self.password = password
        self.connection = None

    def connect(self):
        try:
            self.connection = mysql.connector.connect(
                host=self.host,
                database=self.database,
                user=self.user,
                password=self.password
            )
            if self.connection.is_connected():
                print("Conexão ao banco de dados MySQL estabelecida com sucesso!")
        except Error as e:
            print(f"Erro ao conectar ao MySQL: {e}")

    def disconnect(self):
        if self.connection and self.connection.is_connected():
            self.connection.close()
            print("Conexão ao MySQL encerrada.")

    def execute_query(self, query, params=None, fetch_one=False, fetch_all=False):
        cursor = None
        result = None
        try:
            if not self.connection or not self.connection.is_connected():
                self.connect()
            cursor = self.connection.cursor(dictionary=True)
            cursor.execute(query, params)
            if query.strip().upper().startswith(("INSERT", "UPDATE", "DELETE")):
                self.connection.commit()
                result = cursor.rowcount
            elif fetch_one:
                result = cursor.fetchone()
            elif fetch_all:
                result = cursor.fetchall()
        except Error as e:
            print(f"Erro ao executar query: {e}")
            if self.connection:
                self.connection.rollback()
        finally:
            if cursor:
                cursor.close()
        return result

