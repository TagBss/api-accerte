from flask import Flask, request, jsonify
import requests
from datetime import datetime

app = Flask(__name__)

@app.route('/dadosfin', methods=['GET'])
def consultar_dados_financeiros():
    # Parâmetros da URL
    data_ini = request.args.get("data_ini")
    data_fim = request.args.get("data_fim")

    if not data_ini or not data_fim:
        return jsonify({"erro": "Parâmetros data_ini e data_fim são obrigatórios"}), 400

    # Converte de 'YYYY-MM-DD' para 'DD/MM/YYYY'
    try:
        data_ini_fmt = datetime.strptime(data_ini, "%Y-%m-%d").strftime("%d/%m/%Y")
        data_fim_fmt = datetime.strptime(data_fim, "%Y-%m-%d").strftime("%d/%m/%Y")
    except ValueError:
        return jsonify({"erro": "Datas devem estar no formato YYYY-MM-DD"}), 400

    # Etapa 1: login
    login_url = "https://api.sankhya.com.br/login"
    login_headers = {
        "token": "f017da56-c57e-48f5-91a3-1558bab3bd47",
        "appkey": "43f26c9e-a806-42fc-a75d-bdbf2ef4e62b",
        "username": "controladoria@tagbss.com",
        "password": "TAG@2024",
        "Content-Type": "application/json"
    }

    login_resp = requests.post(login_url, headers=login_headers)
    login_data = login_resp.json()
    token = login_data.get("bearerToken")

    if not token:
        return jsonify({"erro": "Falha no login", "detalhes": login_data}), 401

    # Etapa 2: consulta
    consulta_url = "https://api.sankhya.com.br/gateway/v1/mge/service.sbr?serviceName=CRUDServiceProvider.loadView&outputType=json"
    consulta_headers = {
        "Authorization": f"Bearer {token}",
        "appkey": "43f26c9e-a806-42fc-a75d-bdbf2ef4e62b",
        "Content-Type": "application/json"
    }

    consulta_body = {
        "serviceName": "CRUDServiceProvider.loadView",
        "requestBody": {
            "query": {
                "viewName": "VW_DADOSFIN_ACC",
                "fields": {
                    "field": {
                        "$": (
                            "ORIGEM, CODTIPOPER, TOPORIGEM, CODEMPRESA, NOMEEMPRESA, CODBANCO, NOMEBANCO, RECEITADESPESA, "
                            "DTNEGOCIACAO, DTCOMPETENCIA, DTVENCIMENTO, VLRFINANCEIRO, VLRBAIXA, DHBAIXA, CODINTERNOCONTA, "
                            "CODIGOCONTA, CONTABANCARIA, NRONOTAFISCAL, NUMEROBOLETO, OBSERVACAO, PROJETO, IDENTIFICACAO, CODIGOCR, NOMECR, "
                            "CODIGONATUREZA, NOMENATUREZA, TOPDEBAIXA, NOMETOPBAIXA, NUFIN, CODPARCEIROSECUNDARIO, "
                            "PARCEIROSECUNDARIO, PARCEIRO, NOMEPARCEIRO, VERTICAL"
                        )
                    }
                },
                "where": {
                    "$": f"DTNEGOCIACAO BETWEEN '{data_ini_fmt}' AND '{data_fim_fmt}'"
                },
                "start": 0,
                "limit": 500
            }
        }
    }

    consulta_resp = requests.post(consulta_url, headers=consulta_headers, json=consulta_body)
    
    if consulta_resp.status_code == 200:
        return jsonify(consulta_resp.json())
    else:
        return jsonify({
            "erro": "Erro ao consultar a view",
            "status": consulta_resp.status_code,
            "resposta": consulta_resp.text
        }), consulta_resp.status_code
    

