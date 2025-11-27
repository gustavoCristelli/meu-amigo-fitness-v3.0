#logic.py

from ia_peso import IAPreditorPeso

ia_modelo = IAPreditorPeso()

def analisar_registro(calorias_consumidas, calorias_gastas):
    saldo = calorias_consumidas - calorias_gastas
    if saldo > 300:
        return {"status": "excedeu", "mensagem": "Você consumiu mais do que gastou. Risco de ganhar peso."}
    elif saldo < -300:
        return {"status": "abaixo", "mensagem": "Você gastou mais do que consumiu. Risco de perder peso rápido."}
    else:
        return {"status": "equilibrado", "mensagem": "Seu saldo calórico está equilibrado. Bom trabalho!"}

def analisar_usuario(calorias_consumidas, atividade, peso, idade, sexo, massa_gorda):
    calorias_meta = 2000
    resultado = ia_modelo.prever(calorias_consumidas, calorias_meta, atividade, peso)
    return resultado
