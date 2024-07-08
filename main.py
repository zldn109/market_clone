from typing import Annotated
from fastapi import FastAPI, Form, Response, UploadFile
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from fastapi.staticfiles import StaticFiles
import sqlite3

con = sqlite3.connect('db.db', check_same_thread=False)
cur = con.cursor()

app = FastAPI()



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
async def get_items():
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
    return Response(content=bytes.fromhex(image_bytes))

app.mount("/", StaticFiles(directory="frontend", html = True), name="static")