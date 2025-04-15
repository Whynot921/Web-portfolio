import sqlite3
import base64
class Fdatabase:
    def __init__(self, db):
        self.__db = db
        self.__cur = db.cursor()
        self.__cur.execute('''PRAGMA table_info(accounts)''')
        columns = [column[1] for column in self.__cur.fetchall()]
        self.lenData = len(columns)-2
    def get_data(self):
        try:
            self.__cur.execute('''SELECT * FROM accounts''')
            res = self.__cur.fetchall()
            result = {row1['username']: row1['password'] for row1 in res}
            return result
        except:
            print("Ошибка чтения дата базы")
        return []
    
    def add_data(self,username,password):
        try:
            self.__cur.execute('''INSERT INTO accounts VALUES(?,?,NULL)''',(username, password))
            self.__db.commit()
        except sqlite3.Error as e:
            print("Ошибка добавления данных" +str(e))
            return False, "Ошибка добавления данных" +str(e)
        return True, "Данные успешно добавлены"
    
    def add_file(self,username,files):
        try:
            self.lenData
            binary = sqlite3.Binary(files)
            for i in range(1,self.lenData+1):
                check = self.__cur.execute(f'''SELECT file{i} FROM accounts WHERE username=?''',(username,))
                if check.fetchone()[0] is None:
                    self.__cur.execute(f"UPDATE accounts SET file{i} = ? WHERE username=?",(binary, username))
                    self.__db.commit()
                    return 1
            self.__cur.execute(f'''ALTER TABLE accounts ADD COLUMN file{self.lenData+1} BLOB''')
            self.__db.commit()
            self.__cur.execute(f'''UPDATE accounts SET file{self.lenData+1}=? WHERE username=?''',(binary,username))
            self.__db.commit()

        except sqlite3.Error as e:
            print("Ошибка добавления данных "+str( e))
            return False
        return True

    def get_file(self,username,index=None):
        try:
            files = []
            for i in range(1,self.lenData+1):
                check = self.__cur.execute(f'''SELECT file{i} FROM accounts WHERE username=?''',(username,))
                if check.fetchone()[0] is not None:
                    sql = self.__cur.execute(f'''SELECT file{i} FROM accounts WHERE username=?''',(username,))
                    image = sql.fetchone()[0]
                    files.append(base64.b64encode(image).decode('utf-8'))
            return files
        except sqlite3.Error as e:
            print("Ошибка чтения данных "+str( e))
            return []
                
    def delete_file(self,imgnum,username):
        try:
            self.__cur.execute(f'''UPDATE accounts SET file{imgnum} = NULL WHERE username=?''',(username,))
            self.__db.commit()
        except sqlite3.Error as e:
            print('Ошибка удаления данных ' + str(e))
            return(False)
        return(True)
