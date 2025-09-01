'''
Estrutura dos cursos
O curso já deve ter sido criado pelo programa addBase.py por meio da função addCourse
    caso contrário, essa função não será corretamente preenchida e posteriormente será barrada
'''

from backend.base.discipline import Discipline
from backend.validationError import ValidationError
import backend.tablesProcess as tp
import attrs
import pathlib
import json


@attrs.define
class Course:
    course_code: str = attrs.field(validator=lambda instance, attribute, value: instance._course_code_validator(attribute, value))
    _discipline: list[str] = attrs.field(factory=list)


    def _course_code_validator(self, attribute, value):
        path_course = pathlib.Path('./lib/course.json')
        if not tp.checkValueInTable(path=path_course, keys=[], value=value):
            raise ValidationError("Curso inserido não existe")


    def add_discipline(self, discipline: Discipline):
        if isinstance(discipline, Discipline):
            self._discipline.append(discipline)
        else:
            print("Disciplina não adicionada. Adicione uma instância de disciplina.")


    def delete_discipline(self, code:str):
        if code in self._discipline:
            self._discipline.remove(code)
        else:
            print("Não há o que deletar. O curso não tem essa disciplina.")


    def register_course(self,):
        path = pathlib.Path('./lib/course.json')

        with open(path, mode="r", encoding='utf8') as f:
            course = json.load(f)
        
        for key, value in self._discipline.items():
            course[self._code]['discipline'].append(key)
        
        with open(path, mode="w", encoding='utf8') as f:
            course = json.dump(course, f, indent=4)

        print("Curso registrado")
