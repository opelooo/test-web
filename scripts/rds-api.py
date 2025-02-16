import mysql.connector
import requests
import json

# Konfigurasi koneksi ke RDS MySQL
db_config = {
    'host': 'rds-endpoint.amazonaws.com',
    'user': 'db_user',
    'password': 'db_password',
    'database': 'nama_database'
}

def query_database():
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor(dictionary=True)  # agar hasil dalam bentuk dict
    query = "SELECT * FROM tabel_contoh"
    cursor.execute(query)
    result = cursor.fetchall()
    cursor.close()
    conn.close()
    return result

def kirim_ke_public_api(data):
    # Ganti URL dengan endpoint FastAPI yang di-expose oleh EC2 Public
    url = "http://api-alzril.opelooo.studio/api/receive-data"
    headers = {'Content-Type': 'application/json'}
    response = requests.post(url, data=json.dumps(data), headers=headers)
    return response.status_code, response.text

if __name__ == "__main__":
    hasil_query = query_database()
    status, resp_text = kirim_ke_public_api(hasil_query)
    print("Status Pengiriman:", status)
    print("Response:", resp_text)
