# This file is part of https://github.com/jainamoswal/Flask-Example.
# Usage covered in <IDC lICENSE>
# Jainam Oswal. <jainam.me>
from .crash.crash_manager import (
    media_velas,
    fetch_contagem_cores,
    get_estrategias,
    fetch_velas,
    calculate_balance,
    _build_padroes
)

from .double.double_manager import (
    calculate_rolls_distribution,
    fetch_rolls,
    get_estrategias_double,
    calculate_balance_rolls
)

# Import Libraries
from app import app
from flask import jsonify, request
from flask_cors import cross_origin

# Define route "/api".
@app.route("/api")
def api():
    # return in JSON format. (For API)
    return jsonify({"message": "Hello from Flask!"})


@app.route("/api/<platform>/crash/dashboard")
@cross_origin()
def crashDashboard(platform):
    args = request.args
    qtd_velas = args.get("qtdVelas", default=200, type=int)
    qtd_galho = args.get("qtdGalho", default=0, type=int)
    target_vela = args.get("targetVela", default=2, type=int)
    min_probabilidade = args.get("minProbabilidade", default=50, type=int)
    padroes = args.getlist("padrao")

    descVelas = fetch_velas(platform, qtd_velas)
    ascVelas = list(reversed(descVelas))
    search_filter = {
        'velas': ascVelas,
        'qtd_velas': qtd_velas,
        'qtd_galho': qtd_galho,
        'target_vela': target_vela,
        'min_probabilidade': min_probabilidade,
        'padroes': padroes
    }

    # return in JSON format. (For API)

    result = dict()
    result["media_velas"] = media_velas(ascVelas)
    result["estrategias"] = get_estrategias(search_filter)
    result["contagem_cores"] = fetch_contagem_cores(ascVelas)
    result["velas"] = descVelas
    result['balance'] = calculate_balance(ascVelas)
    return jsonify(result)

@app.route("/api/<platform>/crash/padroes")
def crashPadroesProbabilidades(platform):
    args = request.args
    qtd_velas = args.get("qtdVelas", default=100, type=int)
    qtd_galho = args.get("qtdGalho", default=0, type=int)
    target_vela = args.get("targetVela", default=2, type=int)
    min_probabilidade = args.get("minProbabilidade", default=50, type=int)
    padroes = args.getlist("padrao")

    descVelas = fetch_velas(platform, qtd_velas)
    ascVelas = list(reversed(descVelas))
    search_filter = {
        'velas': ascVelas,
        'qtd_velas': qtd_velas,
        'qtd_galho': qtd_galho,
        'target_vela': target_vela,
        'min_probabilidade': min_probabilidade,
        'padroes': padroes
    }
    return _build_padroes(search_filter)


@app.route("/api/<platform>/double/dashboard")
@cross_origin()
def doubleDashboard(platform):

    args = request.args
    qtd_rolls = args.get("qtdRolls", default=200, type=int)
    qtd_galho = args.get("galho", default=2, type=int)
    min_probabilidade = args.get("minProbabilidade", default=0, type=int)
    target_color = args.get("targetColor", default='*', type=str)
    padroes = args.getlist("padrao")

    # return in JSON format. (For API)
    descRolls = fetch_rolls(platform, qtd_rolls)
    ascRolls = list(reversed(descRolls))

    result = dict()
    result["contagem_cores"] = calculate_rolls_distribution(descRolls)
    result["estrategias"] = get_estrategias_double(ascRolls, qtd_galho, padroes, min_probabilidade, target_color)
    result["rolls"] = descRolls
    result["balance"] = calculate_balance_rolls(ascRolls)
    
    return jsonify(result)

@app.route("/api/blaze/crash/delete/<qtd_velas>", methods=["DELETE"])
def delete(qtd_velas):
    # return in JSON format. (For API)

    velas = fetch_velas(qtd_velas)
    reversedVelas = list(reversed(velas))

    result = dict()
    result["media_intervalos"] = media_velas(reversedVelas)
    result["estrategias"] = get_estrategias(reversedVelas)
    result["contagem_cores"] = fetch_contagem_cores(reversedVelas)
    result["velas"] = velas
    return jsonify(result)
