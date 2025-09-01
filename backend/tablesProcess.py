import pathlib
import json
import copy
from backend.validationError import ValidationError
from backend.environmentVariable import EnvironmentVariables

def openDict(table_dict: dict, keys:list):
    "Iterativamente abre um dicionário"
    if keys:
        return openDict(table_dict=table_dict[keys[0]], keys=keys[1:])
    else:
        return table_dict


def checkValueInTable(path:pathlib.Path, keys:list, value:str):
    "Verifica se determinado valor está num dicionário"

    with open(path, mode="r", encoding="utf8") as f:
        table = json.load(f)

    return value in openDict(table_dict=table, keys=keys)


def write_json(path:pathlib.Path, wr:str) -> None:
    with open(path, mode="w", encoding="utf8") as f:
        json.dump(wr, f, indent=4)


def read_json(path:pathlib.Path) -> dict:
    with open(path, mode="r", encoding="utf8") as f:
        return json.load(f)


def register_discipline(discipline_code:str, discipline_dict: dict):
    # Basta registrar no json discipline.json

    with open('./lib/discipline.json', mode="r", encoding="utf8") as f:
        disciplines = json.load(f)
    
    disciplines[discipline_code].update(discipline_dict)

    with open('./lib/discipline.json', mode="w", encoding="utf8") as f:
        disciplines = json.dump(disciplines, f, indent=4)


def delete_discipline(discipline_code:str):
    # Deletar uma disciplina. É necessário:
    # deletar ela da tabela discipline.json
    # Deletar a disciplina de qualquer curso, discente, ou docente

    path_course = pathlib.Path('./lib/course.json')
    path_discipline = pathlib.Path('./lib/discipline.json')
    path_users = pathlib.Path('./lib/user.json')

    courses = read_json(path_course)
    disciplines = read_json(path_discipline)
    users = read_json(path_users)

    courses_copy = copy.deepcopy(courses)
    users_copy = copy.deepcopy(users)

    del disciplines[discipline_code]

    for key in courses_copy.keys():
        if discipline_code in courses[key]['discipline']:
            courses[key]['discipline'].remove(discipline_code)

    for key in users_copy.keys():
        if discipline_code in users[key]['discipline']:
            users[key]['discipline'].remove(discipline_code)

    write_json(path=path_course, wr=courses)
    write_json(path=path_discipline, wr=disciplines)
    write_json(path=path_users, wr=users)
        

def add_discente_in_discipline(self, discente_code:str, discipline_code:str):
    # É necessário:
    # Atribuir o discente na disciplina em discipline.json
    # Atribuir a disciplina para o discente em user.json

    path_discipline = pathlib.Path('./lib/discipline.json')
    path_users = pathlib.Path('./lib/user.json')

    disciplines = read_json(path_discipline)
    users = read_json(path_users)

    disciplines[discipline_code]['discente'].append(discipline_code)
    users[discipline_code]['discipline'].append(discipline_code)

    write_json(path_discipline, disciplines)
    write_json(path_users, users)


def delete_discente_in_discipline(self, discente_code:str, discipline_code:str):
    # É necessário:
    # Deletar o discente da disciplina em discipline.json
    # Deletar a disciplina no discente em user.json

    path_discipline = pathlib.Path('./lib/discipline.json')
    path_users = pathlib.Path('./lib/user.json')

    disciplines = read_json(path_discipline)
    users = read_json(path_users)

    disciplines[discipline_code]['discente'].remove(discipline_code)
    users[discipline_code]['discipline'].remove(discipline_code)

    write_json(path_discipline, disciplines)
    write_json(path_users, users)


def setDocenteInDiscipline(docente_code:str, discipline_code:str):
    # É necessário:
    # Como uma disciplina só pode ter 1 docente, então basta alterar o docente da disciplina
    # Ir em todos os docente e verificar se algum deles está cadastrado como docente dessa disciplina, se estiver retirar
    # Ir no docente docente_code e atribuir a atual disciplina para ele

    path_user = pathlib.Path('./lib/user.json')
    path_discipline = pathlib.Path('./lib/discipline.json')

    users = read_json(path=path_user)
    disciplines = read_json(path=path_discipline)

    disciplines[discipline_code]['docente_code'] = docente_code

    users_copy = copy.deepcopy(users)
    for key in users_copy.keys():
        if discipline_code in users[key]['discipline'] and users[key]['type'] == EnvironmentVariables.DOCENTE.value:
            users[key]['discipline'].remove(discipline_code)

    users[docente_code]['discipline'].append(discipline_code)

    write_json(path=path_user, wr=users)
    write_json(path=path_discipline, wr=disciplines)

    print('Docente atribuído')


def setDisciplineInCourse(course_code:str, discipline_code:str):
    # É necessário:
    # Ir em todos os cursos e verificar se em algum deles está presente discipline_code, se estiver retirar
    # Ir no curso course_code e atribuir a atual disciplina para ele

    path_course = pathlib.Path('./lib/course.json')

    courses = read_json(path=path_course)

    courses_copy = copy.deepcopy(courses)
    for key in courses_copy.keys():
        if discipline_code in courses[key]['discipline']:
            courses[key]['discipline'].remove(discipline_code)

    courses[course_code]['discipline'].append(discipline_code)

    write_json(path=path_course, wr=courses)

    print('Docente atribuído')
