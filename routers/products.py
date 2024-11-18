from fastapi import APIRouter

router = APIRouter(
    prefix='/products', 
    tags= ['products'],
    responses= {404: {'message': 'No encontrado'}}
)

productsList = ["Producto 1","Producto 2","Producto 3","Producto 4","Producto 5"]

@router.get('/')
async def productos():
    return productsList

@router.get('/{id}')
async def products(id: int):
    return productsList[0]