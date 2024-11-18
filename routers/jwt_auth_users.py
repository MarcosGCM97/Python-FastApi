from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import jwt, JWTError
from passlib.context import CryptContext
from datetime import datetime, timedelta

ALGORITHM = 'HS256'
ACCESS_TOKEN_DURATION = 1
SECRET = '5143536845632159864'

router = APIRouter()

oauth2 = OAuth2PasswordBearer(tokenUrl='Login')

crypt = CryptContext(schemes=['bcrypt'])

class User(BaseModel):
    username: str
    fullName: str
    email: str
    disabled: bool

class UserDB(User): 
    password: str    

users_db = {
    'loboLC': {
        'username': 'loboLC',
        'fullName': 'Marcos Congre',
        'email': 'mc@gmail.com',
        'disabled': False,
        'password': '$2a$12$aCdA.zoP2eZpD9i8V70xI..Wm7FsuPhR0/y8BB5wox7AVr5fWhQnm'
    },
    'negro': {
        'username': 'negro',
        'fullName': 'Marcos Congre 2',
        'email': 'mc@gmail.com',
        'disabled': True,
        'password': '$2a$12$.O3tocKSVSiSp2Z7UYsE..50vNxrGDsyYBH81okylJ217Ymh3tgdu'
    }
}  


def searchUserDB(username: str):
    print(username)
    if username in users_db:
        return UserDB(**users_db[username])

def searchUser(username: str):
    print(username)
    if username in users_db:
        return User(**users_db[username])
    

async def authUser(token: str = Depends(oauth2)):
    
    exception =  HTTPException(
        status_code= status.HTTP_401_UNAUTHORIZED, 
        detail='Credenciales de autenticacion invalidas', 
        headers={'WWW-Authenticate': 'Bearer'})

    try:
        username = jwt.decode(token, SECRET, algorithms= [ALGORITHM]).get('sub')
        if username is None:
            raise exception

    except JWTError:  
        raise exception
    
    return searchUser(username)

async def currentUser(user: User = Depends(authUser)):
    if user.disabled:
        raise HTTPException(status_code= status.HTTP_400_BAD_REQUEST, detail='Usuario inactivo')
    
    return user
  

@router.post('/Login')
async def login(form: OAuth2PasswordRequestForm = Depends()):
    userDB = users_db.get(form.username)

    if not userDB:
        raise HTTPException(status_code= status.HTTP_400_BAD_REQUEST, detail='El usuario no es correcto')
    
    user = searchUserDB(form.username)

    if not crypt.verify(form.password, user.password):
        raise HTTPException(status_code= status.HTTP_400_BAD_REQUEST, detail='La contraseña no es correcta')
    
    accessTokenExpiration = timedelta(minutes=ACCESS_TOKEN_DURATION)

    expire = datetime.utcnow() + accessTokenExpiration

    accessToken= {
        'sub': user.username,
        'exp': expire
    }

    return {'access_token': jwt.encode(accessToken, SECRET, algorithm= ALGORITHM), 'token_type': 'bearer'}


@router.get('/users/me')
async def me(user: User = Depends(currentUser)):
    return user
