#routes.py
#Configuração das rotas da API Flask

from flask import request, jsonify
from models import db, Usuario, RegistroDiario
from logic import analisar_registro, analisar_usuario
import numpy as np

def to_native(x):
    """Converte tipos do NumPy para tipos nativos do Python para serialização JSON."""
    if isinstance(x, (np.integer, np.int64)):
        return int(x)
    if isinstance(x, (np.floating, np.float64)):
        return float(x)
    return x

def configure_routes(app):

    @app.route('/')
    def home():
        return {"mensagem": "API Meu Amigo Fitness funcionando!"}

    @app.route('/usuario', methods=['POST'])
    def criar_usuario():
        dados = request.json
        usuario = Usuario(
            nome=dados['nome'],
            idade=dados['idade'],
            peso_atual=dados['peso_atual'],
            altura=dados['altura'],
            sexo=dados['sexo'],
            nivel_atividade=dados['nivel_atividade']
        )
        db.session.add(usuario)
        db.session.commit()
        return {"mensagem": "Usuário criado!", "id": usuario.id}

    @app.route('/registro', methods=['POST'])
    def registrar():
        dados = request.json
        usuario_id = dados.get("usuario_id")
        
        # 1. Tenta buscar a altura do BD ou usa valor padrão
        altura_db = 1.70
        if usuario_id:
            usuario = db.session.get(Usuario, usuario_id)
            if usuario and usuario.altura is not None:
                altura_db = usuario.altura
             
        # 2. Obtém os dados, priorizando os passados no JSON, mas usando padrões
        atividade = dados.get("atividade", 2)
        peso_atual = dados.get("peso_atual", 70)
        altura = dados.get("altura", altura_db) # Usa altura do JSON ou do BD/padrão
        calorias_consumidas = dados.get("calorias_consumidas", 2000)
        calorias_gastas = dados.get("calorias_gastas", 300)
        idade = dados.get("idade", 30)
        sexo = dados.get("sexo", "M")
        massa_gorda = dados.get("massa_gorda", 25.0)

        # 3. Salva o registro
        registro = RegistroDiario(
            usuario_id=usuario_id,
            calorias_consumidas=calorias_consumidas,
            calorias_gastas=calorias_gastas
        )
        db.session.add(registro)
        db.session.commit()

        saldo_calorico = calorias_consumidas - calorias_gastas
        resposta_analise = analisar_registro(calorias_consumidas, calorias_gastas)
        
        # 4. Chama a função de análise IA com o novo parâmetro 'altura'
        previsao_ia = analisar_usuario(
            calorias_consumidas,
            atividade,
            peso_atual,
            altura, # NOVO PARÂMETRO
            idade,
            sexo, # Este é o string "M" ou "F" que será ignorado/convertido no logic.py
            massa_gorda
        )
        
        # 5. Retorna o JSON com os novos campos de previsão
        return jsonify({
            "mensagem": "Registro salvo com sucesso!",
            "usuario": {k: to_native(v) for k, v in {
                "id": usuario_id,
                "peso_atual": peso_atual,
                "altura": altura,
                "atividade": atividade,
                "idade": idade,
                "sexo": sexo,
                "massa_gorda": massa_gorda
            }.items()},
            "registro": {k: to_native(v) for k, v in {
                "calorias_consumidas": calorias_consumidas,
                "calorias_gastas": calorias_gastas,
                "saldo_calorico": saldo_calorico
            }.items()},
            "analise_saldo": {k: to_native(v) for k, v in resposta_analise.items()},
            "previsao_ia": {
                "tendencia": to_native(previsao_ia["tendencia"]),
                "descricao": previsao_ia["explicacao"],
                "peso_futuro_estimado": f"{to_native(previsao_ia['peso_futuro_estimado']):.2f} kg", # Formata para 2 casas decimais
                "imc": f"{to_native(previsao_ia['imc']):.2f}",
                "classificacao_imc": previsao_ia["classificacao_imc"]
            }
        })

    @app.route("/ia/prever", methods=["POST"])
    def prever_ia():
        dados = request.json
        calorias_consumidas = dados.get("calorias_consumidas")
        atividade = dados.get("atividade", 2)
        peso = dados.get("peso")
        altura = dados.get("altura", 1.70) # Novo parâmetro 'altura' com valor padrão
        idade = dados.get("idade")
        sexo_str = dados.get("sexo", "M")
        sexo_int = 1 if sexo_str == "M" else 0
        massa_gorda = dados.get("massa_gorda", 25.0)

        # Chama a função de análise IA com o novo parâmetro 'altura'
        previsao = analisar_usuario(calorias_consumidas, atividade, peso, altura, idade, sexo_int, massa_gorda)

        # Retorna o JSON com os novos campos de previsão
        return jsonify({
            "usuario": {
                "peso": to_native(peso),
                "altura": to_native(altura),
                "atividade": to_native(atividade),
                "idade": to_native(idade),
                "sexo": sexo_str,
                "massa_gorda": to_native(massa_gorda)
            },
            "previsao_ia": {
                "tendencia": to_native(previsao["tendencia"]),
                "descricao": previsao["explicacao"],
                "peso_futuro_estimado": f"{to_native(previsao['peso_futuro_estimado']):.2f} kg",
                "imc": f"{to_native(previsao['imc']):.2f}",
                "classificacao_imc": previsao["classificacao_imc"]
            }
        })