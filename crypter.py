import os
import json
import psycopg2
import pyAesCrypt
from io import BytesIO


class Crypter:
    def __init__(self, path: str) -> None:
        self.path = path
        self.login = None
        self.password = None
        self.buffersize = 64 * 1024
        self.sequence_bytes = BytesIO()


    def write_to_db(self,login=None):
        try:
            conn = psycopg2.connect(dbname='testdb',user='postgres',password='12345',host='localhost')
            cursor =conn.cursor()
            cursor.execute('select  login from users where login=%s;',(login,))
            result = cursor.fetchall()
            if result:
                return result[0][0]
            else:
                cursor.execute("INSERT INTO users(login) VALUES(%s)",(login,))
        except Exception as err:
            print(err)
        finally:
            conn.commit()
            cursor.close()
            conn.close()        

    def create_password(self):
        while True:
            self.login = input("create your login ...")
            password = input("please create password ...")
            repeat_password = input("repeat password ...")
            if password == repeat_password:
                self.password = repeat_password
                if self.login == self.write_to_db(self.login):
                    print('Вы уже есть в базе ')
                    return
                else:
                    print('вы внесены в базу')
                    return
            

    def validate(self):
        while True:
            input_number = input("enter password....")
            if input_number == self.password:
                break

    def memory_crypter(self):
        with open(self.path, "rb") as f:
            file_content = BytesIO(f.read())

        with open(self.path, "wb") as f:
            print("press 1 - Encrypt\npress 2 - Decrypt\n")
            method = int(input("->"))
            is_encrypted = True if method == 1 else False
            if is_encrypted:
                
                if not isinstance(self.write_to_db(self.login),str):
                    print('Вас нет в БД. Создайте логин и пароль')
                    self.create_password()
                print('Ваш профиль найден !')
                pyAesCrypt.encryptStream(
                file_content, self.sequence_bytes, self.password, self.buffersize
                )
                print('файл зашифрован успешно')
            else:
                self.validate()
                pyAesCrypt.decryptStream(
                    file_content,
                    self.sequence_bytes,
                    self.password,
                    self.buffersize,
                    len(file_content.getvalue()),
                )
            f.write(self.sequence_bytes.getvalue())


obj = Crypter("test.txt")
obj.memory_crypter()