@app.route('/dadosBanc', methods=['GET'])
def movimento_bancario():
    # Parâmetros da URL
    data_ini = request.args.get("data_ini")
    data_fim = request.args.get("data_fim")

    if not data_ini or not data_fim:
        return jsonify({"erro": "Parâmetros data_ini e data_fim são obrigatórios"}), 400

    # Converte de 'YYYY-MM-DD' para 'DD/MM/YYYY'
    try:
        data_ini_fmt = datetime.strptime(data_ini, "%Y-%m-%d").strftime("%d/%m/%Y")
        data_fim_fmt = datetime.strptime(data_fim, "%Y-%m-%d").strftime("%d/%m/%Y")
    except ValueError:
        return jsonify({"erro": "Datas devem estar no formato YYYY-MM-DD"}), 400

    # Etapa 1: login
    login_url = "https://api.sankhya.com.br/login"
    login_headers = {
        "token": "f017da56-c57e-48f5-91a3-1558bab3bd47",
        "appkey": "43f26c9e-a806-42fc-a75d-bdbf2ef4e62b",
        "username": "controladoria@tagbss.com",
        "password": "TAG@2024",
        "Content-Type": "application/json"
    }

    login_resp = requests.post(login_url, headers=login_headers)
    login_data = login_resp.json()
    token = login_data.get("bearerToken")

    if not token:
        return jsonify({"erro": "Falha no login", "detalhes": login_data}), 401

    # Etapa 2: consulta
    consulta_url = "https://api.sankhya.com.br/gateway/v1/mge/service.sbr?serviceName=CRUDServiceProvider.loadView&outputType=json"
    consulta_headers = {
        "Authorization": f"Bearer {token}",
        "appkey": "43f26c9e-a806-42fc-a75d-bdbf2ef4e62b",
        "Content-Type": "application/json"
    }

    
    consulta_body = {
            "serviceName": "CRUDServiceProvider.loadView",
            "requestBody": {
                "query": {
                    "viewName": "VW_DADOSMBC_ACC",
                    "fields": {
                        "field": {
                            "$": (
                                "TIPOMOVIMENTO, NROUNICO, VLRLANCAMENTO, DTLANCAMENTO, LANCAMENTOORIGEM, CONTAORIGEM, "
                                "LANCAMENTODESTINO, CONTADEST, HISTORICO "
                            )
                        }
                    },
                    "where": {
                        "$": f"DTLANCAMENTO BETWEEN '{data_ini_fmt}' AND '{data_fim_fmt}'"
                    },
                    "start": 0,
                    "limit": 500
                }
            }
        }

    consulta_resp = requests.post(consulta_url, headers=consulta_headers, json=consulta_body)
    
    if consulta_resp.status_code == 200:
        return jsonify(consulta_resp.json())
    else:
        return jsonify({
            "erro": "Erro ao consultar a view",
            "status": consulta_resp.status_code,
            "resposta": consulta_resp.text
        }), consulta_resp.status_code
    

@app.route('/impostoFaturamento', methods=['GET'])
def consultar_imposto_faturamento():
    # # Parâmetros da URL
    # data_ini = request.args.get("data_ini")
    # data_fim = request.args.get("data_fim")

    # if not data_ini or not data_fim:
    #     return jsonify({"erro": "Parâmetros data_ini e data_fim são obrigatórios"}), 400

    # # Converte de 'YYYY-MM-DD' para 'DD/MM/YYYY'
    # try:
    #     data_ini_fmt = datetime.strptime(data_ini, "%Y-%m-%d").strftime("%d/%m/%Y")
    #     data_fim_fmt = datetime.strptime(data_fim, "%Y-%m-%d").strftime("%d/%m/%Y")
    # except ValueError:
    #     return jsonify({"erro": "Datas devem estar no formato YYYY-MM-DD"}), 400

    # Etapa 1: login
    login_url = "https://api.sankhya.com.br/login"
    login_headers = {
        "token": "f017da56-c57e-48f5-91a3-1558bab3bd47",
        "appkey": "43f26c9e-a806-42fc-a75d-bdbf2ef4e62b",
        "username": "controladoria@tagbss.com",
        "password": "TAG@2024",
        "Content-Type": "application/json"
    }

    login_resp = requests.post(login_url, headers=login_headers)
    login_data = login_resp.json()
    token = login_data.get("bearerToken")

    if not token:
        return jsonify({"erro": "Falha no login", "detalhes": login_data}), 401

    # Etapa 2: consulta
    consulta_url = "https://api.sankhya.com.br/gateway/v1/mge/service.sbr?serviceName=CRUDServiceProvider.loadView&outputType=json"
    consulta_headers = {
        "Authorization": f"Bearer {token}",
        "appkey": "43f26c9e-a806-42fc-a75d-bdbf2ef4e62b",
        "Content-Type": "application/json"
    }

    
    consulta_body = {
       "serviceName": "CRUDServiceProvider.loadView",
       "requestBody": {
           "query": {
               "viewName": "VW_DADOSIMPFIN_ACC",
               "fields": {
                   "field": {
                       "$": (
                           "CODEMP, DTCOMPETENCIA, VLRFATURADOREC, PIS, COFINS, IRPJ, "
                           "CSLL, VLRFATURADODESP, DIFFAT, ADDIRPJ"
                       )
                   }
               },
               "where": {
                   "$": f"1=1"
               },
               "start": 0,
               "limit": 500
           }
       }
   }

    consulta_resp = requests.post(consulta_url, headers=consulta_headers, json=consulta_body)
    
    if consulta_resp.status_code == 200:
        return jsonify(consulta_resp.json())
    else:
        return jsonify({
            "erro": "Erro ao consultar a view",
            "status": consulta_resp.status_code,
            "resposta": consulta_resp.text
        }), consulta_resp.status_code


