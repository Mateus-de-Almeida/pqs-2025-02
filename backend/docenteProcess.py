'''
Todo o processo que um docente precisa fazer é estabelecido nesse código
O Docente JÁ PRECISA TER SIDO CRIADO caso contrário todo o processo que pode ser feito aqui
    terá sido em vão pois o código vai, no final, barrar o processo por conta do docente não existir
'''

from dataclasses import dataclass
from backend.environmentVariable import EnvironmentVariables
from backend.validationError import ValidationError
import pathlib
import json


@dataclass
class DocenteProcess:
    #TODO: Se os códigos de controle solicitados pelas funções dessa classe existirem, então todos os processos podem ser acessados
    # Ou seja, não há restrições. Por exemplo, se um docente quiser ser professor de 30 cursos e 30000 disciplinas, ele pode, 
    #   basta ter os códigos delas. Se quiserem coloquem restrições.

    '''
    _docente_code = Código de um discente que existe no sistema
    '''
    _docente_code: str
    _docente_name: str = "False"

    def __post_init__(self,):
        # Verifica se o código do docente fornecido existe
        if self.set_docente_code(self.get_docente_code()):
            print("Discente aceito")
        else:
            print("Discente não aceito.")
            raise(ValidationError)


    def set_docente_code(self, code):
        path = pathlib.Path('./lib/user.json')

        with open(path, mode="r", encoding="utf8") as f:
            if path.stat().st_size > 0:
                users = json.load(f)
            else:
                # Se o arquivo está vazio retorna um dicionário vazio
                users = {}
        
        if code in users.keys():
            if users[code]['type'] == EnvironmentVariables.DOCENTE.value:
                self._docente_code = code
                self._docente_name = users[code]['name']
                return True
            else:
                self._docente_name = False
                self._docente_name = False
                print("O código fornecido existe, mas não pertence a um docente")
                return False
        else:
            self._docente_name = False
            self._docente_name = False
            print("O código fornecido não existe.")
            return False


    def add_discipline(self, code:str):

        path_1 = pathlib.Path('./lib/discipline.json')
        with open(path_1, mode="r", encoding="utf8") as f:
            if path_1.stat().st_size > 0:
                disciplines = json.load(f)
            else:
                # Se o arquivo está vazio retorna um dicionário vazio
                disciplines = {}
        
        if code in disciplines.keys():
            path_2 = pathlib.Path('./lib/user.json')

            with open(path_2, mode="r", encoding="utf8") as f:
                if path_2.stat().st_size > 0:
                    users = json.load(f)
                else:
                    # Se o arquivo está vazio retorna um dicionário vazio
                    users = {}

            if 'discipline' in users[self.get_docente_code()].keys():
                if code not in users[self.get_docente_code()]['discipline']:
                    users[self.get_docente_code()]['discipline'].append(code)
            else:
                users[self.get_docente_code()]['discipline'] = []
                users[self.get_docente_code()]['discipline'].append(code)
            
            if self.get_docente_code() not in disciplines[code]['discente']:
                disciplines[code]['discente'].append(self.get_docente_code())

            with open(path_1, mode="w", encoding="utf8") as f:
                json.dump(disciplines, f, indent=4,)
            
            with open(path_2, mode="w", encoding="utf8") as f:
                json.dump(users, f, indent=4,)

            print("Aluno aceito na disciplina.")
        else:
            print("O código de disciplina fornecido não existe.")

    
    def delete_discipline(self, code:str):

        path_1 = pathlib.Path('./lib/discipline.json')
        with open(path_1, mode="r", encoding="utf8") as f:
            if path_1.stat().st_size > 0:
                disciplines = json.load(f)
            else:
                # Se o arquivo está vazio retorna um dicionário vazio
                disciplines = {}
        
        if code in disciplines.keys():
            path_2 = pathlib.Path('./lib/user.json')

            with open(path_2, mode="r", encoding="utf8") as f:
                if path_2.stat().st_size > 0:
                    users = json.load(f)
                else:
                    # Se o arquivo está vazio retorna um dicionário vazio
                    users = {}

            if 'discipline' in users[self.get_docente_code()].keys() and code in users[self.get_docente_code()]['discipline']:
                users[self.get_docente_code()]['discipline'].remove(code)

                disciplines[code]['discente'].remove(self.get_docente_code())

                with open(path_1, mode="w", encoding="utf8") as f:
                    json.dump(disciplines, f, indent=4,)
                
                with open(path_2, mode="w", encoding="utf8") as f:
                    json.dump(users, f, indent=4,)
                
                print("Disciplina deletada de seus registros.")
            else:
                print('Não há o que deletar, essa disciplina não existe em seus registros')
        else:
            print("O código de disciplina fornecido não existe.")
                

    def get_docente_code(self):
        return self._docente_code

    def get_docente_name(self):
        return self._docente_name
