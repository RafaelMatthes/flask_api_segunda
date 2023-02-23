import mysql.connector

class MyDatabase:

    def __init__(self):
        try:
            self._db = mysql.connector.connect(
                host='localhost',
                database='apexalunos',
                user='admin',
                password='pass@1803'
            )
            self._cursor = self._db.cursor()
        except Exception as e:
            print(f"Erro ao conectar no banco de dados. error ")


class UserDatabase(MyDatabase):

    def __init__(self):
        super().__init__()

        self._create_table()

    def _create_table(self):

        query = (
            "CREATE TABLE IF NOT EXISTS user ("
            "id INT AUTO_INCREMENT PRIMARY KEY,"
            "username VARCHAR(255) NOT NULL UNIQUE,"
            "password VARCHAR(255) NOT NULL,"
            "created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP"
            ")  ENGINE=INNODB;"
        )
        self._cursor.execute(query)

    def insert(self, username, password):

        self._cursor.execute(
            "INSERT INTO user (username, password) VALUES (%s,%s)",
            (f"{username}",f"{password}" )
        )

        self._db.commit()

    def select(self, username):

        self._cursor.execute(f"SELECT * FROM user WHERE username = '{username}'")

        return self._cursor.fetchall()

    def update(self, id, username, password):
        self._cursor.execute(
            f"UPDATE user SET username='{username}', password='{password}' WHERE id = {id}"
        )

        self._db.commit()