@app.route('/lucroPresumido', methods=['GET'])
def lucro_presumido():
    # # Parâmetros da URL
    # data_ini = request.args.get("data_ini")
    # data_fim = request.args.get("data_fim")

    # if not data_ini or not data_fim:
    #     return jsonify({"erro": "Parâmetros data_ini e data_fim são obrigatórios"}), 400

    # # Converte de 'YYYY-MM-DD' para 'DD/MM/YYYY'
    # try:
    #     data_ini_fmt = datetime.strptime(data_ini, "%Y-%m-%d").strftime("%d/%m/%Y")
    #     data_fim_fmt = datetime.strptime(data_fim, "%Y-%m-%d").strftime("%d/%m/%Y")
    # except ValueError:
    #     return jsonify({"erro": "Datas devem estar no formato YYYY-MM-DD"}), 400

    # Etapa 1: login
    login_url = "https://api.sankhya.com.br/login"
    login_headers = {
        "token": "f017da56-c57e-48f5-91a3-1558bab3bd47",
        "appkey": "43f26c9e-a806-42fc-a75d-bdbf2ef4e62b",
        "username": "controladoria@tagbss.com",
        "password": "TAG@2024",
        "Content-Type": "application/json"
    }

    login_resp = requests.post(login_url, headers=login_headers)
    login_data = login_resp.json()
    token = login_data.get("bearerToken")

    if not token:
        return jsonify({"erro": "Falha no login", "detalhes": login_data}), 401

    # Etapa 2: consulta
    consulta_url = "https://api.sankhya.com.br/gateway/v1/mge/service.sbr?serviceName=CRUDServiceProvider.loadView&outputType=json"
    consulta_headers = {
        "Authorization": f"Bearer {token}",
        "appkey": "43f26c9e-a806-42fc-a75d-bdbf2ef4e62b",
        "Content-Type": "application/json"
    }

    
    consulta_body = {
       "serviceName": "CRUDServiceProvider.loadView",
       "requestBody": {
           "query": {
               "viewName": "VW_DADOSIMPFIN_TRIM_ACC",
               "fields": {
                   "field": {
                       "$": (
                           "CODEMP, ANO, VLRFAT_Q1, VLRFAT_Q2, VLRFAT_Q3, VLRFAT_Q4, "
                           "IRPJ_Q1, IRPJ_Q2, IRPJ_Q3, IRPJ_Q4 "
                       )
                   }
               },
               "where": {
                   "$": f"1=1"
               },
               "start": 0,
               "limit": 500
           }
       }
   }

    consulta_resp = requests.post(consulta_url, headers=consulta_headers, json=consulta_body)
    
    if consulta_resp.status_code == 200:
        return jsonify(consulta_resp.json())
    else:
        return jsonify({
            "erro": "Erro ao consultar a view",
            "status": consulta_resp.status_code,
            "resposta": consulta_resp.text
        }), consulta_resp.status_code

if __name__ == '__main__':
    app.run(debug=True)


