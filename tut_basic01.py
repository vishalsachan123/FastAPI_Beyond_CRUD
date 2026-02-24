from fastapi import FastAPI
from enum import Enum
from pydantic import BaseModel

app = FastAPI()


class ModelName(str, Enum):
    alexnet = "alexnet"
    resnet = "resnet"
    lenet = "lenet"


class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None
    custom: str | None = None





@app.get("/") #path operation function
async def root():
    return {"response:": "Hello World"}

@app.get("/users/me")# to avoid conflicts between path operations, you can declare paths with fixed values before paths with path parameters.
async def read_user_me():
    return {"user_id": "the current user"}


@app.get("/users/{user_id}")
async def read_user(user_id: str):
    return {"user_id": user_id}


@app.get("/items/{item_id}") #You can declare path "parameters" or "variables" with the same syntax used by Python format strings.
async def read_item(item_id: int, q: str | None = None):#The value of the path parameter item_id will be passed to your function as the argument item_id.
    return {"item_id": item_id, "q": q}


@app.get("/models/{model_name}")
async def get_model(model_name: ModelName):
    if model_name is ModelName.alexnet:
        return {"model_name": model_name, "message": "Deep Learning FTW!"}

    if model_name.value == "lenet":
        return {"model_name": model_name, "message": "LeCNN all the images"}

    return {"model_name": model_name, "message": "Have some residuals"}



@app.get("/files/{file_path:path}")
async def read_file(file_path: str):
    """You could need the parameter to contain /home/johndoe/myfile.txt, with a leading slash (/).

In that case, the URL would be: /files//home/johndoe/myfile.txt, with a double slash (//) between files and home."""
    return {"file_path": file_path}




"""When you declare other function parameters that are not part of the path parameters,
 they are automatically interpreted as "query" parameters.
 
 The query is the set of key-value pairs that go after the ? in a URL, separated by & characters.

For example, in the URL: http://127.0.0.1:8000/items/?skip=0&limit=10

As query parameters are not a fixed part of a path, they can be optional and can have default values.

Query parameter type conversion ho jata hai, jaise ki path parameters ke case mein hota hai.

"""


fake_items_db = [{"item_name": "Foo"}, {"item_name": "Bar"}, {"item_name": "Baz"}]


@app.get("/items/")
async def read_item(skip: int = 0, limit: int = 10):
    return fake_items_db[skip : skip + limit]




#------------post request with body-----------------

@app.post("/items/")
async def create_item(item: Item):
    item_dict = item.model_dump()
    if item.tax is not None:
        price_with_tax = item.price + item.tax
        item_dict.update({"price_with_tax": price_with_tax})
    return item_dict


@app.put("/items/{item_id}")
async def update_item(item_id: int, item: Item):
    item_dict = item.model_dump()
    # item_dict.update({"item_id": item_id})
    return {"item_id": item_id, **item.model_dump()}
    return item_dict


"""The function parameters will be recognized as follows:

If the parameter is also declared in the path, it will be used as a path parameter.
If the parameter is of a singular type (like int, float, str, bool, etc) it will be interpreted as a query parameter.
If the parameter is declared to be of the type of a Pydantic model, it will be interpreted as a request body"""


@app.put("/items2/{item_id}")
async def update_item(item_id: int, item: Item, q: str | None = None):
    result = {"item_id": item_id, **item.model_dump()}
    if q:
        result.update({"q": q})
    return result


#Annoted and validation
from typing import Annotated
from fastapi import Query

@app.get("/items3/")
async def read_items(q: Annotated[str, Query(min_length=3, max_length=20)] = "fixedquery"):
    results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
    if q:
        results.update({"q": q})
    return results


# visit the documentation for more validation options, like aftervalidator and all






