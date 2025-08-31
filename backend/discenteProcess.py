'''
Todo o processo que um discente precisa fazer é estabelecido nesse código
O Discente JÁ PRECISA TER SIDO CRIADO caso contrário todo o processo que pode ser feito aqui
    terá sido em vão pois o código vai, no final, barrar o processo por conta do discente não existir
'''

from dataclasses import dataclass
from backend.environmentVariable import EnvironmentVariables
from backend.validationError import ValidationError
import pathlib
import json


@dataclass
class DiscenteProcess:
    #TODO: Se os códigos de controle solicitados pelas funções dessa classe existirem, então todos os processos podem ser acessados
    # Ou seja, não há restrições. Por exemplo, se um discente quiser estar cadastrado em 30 cursos e 30000 disciplinas, ele pode, 
    #   basta ter os códigos delas. Se quiserem coloquem restrições.

    '''
    __discente_code = Código de um discente que existe no sistema
    '''
    __discente_code: str
    __discente_name: str = "False"

    def __post_init__(self,):
        # Verifica se o código do discente fornecido existe
        if self.set_discente_code(self.get_discente_code()):
            print("Discente aceito")
        else:
            print("Discente não aceito.")
            raise(ValidationError)


    def set_discente_code(self, code):
        path = pathlib.Path('./lib/user.json')

        with open(path, mode="r", encoding="utf8") as f:
            if path.stat().st_size > 0:
                users = json.load(f)
            else:
                # Se o arquivo está vazio retorna um dicionário vazio
                users = {}
        
        if code in users.keys():
            if users[code]['type'] == EnvironmentVariables.DISCENTE.value:
                self.__discente_code = code
                self.__discente_name = users[code]['name']
                return True
            else:
                self.__discente_name = False
                self.__discente_name = False
                print("O código fornecido existe, mas não pertence a um discente")
                return False
        else:
            self.__discente_name = False
            self.__discente_name = False
            print("O código fornecido não existe em docente.")
            return False

    
    def add_discipline(self, code:str):
        path = pathlib.Path('./lib/discipline.json')
        with open(path, mode="r", encoding="utf8") as f:
            if path.stat().st_size > 0:
                disciplines = json.load(f)
            else:
                # Se o arquivo está vazio retorna um dicionário vazio
                disciplines = {}
        
        if code in disciplines.keys():
            path = pathlib.Path('./lib/user.json')

            with open(path, mode="r", encoding="utf8") as f:
                if path.stat().st_size > 0:
                    users = json.load(f)
                else:
                    # Se o arquivo está vazio retorna um dicionário vazio
                    users = {}
            
            if code in users.keys():
                if 'discipline' in users[code].keys():
                    users[code]

    def get_discente_code(self):
        return self.__discente_code

    def get_discente_name(self):
        return self.__discente_name
