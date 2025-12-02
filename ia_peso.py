# ia_peso.py (EXPANDIDO)
#Implementação do nosso Machine Learning

import numpy as np
import pandas as pd
# Regressão Linear para a nova previsão
from sklearn.linear_model import LogisticRegression, LinearRegression 

class IAPreditorPeso:
    def __init__(self):
        # Modelo para PREVISÃO DE TENDÊNCIA (usando Regressão Logística)
        self.modelo_tendencia = LogisticRegression(max_iter=1000)
        self.modelo_peso_futuro = LinearRegression()
        self.treinou = False

    def gerar_dataset_sintetico(self, n=2500):
        #Geração do dataset sintetico (2500 linhas)
        dados = []
        for _ in range(n):
            calorias_meta = np.random.randint(1500, 3000)
            calorias_consumidas = calorias_meta + np.random.randint(-1200, 1200)
            atividade = np.random.choice([1, 2, 3])
            peso_atual = np.random.uniform(50, 120)
            altura = np.random.uniform(1.50, 1.90)
            saldo = calorias_consumidas - calorias_meta
            
            if saldo > 350:
                tendencia = 1
            elif saldo < -350:
                tendencia = -1
            else:
                tendencia = 0
                
            # Lógica para Peso Futuro (Exemplo Simplificado: 
            # Saldo positivo -> Ganho de peso; Saldo negativo -> Perda de peso
            peso_futuro = peso_atual + (saldo / 7700) * 1.5 # 7700 kcal ~= 1kg
            
            dados.append([calorias_consumidas, calorias_meta, saldo, atividade, 
                          peso_atual, altura, tendencia, peso_futuro])
            
        df = pd.DataFrame(dados, columns=["cal_consumidas", "cal_meta", "saldo", 
                                        "atividade", "peso_atual", "altura", 
                                        "tendencia", "peso_futuro"])
        return df

    def treinar(self):
        df = self.gerar_dataset_sintetico()
        
        # Treinamento do modelo de TENDÊNCIA
        X_tendencia = df[["cal_consumidas", "cal_meta", "saldo", "atividade", "peso_atual"]]
        y_tendencia = df["tendencia"]
        self.modelo_tendencia.fit(X_tendencia, y_tendencia)
        
        # Treinamento do modelo de PESO FUTURO
        X_peso_futuro = df[["saldo", "peso_atual"]]
        y_peso_futuro = df["peso_futuro"]
        self.modelo_peso_futuro.fit(X_peso_futuro, y_peso_futuro)
        
        self.treinou = True

    def prever_tendencia(self, calorias_consumidas, calorias_meta, atividade, peso_atual):
        if not self.treinou:
            self.treinar()
            
        saldo = calorias_consumidas - calorias_meta
        entrada = np.array([[calorias_consumidas, calorias_meta, saldo, atividade, peso_atual]])
        tendencia = self.modelo_tendencia.predict(entrada)[0]
        explicacao = self.gerar_explicacao(tendencia, saldo, atividade)
        
        return {"tendencia": int(tendencia), "explicacao": explicacao}
        
    def prever_peso_futuro(self, calorias_consumidas, calorias_meta, peso_atual):
        if not self.treinou:
            self.treinar()
            
        saldo = calorias_consumidas - calorias_meta
        entrada = np.array([[saldo, peso_atual]])
        peso_futuro = self.modelo_peso_futuro.predict(entrada)[0]
        
        return float(peso_futuro)

    def calcular_imc(self, peso_atual, altura):
        """Calcula o Índice de Massa Corporal (IMC)"""
        # IMC = peso / altura²
        if altura <= 0:
             return 0.0
        imc = peso_atual / (altura ** 2)
        return float(imc)
        
    def interpretar_imc(self, imc):
        """Retorna a classificação do IMC"""
        if imc < 18.5:
            return "Abaixo do Peso"
        elif 18.5 <= imc < 24.9:
            return "Peso Normal"
        elif 25.0 <= imc < 29.9:
            return "Sobrepeso"
        elif 30.0 <= imc < 34.9:
            return "Obesidade Grau I"
        elif 35.0 <= imc < 39.9:
            return "Obesidade Grau II"
        else:
            return "Obesidade Grau III (Mórbida)"

    def gerar_explicacao(self, tendencia, saldo, atividade):
        if tendencia == 1:
            return f"Tendência de **GANHO** de peso. Você está em superávit de **{saldo:.0f} kcal**. Com a atividade física atual (nível {atividade}), o corpo tende a armazenar o excedente como gordura."
        elif tendencia == -1:
            return f"Tendência de **PERDA** de peso. Seu déficit de **{abs(saldo):.0f} kcal** está fazendo seu corpo usar as reservas como energia."
        else:
            return f"Tendência de **ESTABILIDADE**. O saldo calórico atual ({saldo:.0f} kcal) está próximo do neutro, mantendo o peso."