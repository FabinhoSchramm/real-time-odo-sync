import gspread
from oauth2client.service_account import ServiceAccountCredentials
import time
from main import auto_command


class ExcelUpdater:

    def __init__(self):
        scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
        credentials = ServiceAccountCredentials.from_json_keyfile_name('auth/googlesheetauth.json', scope)
        self.gc = gspread.authorize(credentials)

        self.planilha = self.gc.open_by_url('')

        self.worksheet = self.planilha.worksheet('Respostas')

        self.current_data = self.get_data()

        self.send = auto_command()

    def get_data(self):
        try:
            data = self.worksheet.get_all_records()
            return data
        except IndexError:
            return []

    def check_for_new_data(self):
        while True:
            new_data = self.get_data()
            
            if not self.current_data and new_data:
                self.current_data = new_data
                print("Dados iniciais detectados na planilha.")
            elif new_data != self.current_data:
                self.perform_operation(new_data)
                self.current_data = new_data
                print("Dados atualizados com sucesso.")
            else:
                print("Nenhum dado novo encontrado.")

            time.sleep(5)

    def replace_char(self,char: str) -> str:
        return str(char).replace('-','').strip().replace(' ','').replace('.','').upper()

    def perform_operation(self, new_data):
        for data in new_data:
            if data not in self.current_data:
                motorista = data['Nome:']
                placa = self.replace_char(str(data['Placa:']))
                odometro = data['Odômetro:']
                dados_equip = self.send.simcard_model(placa=placa)
                modelo = dados_equip[0][0]
                simcard = dados_equip[0][1]
                if modelo == 'GV55':
                    print(self.send.send_command_gv55(number=simcard,id_capaing=motorista,odometro=odometro,placa=placa.upper()))
                else:    
                    print(self.send.send_command_gv50(modelo=modelo,number=simcard,id_capaing=motorista,odometro=odometro,placa=placa.upper()))        
        self.current_data = new_data

if __name__ == '__main__':
    while True:
        try:
            excel_updater = ExcelUpdater()
            excel_updater.check_for_new_data()
        except Exception as e:
            print(f"Ocorreu um erro: {str(e)}. O programa será reiniciado.")