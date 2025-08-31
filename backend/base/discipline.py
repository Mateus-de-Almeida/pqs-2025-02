'''
Estrutura das disciplinas
O Docente já deve ter sido criado pelo programa addBase.py por meio da função addUser
    caso contrário, essa função não será corretamente preenchida e posteriormente será barrada.
    O mesmo critério de existência vale para o código da disciplina, pois já deve ter sido criado
    pelo programa addBase.py por meio da função addDiscipline
'''

from dataclasses import dataclass, field
import json
import pathlib
from backend.environmentVariable import EnvironmentVariables
from backend.validationError import ValidationError

@dataclass
class Discipline:
    #TODO: Falta restrições. A única restrição inserida aqui é verificar se a disciplina e docente da disciplina existem
    '''
    name = nome da disciplina
    __code = código da disciplina
    workload = carga horária dessa disciplina
    day = dias que essa disciplina ocorre. Ex.: [2,3,4] = [segunda, terça, quarta]
    classroom = aulas em que essa disciplina ocorre. Ex.: [2,3] = [segundo e terceiro horário]
    shift = turno
    __docente_code = código do docente dessa disciplina
    '''

    __code:str
    workload: str
    day:list
    classroom: list
    shift: str
    __docente_code:str
    __name: str = 'False'


    def __post_init__(self):
        # Valida se o docente inserido existe
        if self.set_docente_code(self.__docente_code):
            print("Docente aceito")
        else:
            self.__docente_code = False
            raise ValidationError("O Docente não foi aceito")

        # Valida se a disciplina existe
        if self.set_code_discipline(self.__code):
            print("Disciplina aceita")
        else:
            raise ValidationError("O código da Disciplina não existe.")


    def set_code_discipline(self, code:str)->bool:
        path = pathlib.Path('./lib/discipline.json')

        with open(path, mode="r", encoding="utf8") as f:
            if path.stat().st_size > 0:
                disciplines = json.load(f)
            else:
                # Se o arquivo está vazio retorna um dicionário vazio
                disciplines = {}
        
        if code in disciplines.keys():
            self.__code = code
            self.__name = disciplines[code]['name']
            return True
        else:
            print("O código de disciplina inserida não existe.")
            self.__code = False
            self.__name = False
            return False


    def set_docente_code(self, code:str) -> bool:

        path = pathlib.Path('./lib/user.json')

        with open(path, mode="r", encoding="utf8") as f:
            if path.stat().st_size > 0:
                users = json.load(f)
            else:
                # Se o arquivo está vazio retorna um dicionário vazio
                users = {}
        
        if code in users.keys():
            if users[code]['type'] == EnvironmentVariables.DOCENTE.value:
                self.__docente_code = code
                return True
            else:
                print("O código fornecido existe, mas não pertence a um docente")
                return False
        else:
            print("O código fornecido não existe.")
            return False


    def get_docente_code(self,):
        return self.__docente_code


    def get_code(self,):
        return self.__code


    def get_name(self,):
        return self.__name


    def get_dict_discipline(self,):        
        return {
            'name': self.__name, 'workload': self.workload, 'day': self.day, 'classroom': self.classroom,
            'shift': self.shift, 'docente_code': self.__docente_code, 'discentes': []
            }
    
    def register_discipline(self,):
        path = pathlib.Path('./lib/discipline.json')
        with open(path, mode="r", encoding="utf8") as f:
            if path.stat().st_size > 0:
                disciplines = json.load(f)
            else:
                # Se o arquivo está vazio retorna um dicionário vazio
                disciplines = {}

        disciplines[self.get_code()] = self.get_dict_discipline()
        with open(path, mode="w", encoding='utf8') as f:
            json.dump(disciplines, f, indent= 4)

        
