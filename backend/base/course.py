'''
Estrutura dos cursos
O curso já deve ter sido criado pelo programa addBase.py por meio da função addCourse
    caso contrário, essa função não será corretamente preenchida e posteriormente será barrada
'''

from backend.base.discipline import Discipline
from backend.validationError import ValidationError
from dataclasses import dataclass, field
import pathlib
import json


@dataclass
class Course:
    __code: str
    __discipline: dict[str] = field(default_factory=dict)


    def __post_init__(self):
        # Valida se o curso inserido existe

        if self.set_code(self.__code):
            print("Curso aceito")
        else:
            raise ValidationError("O código não foi aceito.")


    def get_code(self,):
        return self.__code


    def set_code(self, code:str):
        path = pathlib.Path('./lib/course.json')

        with open(path, mode="r", encoding="utf8") as f:
            if path.stat().st_size > 0:
                course = json.load(f)
            else:
                # Se o arquivo está vazio retorna um dicionário vazio
                course = {}
        
        if code in course.keys():
            self.__code = code
            return True
        else:
            print("O código de curso inserido não existe")
            self.__code = False
            return False


    def add_discipline(self, discipline: Discipline)->bool:
        if isinstance(discipline, Discipline):
            self.__discipline[discipline.get_code()] = discipline
            print("Disciplina aceita.")
            return True
        else:
            print("Disciplina não adicionada. Adicione uma instância de disciplina.")


    def get_discipline(self,):
        return self.__discipline

    def get_code(self,):
        return self.__code


    def delete_discipline(self, code:str):
        if code in self.__discipline.keys():
            del self.__discipline[code]
            print("Disciplina deletada desse curso")
        else:
            print("Não há o que deletar. O curso não tem essa disciplina.")


    def register_course(self,):
        if self.__code:
            path = pathlib.Path('./lib/course.json')
            with open(path, mode="r", encoding='utf8') as f:
                course = json.load(f)
            
            for key, value in self.__discipline.items():
                course[self.__code]['discipline'].append(key)
            
            with open(path, mode="w", encoding='utf8') as f:
                course = json.dump(course, f, indent=4)
            print("Curso registrado")
        else:
            print("Não é possível registrar esse curso. Código de curso não reconhecido.")
