#test_api.py
#Teste simples da API Flask

import requests
import json

url = "http://127.0.0.1:5000/registro"
data = {"usuario_id": 1}

response = requests.post(url, json=data)

print("STATUS:", response.status_code)
try:
    print("RESPOSTA JSON:", json.dumps(response.json(), indent=4, ensure_ascii=False))
except Exception as e:
    print("Erro ao decodificar JSON:", e)
    print("Resposta bruta:", response.text)
