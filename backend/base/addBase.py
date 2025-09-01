'''
Criar as unidades básicas do software. São as únicas unidades que tem a permissão de serem inseridas apenas
com os valores de 'nome' e 'código' (no caso de users, eles também precisam de um tipo: docente ou discente) 
'''

from backend.environmentVariable import EnvironmentVariables
import json
import pathlib


def addCourse(name:str, code:str):
    #TODO: Não é verificado a unicidade dos cursos

    path = pathlib.Path('./lib/course.json')

    if not path.exists():
        path.parent.mkdir(parents=True, exist_ok=True)
        path.touch(exist_ok=True)

    with open(path, mode="r", encoding="utf8") as f:
        if path.stat().st_size > 0:
            courses = json.load(f)
        else:
            # Se o arquivo está vazio retorna um dicionário vazio
            courses = {}
    

    courses[code] = {'name': name, 'discipline': []}
    with open(path, mode="w", encoding='utf8') as f:
        json.dump(courses, f, indent= 4)
    
    print("Curso adicionado")


def addDiscipline(code:str, name:str):
    # Adiciona uma disciplina

    path = pathlib.Path('./lib/discipline.json')

    if not path.exists():
        path.parent.mkdir(parents=True, exist_ok=True)
        path.touch(exist_ok=True)

    with open(path, mode="r", encoding="utf8") as f:
        if path.stat().st_size > 0:
            disciplines = json.load(f)
        else:
            # Se o arquivo está vazio retorna um dicionário vazio
            disciplines = {}

    disciplines[code] = {'name':name}
    with open(path, mode="w", encoding='utf8') as f:
        json.dump(disciplines, f, indent= 4)

    print("Disciplina adicionada")



def addUser(type_:EnvironmentVariables, name:str, code:str):
    #TODO: Não é verificado a unicidade dos usuários, nem se o email deles (code) realmente existem

    path = pathlib.Path('./lib/user.json')
    if not path.exists():
        path.parent.mkdir(parents=True, exist_ok=True)
        path.touch(exist_ok=True)

    with open(path, mode="r", encoding="utf8") as f:
        if path.stat().st_size > 0:
            users = json.load(f)
        else:
            # Se o arquivo está vazio retorna um dicionário vazio
            users = {}
    

    users[code] = {'name': name, 'type':type_.value, 'discipline': []}
    with open(path, mode="w", encoding='utf8') as f:
        json.dump(users, f, indent= 4)
    
    print("Usuário adicionado")