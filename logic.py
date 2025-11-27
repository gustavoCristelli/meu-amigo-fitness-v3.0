# logic.py (ATUALIZADO)
#Lógica de análise e previsão

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

def analisar_usuario(calorias_consumidas, atividade, peso, altura, idade, sexo, massa_gorda):
    calorias_meta = 2000
    
    #1 Previsão de Tendência
    resultado_tendencia = ia_modelo.prever_tendencia(calorias_consumidas, calorias_meta, atividade, peso)
    
    #2 Previsão de Peso Futuro
    peso_futuro = ia_modelo.prever_peso_futuro(calorias_consumidas, calorias_meta, peso)
    
    #3 Cálculo e Interpretação do IMC
    imc = ia_modelo.calcular_imc(peso, altura)
    classificacao_imc = ia_modelo.interpretar_imc(imc)
    
    return {
        "tendencia": resultado_tendencia["tendencia"],
        "explicacao": resultado_tendencia["explicacao"],
        "peso_futuro_estimado": peso_futuro,
        "imc": imc,
        "classificacao_imc": classificacao_imc
    }