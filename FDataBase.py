import sqlite3


class FDataBase:
    def __init__(self, db):
        self.__db = db
        self.__cur = db.cursor()

    def getUsersTable(self):
        sql = '''SELECT * FROM users'''
        try:
            self.__cur.execute(sql)
            res = self.__cur.fetchall()
            if res:
                return res
        except:
            print("Ошибка чтения из БД")
        return []

    def addUser(self, username, email, hash_password):
        try:
            self.__cur.execute(f"SELECT COUNT() as 'count' FROM users WHERE username LIKE '{username}'")
            res = self.__cur.fetchone()
            if res['count'] > 0:
                print('Username already exist')
                return False, "username"
            self.__cur.execute(f"SELECT COUNT() as 'count' FROM users WHERE email LIKE '{email}'")
            res = self.__cur.fetchone()
            if res['count'] > 0:
                print('Email already exist')
                return False, "email"
            self.__cur.execute("INSERT INTO users VALUES(NULL, ?, ?, ?)", (username, email, hash_password))
            self.__db.commit()
        except sqlite3.Error as e:
            print('Insert user error ' + str(e))
            return False, "error"

        return True, "good"

    def addResult(self, username, email, time, blob_file, proteins, peptides):
        try:
            self.__cur.execute("INSERT INTO searchResults VALUES(NULL, ?, ?, ?, ?, ?, ?)",
                               (username, email, time, blob_file, peptides, proteins))
            self.__db.commit()
        except sqlite3.Error as e:
            print('Insert result error ' + str(e))
            return False, "error"

        return True

    def getSearchResult(self, username, email):
        try:
            print(username, email)
            self.__cur.execute(f"SELECT tm, proteins, peptides FROM searchResults WHERE username = '{username}' AND email = '{email}'")
            time = self.__cur.fetchall()
            if not time:
                print("User no have result")
                return False
            return time #, files
        except sqlite3.Error as e:
            print(e)

    def getfile(self, email, date):
        try:
            self.__cur.execute(f"SELECT file FROM searchResults WHERE tm = '{date}' AND email = '{email}'")
            files = self.__cur.fetchall()
            date = date.replace(' ', '').replace(':', '')
            if len(files) > 0:
                _file = open(f"uploads/outputs/{date}.zip", 'wb')
                _file.write(files[0][0])
                _file.close()
        except Exception as ex:
            print(ex)

    def remove_result(self, email, date):
        try:
            self.__cur.execute(f"DELETE FROM searchResults WHERE tm = '{date}' AND email = '{email}'")
            self.__db.commit()
        except sqlite3.Error as e:
            print('Insert result error ' + str(e))
            return False, "error"
        return True

    def getUser(self, user_id):
        try:
            self.__cur.execute(f"SELECT * FROM users WHERE id = '{user_id}' LIMIT 1")
            res = self.__cur.fetchone()
            if not res:
                print("User not exist")
                return False
            return res
        except sqlite3.Error as e:
            print(e)

        return False

    def getUserByEmail(self, email):
        try:
            self.__cur.execute(f"SELECT * FROM users WHERE email = '{email}' LIMIT 1")
            res = self.__cur.fetchone()
            if not res:
                print("User not exist")
                return False
            return res
        except sqlite3.Error as e:
            print(e)

        return False

    def getUserByName(self, username):
        try:
            self.__cur.execute(f"SELECT * FROM users WHERE username = '{username}' LIMIT 1")
            res = self.__cur.fetchone()
            if not res:
                print("User not exist")
                return False
            return res
        except sqlite3.Error as e:
            print(e)

        return False

