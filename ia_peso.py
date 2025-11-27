#ia_peso.py

import numpy as np
import pandas as pd
from sklearn.linear_model import LogisticRegression

class IAPreditorPeso:
    def __init__(self):
        self.modelo = LogisticRegression()
        self.treinou = False

    def gerar_dataset_sintetico(self, n=1500):
        dados = []
        for _ in range(n):
            calorias_meta = np.random.randint(1500, 3000)
            calorias_consumidas = calorias_meta + np.random.randint(-900, 900)
            atividade = np.random.choice([1, 2, 3])
            peso = np.random.uniform(50, 120)
            saldo = calorias_consumidas - calorias_meta
            if saldo > 300:
                tendencia = 1
            elif saldo < -300:
                tendencia = -1
            else:
                tendencia = 0
            dados.append([calorias_consumidas, calorias_meta, saldo, atividade, peso, tendencia])
        df = pd.DataFrame(dados, columns=["cal_consumidas", "cal_meta", "saldo", "atividade", "peso", "tendencia"])
        return df

    def treinar(self):
        df = self.gerar_dataset_sintetico()
        X = df[["cal_consumidas", "cal_meta", "saldo", "atividade", "peso"]]
        y = df["tendencia"]
        self.modelo.fit(X, y)
        self.treinou = True

    def prever(self, calorias_consumidas, calorias_meta, atividade, peso):
        if not self.treinou:
            self.treinar()
        saldo = calorias_consumidas - calorias_meta
        entrada = np.array([[calorias_consumidas, calorias_meta, saldo, atividade, peso]])
        tendencia = self.modelo.predict(entrada)[0]
        explicacao = self.gerar_explicacao(tendencia, saldo, atividade)
        return {"tendencia": int(tendencia), "explicacao": explicacao}

    def gerar_explicacao(self, tendencia, saldo, atividade):
        if tendencia == 1:
            return f"Tendência de GANHO de peso. Você está em superávit de {saldo} kcal. Com a atividade física atual (nível {atividade}), o corpo tende a armazenar o excedente como gordura."
        elif tendencia == -1:
            return f"Tendência de PERDA de peso. Seu déficit de {saldo} kcal está fazendo seu corpo usar as reservas como energia."
        else:
            return f"Tendência de ESTABILIDADE. O saldo calórico atual ({saldo} kcal) está próximo do neutro, mantendo o peso."
