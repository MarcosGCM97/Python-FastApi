from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

router = APIRouter()

oauth2 = OAuth2PasswordBearer(tokenUrl='Login')

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
        'password': '1234'
    },
    'negro': {
        'username': 'negro',
        'fullName': 'Marcos Congre 2',
        'email': 'mc@gmail.com',
        'disabled': True,
        'password': '4321'
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
    

async def currentUser(token: str = Depends(oauth2)):
    user = searchUser(token)
    if not user:
        raise HTTPException(status_code= status.HTTP_401_UNAUTHORIZED, 
                            detail='Credenciales de autenticacion invalidas', 
                            headers={'WWW-Authenticate': 'Bearer'})
    if user.disabled:
        raise HTTPException(status_code= status.HTTP_400_BAD_REQUEST, detail='Usuario inactivo')
    
    return user


@router.post('/Login')
async def login(form: OAuth2PasswordRequestForm = Depends()):
    userDB = users_db.get(form.username)

    if not userDB:
        raise HTTPException(status_code= status.HTTP_400_BAD_REQUEST, detail='El usuario no es correcto')
    
    user = searchUserDB(form.username)
    if not form.password == user.password:
        raise HTTPException(status_code= status.HTTP_400_BAD_REQUEST, detail='La contraseña no es correcta')
    
    return {'access_token': user.username, 'token_type': 'bearer'}

@router.get('/users/me')
async def me(user: User = Depends(currentUser)):
    return user