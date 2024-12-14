import requests
from conexaoSQL import conectaSQL, fecharConexao
import json
import time

class auto_command:

  def db_send(self,placa,motorista,odometro,numero,
              status_envio,confirmacao,comando,id_evento,resposta) -> None:
    conexao = conectaSQL(1)
    cursor = conexao.cursor()
    cursor.execute("""SELECT * FROM """""""" WHERE
                      Placa = %s AND Motorista = %s AND Odometro = %s AND
                      Numero = %s AND Status_envio = %s AND Confirmacao = %s
                               """,(placa,motorista,odometro,numero,
                                    status_envio,confirmacao))
    if cursor.fetchone():
      return []
    else:
      cursor.execute("""INSERT INTO """"""""(Placa,Motorista,
                     Odometro,Numero,Status_envio,Confirmacao,Comando,Id_envio,Resposta)
                     VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s)
                     """,params=(placa,motorista,odometro,numero,
                                  status_envio,confirmacao,comando,id_evento,resposta))
      conexao.commit()

  def simcard_model(self,placa) -> list:
    conexao = conectaSQL(1)
    cursor = conexao.cursor()
    sql = 'SELECT Modelo,Chip FROM """""""" WHERE Placa = %s'
    value = (placa,)
    cursor.execute(sql,value)
    dados = cursor.fetchall()
    return dados

  def analise_banco_enviados(self,placa,odometro,motorista):
    conexao = conectaSQL(1)
    cursor = conexao.cursor()
    sql = "SELECT Placa,Odometro FROM """""""" WHERE Placa = %s and Odometro = %s and Motorista = %s"
    valor = (placa,odometro,motorista)
    cursor.execute(sql,valor)
    dados = cursor.fetchall()
    fecharConexao(cursor,conexao)
    return dados

  def send_command_gv50(self,modelo: str, number: str, id_capaing: str, odometro: str, placa: str) -> None:
    COUNTRY_CODE = 55
    TYPE_ = 1
    TIMEZONE = "-03:00"
    URL = '' #api sms market
    content = f'AT+GTCFG={modelo.lower()},{modelo.lower()},{modelo.lower()},1,{str(odometro).replace(",","")},,,3F,2,,2180F,,1,0,300,0,,,1,17,0,FFFF$'
    params = {
        'user': '',
        'password': '',
        'country_code': COUNTRY_CODE,
        'number': number,
        'content': content,
        'campaign_id': f'{id_capaing} {placa}',
        'type': TYPE_,
        'timezone': TIMEZONE,
        'utf8': 1,
    }
    HEADERS = {'Content-Type': 'application/x-www-form-urlencoded'}

    response = requests.get(URL, params=params, headers=HEADERS)
    response_body = response.text
    data = json.loads(response_body)
    if not data["success"]:
            print(Exception(f"Erro no envio do comando: {data['responseDescription']}"))
    self.db_send(placa=placa,motorista=id_capaing,numero=number,status_envio=data["success"],
                confirmacao=data["responseDescription"],
                comando=content,id_evento=data["id"],resposta=data["responseCode"],
                odometro=odometro)
    return f'status_code:{data["responseCode"]}, suceess: {data["success"]}, resposta_sms_mkt:{data["responseDescription"]}'

  def send_command_gv55(self, number: str, id_capaing: str, odometro: str, placa: str) -> None:
    COUNTRY_CODE = 55
    TYPE_ = 1
    TIMEZONE = "-03:00"
    URL = ''
    content = f'AT+GTCFG=GV55,,GV55,1,{str(odometro).replace(",","")},,,003F,2,,100C,1,0,0,,,,,,,,,,,,,,,,,,,FFFF$'
    params = {
        'user': '',
        'password': '',
        'country_code': COUNTRY_CODE,
        'number': number,
        'content': content,
        'campaign_id': f'{id_capaing} {placa}',
        'type': TYPE_,
        'timezone': TIMEZONE,
        'utf8': 1,
    }
    HEADERS = {'Content-Type': 'application/x-www-form-urlencoded'}

    response = requests.get(URL, params=params, headers=HEADERS)
    response_body = response.text
    data = json.loads(response_body)
    if not data["success"]:
            print(Exception(f"Erro no envio do comando: {data['responseDescription']}"))
    self.db_send(placa=placa,motorista=id_capaing,numero=number,status_envio=data["success"],
                confirmacao=data["responseDescription"],
                comando=content,id_evento=data["id"],resposta=data["responseCode"],
                odometro=odometro)
    return f'status_code:{data["responseCode"]}, suceess: {data["success"]}, resposta_sms_mkt:{data["responseDescription"]}'
  
  def log_err(self,values) -> None:
    conexao = conectaSQL(1)
    cursor = conexao.cursor()
    sql = """INSERT INTO """"""""(Nome,Placa,Odometro,Erro)
            VALUES(%s,%s,%s,%s)  
            """
    cursor.execute(sql,values)
    conexao.commit()
    fecharConexao(cursor,conexao)

  def err(self,values) -> None:
    conexao = conectaSQL(1)
    cursor = conexao.cursor()
    sql = """INSERT INTO """"""""(error)
            VALUES(%s)  
            """
    cursor.execute(sql,values)
    conexao.commit()
    fecharConexao(cursor,conexao)

  def handle_exception(self, motorista, placa, odometro, simcard, erro):
    with open('error_log.txt', 'a') as log_file:
        log_file.write(f"{time.strftime('%Y-%m-%d %H:%M:%S')} - Erro: {erro}\n")

    conexao = conectaSQL(1)
    cursor = conexao.cursor()
    sql = """INSERT INTO """"""""(Nome, Placa, Odometro, Simcard, Erro)
              VALUES(%s, %s, %s, %s, %s)  
          """
    values = (motorista, placa, odometro, simcard, erro) #, time.strftime('%Y-%m-%d %H:%M:%S')
    cursor.execute(sql, values)
    conexao.commit()
    fecharConexao(cursor, conexao)