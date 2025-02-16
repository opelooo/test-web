from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

app = FastAPI()

@app.post("/api/receive-data")
async def receive_data(request: Request):
    try:
        data = await request.json()
        # Lakukan proses yang diinginkan dengan data tersebut, misalnya simpan ke database lokal atau log
        print("Data diterima:", data)
        return JSONResponse(content={"message": "Data berhasil diterima", "jumlah_data": len(data)})
    except Exception as e:
        return JSONResponse(status_code=400, content={"message": "Gagal memproses data", "error": str(e)})

# Endpoint tambahan untuk menampilkan data, jika diperlukan
@app.get("/api/status")
def status():
    return {"message": "FastAPI berjalan dengan baik"}

@app.get('/api/call?{nama}')
async def get_specific_data(nama: str):
    data={}
    # Get data from the database
    data = func.filter_data(nama)

    # Return the data as JSON response
    if data:
        return data
    else:
        return {"message": "No data found"}
