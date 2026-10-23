from pydantic import BaseModel

class Product(BaseModel):
    id : int = "Enter the ID"
    name :str = "Enter the Name"
    price : float ="Enter the correct Float"
    product_Avail: bool  = True

productOne = Product(id=1, name="Football" , price = 100.5)
productTwo = Product(id=1, name="Football" , price = 100.5, product_Avail = False)
productThree = Product(name="Football" , price = 100.5, product_Avail = False)
print(productOne)
print(productTwo)
print(productThree)