from fastapi import FastAPI, HTTPException, Request, Depends, status
import mysql.connector
from mysql.connector import Error
from fastapi.responses import HTMLResponse, JSONResponse
import os
from slowapi import Limiter
from slowapi.util import get_remote_address
from sqlalchemy import text
from fastapi.middleware.cors import CORSMiddleware


limiter = Limiter(key_func=get_remote_address)
app = FastAPI()

ALLOWED_ORIGINS = ["https://web-alzril.opelooo.studio"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["Authorization", "Content-Type"],
)


@app.middleware("http")
async def check_origin(request: Request, call_next):
    origin = request.headers.get("origin")

    # Reject requests from unapproved origins
    if origin and origin not in ALLOWED_ORIGINS:
        raise HTTPException(status_code=403, detail="CORS policy does not allow this origins")

    response = await call_next(request)
    return response

async def verify_referer(request: Request):
    referer = request.headers.get("referer")
    allowed_referers = [
        "https://api-alzril.opelooo.studio/docs",
        "https://api-alzril.opelooo.studio/"
    ]
    if referer not in allowed_referers:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access forbidden: Invalid referer."
        )

def get_db_connection():
    # Adjust the connection parameters according to your database settings.
    connection = mysql.connector.connect(
        host="172.31.0.29",          # Use your MariaDB host (could be a private IP)
        user="api_user",       # Replace with your MariaDB username
        password="strongpassword", # Replace with your MariaDB password
        database="dummy_db"        # The dummy database you created
    )
    return connection

@app.get("/employees", dependencies=[Depends(verify_referer)])
@limiter.limit("30/minute")  # Limit to 10 requests per minute per IP
def read_employees(request: Request):
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)  # Use dictionary=True to return rows as dict
        cursor.execute("SELECT * FROM employees")
        rows = cursor.fetchall()
        cursor.close()
        conn.close()
        return {"employees": rows}
    except Error as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/", response_class=HTMLResponse)
def read_index():
    index_path = "/usr/share/nginx/html/index.html"
    if os.path.isfile(index_path):
        try:
            with open(index_path, "r", encoding="utf-8") as f:
                content = f.read()
            return content
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error reading index file: {e}")
    else:
        raise HTTPException(status_code=404, detail="Index file not found.")

@app.exception_handler(Exception)
async def generic_exception_handler(request, exc):
    return JSONResponse(status_code=500, content={"message": "Internal Server Error"})


