'''
Estrutura das disciplinas
O Docente já deve ter sido criado pelo programa addBase.py por meio da função addUser
    caso contrário, essa função não será corretamente preenchida e posteriormente será barrada.
    O mesmo critério de existência vale para o código da disciplina, pois já deve ter sido criado
    pelo programa addBase.py por meio da função addDiscipline
'''

import attrs
import pathlib
from backend.validationError import ValidationError
import  backend.tablesProcess as tp
import json


@attrs.define
class Discipline:
    #TODO: Falta restrições relativas a correlação de day, classroom e workload.
    '''
    discipline_code = código da disciplina
    workload = carga horária dessa disciplina
    day = dias que essa disciplina ocorre. Ex.: [2,3,4] = [segunda, terça, quarta]
    classroom = aulas em que essa disciplina ocorre. Ex.: [2,3] = [segundo e terceiro horário]
    shift = turno
    '''

    discipline_code:str = attrs.field(validator=lambda instance, attribute, value: instance._discipline_code_validator(attribute, value))
    workload: int = attrs.field(validator=lambda instance, attribute, value: instance._workload_validator(attribute, value))
    day:list[int] = attrs.field(validator=lambda instance, attribute, value: instance._day_validator(attribute, value))
    classroom: list[int] = attrs.field(validator=lambda instance, attribute, value: instance._classroom_validator(attribute, value))
    shift: str = attrs.field(validator=lambda instance, attribute, value: instance._shift_validator(attribute, value))


    def get_dict_discipline(self,):        
        return {
            'workload': self.workload, 'day': self.day, 'classroom': self.classroom,
            'shift': self.shift, 'discente': []
            }

    def _discipline_code_validator(self, attribute, value):
        path_discipline = pathlib.Path('./lib/discipline.json')
        if not tp.checkValueInTable(path=path_discipline, keys=[], value=value):
            raise ValidationError("Disciplina inserida não existe")
            
    
    def _workload_validator(self, attribute, value):
        if not (isinstance(value, int) and value >= 16 and value <= 256):
            raise ValidationError("Carga horária invalida")
    
    def _day_validator(self, attribute, value):
        if any((not isinstance(i, int) or i not in [2,3,4,5,6,7]) for i in value):
            raise ValidationError("Os dias inseridos são inválidos")
    
    def _classroom_validator(self, attribute, value):
        if any((not isinstance(i, int) or i not in [1,2,3,4,5]) for i in value):
            raise ValidationError("Os horários de aulas inseridos são inválidos")

    def _shift_validator(self, attribute, value):
        if value not in ('noturno', 'matutino', 'vespertino'):
            raise ValidationError("O turno inserido é inválido")

    def register_discipline(self,):
        tp.register_discipline(discipline_code=self.discipline_code, discipline_dict=self.get_dict_discipline())
    
    @classmethod
    def delete_discipline(self,):
        tp.delete_discipline(self.discipline_code)
        

            

        
