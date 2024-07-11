import hashlib
from typing import Annotated
from fastapi import Depends, FastAPI, Form, Response, UploadFile
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from fastapi.staticfiles import StaticFiles
import sqlite3
from fastapi_login import LoginManager
from fastapi_login.exceptions import InvalidCredentialsException 


con = sqlite3.connect('db.db', check_same_thread=False)
cur = con.cursor()

# cur.execute(f"""
#             CREATE TABLE IF NOT EXISTS items (
#                 id INTEGER PRIMARY KEY,
# 	            title TEXT NOT NULL,
# 	            image BLOB,
# 	            price INTEGER NOT NULL,
# 	            description TEXT, 
# 	            place TEXT NO NULL,
# 	            insertAt INTEGER NOT NULL
#             );
#             """)

# cur.execute(f"""
#            CREATE TABLE IF NOT EXISTS users (
#                 id TEXT PRIMARY KEY,
#                 name TEXT NOT NULL,
# 	            email TEXT NOT NULL,
# 	            password TEXT NOT NULL
#             );
#             """)

app = FastAPI()

SECRET = "super-coding"
manager = LoginManager(SECRET,"/login")

@manager.user_loader()
def query_user(data):
    WHERE_STATEMENTS = f'id="{data}"'
    if type(data) == dict:
        WHERE_STATEMENTS = f'''id="{data['id']}"'''
    con.row_factory = sqlite3.Row 
    cur = con.cursor()
    user = cur.execute(f"""
                       SELECT * FROM users WHERE {WHERE_STATEMENTS}
                       """).fetchone()
    return user
    
def hash_password(password):
    hash = hashlib.sha256(password.encode()).hexdigest()
    return hash

@app.post("/login")
def login(id:Annotated[str,Form()],
          password:Annotated[str,Form()]):
    user = query_user(id)
    sha256_password = hash_password(password)

    if not user:
        raise InvalidCredentialsException
        # 파이썬은 raise로 오류메세지 던짐
        # InvalidCredentialsException이 자동으로 status code를 401로 내려줌
    elif sha256_password != user['password']:
        raise InvalidCredentialsException
    
    access_token = manager.create_access_token(data={
        'sub':{
            'id':user['id'],
            'name':user['name'],
            'email':user['email']
        }
    })
    return {'access_token' : access_token}
    # 뭐로 리턴하든 status code는 200을 내려줌

@app.post("/signup") # 프론트엔드에서 폼을 통해서 post로 보냄(회원가입을 시켜달라고 요청을 보내는거니까)
def signup(id:Annotated[str,Form()],
           password:Annotated[str,Form()],
           name:Annotated[str,Form()],
           email:Annotated[str,Form()]):
    sha256_password = hash_password(password)
    cur.execute(f"""
                INSERT INTO users(id,name,email,password)
                VALUES ('{id}','{name}','{email}','{sha256_password}')
                """)
    con.commit()
    return "200"

@app.post("/items")
async def create_item(
                image:UploadFile, 
                title:Annotated[str,Form()], 
                price:Annotated[int,Form()], 
                description:Annotated[str,Form()], 
                place:Annotated[str,Form()],
                insertAt:Annotated[int,Form()]
                ):
    
    image_bytes = await image.read()
    cur.execute(f"""
                INSERT INTO 
                items (title, image, price, description, place, insertAt)
                VALUES
                ('{title}','{image_bytes.hex()}',{price},'{description}','{place}','{insertAt}')
                """)
    con.commit()
    return "200"
    
@app.get("/items")
async def get_items(user=Depends(manager)):
    # 아이템을 불러올때 user가 존재할때만 가능하도록 조건 달기
    con.row_factory = sqlite3.Row 
    #컬럼명도 함께 가져오도록 하는 문법
    #없을땐 컬럼명은 없이 데이터만 가지고 옴
    cur = con.cursor()
    rows = cur.execute(f"""
                       SELECT * from items;
                       """).fetchall()
    
    return JSONResponse(jsonable_encoder(dict(row) for row in rows))
    #위에서 컬럼명도 함께 받았는데 dict(row) for row in rows 이걸해주면 그 데이터들이 dictionary로 정리가 됨


@app.get("/images/{item_id}")
async def get_image(item_id: int):
    cur=con.cursor()
    image_bytes = cur.execute(f"""
                          SELECT image FROM items WHERE id={item_id}
                          """).fetchone()[0]
    return Response(content=bytes.fromhex(image_bytes),media_type="image/*")

app.mount("/", StaticFiles(directory="frontend", html = True), name="static")