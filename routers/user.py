from typing import Union
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

router = APIRouter(
    prefix='/users',
    tags=['users'],
    responses= {404: {'message': 'No encontrado'}}
)

#Etidad User
class User(BaseModel):
    id: int
    name: str
    surname: str
    url: str
    age: int

usersList = [
    User(id= 1,name='Marcos', surname='Lobo', url='google.com', age= 25),
    User(id= 2,name='Cristian', surname='Cris', url='google.com', age= 25),
    User(id= 3,name='Jorge', surname='Tojor', url='google.com', age= 25)
]

@router.get("/usersJson")
async def usersJson():
    return [
        {"name": 'Marcos', 'surname': 'Lobo', 'url': 'google.com', 'age': 25},
        {"name": 'Cristian', 'surname': 'Cris', 'url': 'google.com', 'age': 25},
        {"name": 'Jorge', 'surname': 'Tojor', 'url': 'google.com', 'age': 25}
    ]

#llamar a todos PAHT
@router.get('/')
async def userClass():
    return usersList

#Llamar un solo id
@router.get('/{id}', status_code=200)
async def user(id: int):
    return searchUser(id)
#llamar a un id a travez del Query    
@router.get('/', status_code=200)
async def user(id: int):
    return searchUser(id)

#solicitud POST PUT DELETE   
@router.post('/',response_model= User , status_code=201)
async def userPost(user: User):
    if type(searchUser(user.id)) == User:
        raise HTTPException(status_code=204, detail= 'Este usuario ya existe')
    
    usersList.append(user)
    return user

@router.put('/')
async def userPut(user: User):

    found = False

    for index, savedUser in enumerate(usersList):
        if savedUser.id == user.id:
            usersList[index] = user
            found = True
    if not found:
        return {'error': 'No se encontro usuario'}
    
    return user        

@router.delete('/{id}', status_code=204)
async def userDelete(id: int):

    found = False

    for index, savedUser in enumerate(usersList):
        if savedUser.id == id:
            del usersList[index]
            found = True

    if not found:
        raise HTTPException(status_code=404, detail= 'Usuario no encontrado')   

    return {'status': 204, 'message': 'eliminado con exito'}     

#funciones
def searchUser(id: int):   
    users = filter(lambda user: user.id == id, usersList)
    try:
        return list(users)[0]
    except:
        raise HTTPException(status_code=404, detail= 'Usuario no encontrado')  