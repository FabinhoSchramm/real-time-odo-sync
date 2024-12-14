import mysql.connector


def conectaSQL(local, banco=''):
    
    if local == 1:
        myHost = ''
        myUser = ''
        myPwd = '4'
        myDB = banco
        return mysql.connector.Connect(host=myHost, user=myUser, password=myPwd, database=myDB)

def fecharConexao(cursor, connection):
    cursor.close()
    connection.close()