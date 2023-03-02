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

    def select(self, username=None, user_id=None):

        if username:
            self._cursor.execute(f"SELECT * FROM user WHERE username = '{username}'")
        else:
            self._cursor.execute(f"SELECT * FROM user WHERE id = {user_id}")

        return self._cursor.fetchall()

    def update(self, id, username, password):
        self._cursor.execute(
            f"UPDATE user SET username='{username}', password='{password}' WHERE id = {id}"
        )

        self._db.commit()


class TokenDatabase(MyDatabase):

    def __init__(self):
        super().__init__()

        self._create_table()

    def _create_table(self):

        query = (
            "CREATE TABLE IF NOT EXISTS token ("
            "id INT AUTO_INCREMENT PRIMARY KEY,"
            "code VARCHAR(255) NOT NULL UNIQUE,"
            "user_id INT NOT NULL,"
            "created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,"
            "FOREIGN KEY (user_id) REFERENCES user(id)"
            ") ENGINE=INNODB;"
        )
        self._cursor.execute(query)

    def insert(self, user_id, token_code):

        self._cursor.execute(
            "INSERT INTO token (code, user_id) VALUES (%s,%s)",
            (f"{token_code}",f"{user_id}")
        )

        self._db.commit()

    def select(self, token_code=None, user_id=None):

        if user_id:
            self._cursor.execute(f"SELECT * FROM token WHERE user_id = {user_id} ORDER BY created_at DESC")
        else:
            self._cursor.execute(f"SELECT * FROM token WHERE code = '{token_code}' ORDER BY created_at DESC")

        if user_id or token_code:
            return self._cursor.fetchall()

        raise ValueError("token ou user_id não informados")


