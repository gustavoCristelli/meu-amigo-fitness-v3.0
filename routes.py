#routes.py

from flask import request, jsonify
from models import db, Usuario, RegistroDiario
from logic import analisar_registro, analisar_usuario
import numpy as np

def to_native(x):
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
        atividade = dados.get("atividade", 2)
        peso_atual = dados.get("peso_atual", 70)
        calorias_consumidas = dados.get("calorias_consumidas", 2000)
        calorias_gastas = dados.get("calorias_gastas", 300)
        idade = dados.get("idade", 30)
        sexo = dados.get("sexo", "M")
        massa_gorda = dados.get("massa_gorda", 25.0)

        registro = RegistroDiario(
            usuario_id=usuario_id,
            calorias_consumidas=calorias_consumidas,
            calorias_gastas=calorias_gastas
        )
        db.session.add(registro)
        db.session.commit()

        saldo_calorico = calorias_consumidas - calorias_gastas
        resposta_analise = analisar_registro(calorias_consumidas, calorias_gastas)
        previsao_ia = analisar_usuario(
            calorias_consumidas,
            atividade,
            peso_atual,
            idade,
            1 if sexo == "M" else 0,
            massa_gorda
        )

        return jsonify({
            "mensagem": "Registro salvo com sucesso!",
            "usuario": {k: to_native(v) for k, v in {
                "id": usuario_id,
                "peso_atual": peso_atual,
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
                "descricao": previsao_ia["explicacao"]
            }
        })

    @app.route("/ia/prever", methods=["POST"])
    def prever_ia():
        dados = request.json
        calorias_consumidas = dados.get("calorias_consumidas")
        atividade = dados.get("atividade", 2)
        peso = dados.get("peso")
        idade = dados.get("idade")
        sexo = 1 if dados.get("sexo", "M") == "M" else 0
        massa_gorda = dados.get("massa_gorda", 25.0)

        previsao = analisar_usuario(calorias_consumidas, atividade, peso, idade, sexo, massa_gorda)

        return jsonify({
            "usuario": {
                "peso": to_native(peso),
                "atividade": to_native(atividade),
                "idade": to_native(idade),
                "sexo": "M" if sexo == 1 else "F",
                "massa_gorda": to_native(massa_gorda)
            },
            "previsao_ia": {
                "tendencia": to_native(previsao["tendencia"]),
                "descricao": previsao["explicacao"]
            }
        })
