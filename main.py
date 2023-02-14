import os
import json
import shutil
import requests
import random
import telethon
import time

from logging import exception
from flask import Flask, request, jsonify, json

app = Flask(__name__)


def delLogs():
    try:
        shutil.rmtree("./consultas")
        os.mkdir("consultas")
        shutil.rmtree("./data/__pycache__")
        output = open(f"logs.json", 'w+')
        output.write(f" ")
    except:
        pass


def gen_cod(digitos):
    chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789"
    gerado = ''.join((random.choice(chars) for i in range(int(digitos))))
    return gerado


def api_check(key):
    f = open(f"users.json", 'r').read()
    if f"<apikey >{key}< apikey>" in f:
        return "sim"
    else:
        return "nao"


def consulta(key, msg):
    token = gen_cod(4)
    os.system("python3 scrapper.py %s %s %s" % (token, key, msg))
    with open(f'consultas/{token}-consulta.json') as f:
        resultado_consulta = json.load(f)
    return resultado_consulta


def base_rand(txt, str):
    base = txt.split(f'<label>{str}</label>\n')[1].split('value="')[1].split(
        '">')[0]
    return base


def consulta2(key1, consul, apikey):
    key = api_check(apikey)
    if "sim" in key:
        resultado_consulta = consulta(key1, consul)
        return resultado_consulta
    else:
        base = {}
        base['message'] = "api key incorreta"
        base['status'] = 404
        return base


def emailzap(msg, numero, apikey):
    key = api_check(apikey)
    token = gen_cod(8)
    if "sim" in key:
        headers = {
            "accept": "*/*",
            "accept-language":
            "pt-BR,pt;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
            "content-type": "application/x-www-form-urlencoded",
            "sec-ch-ua":
            "\"Microsoft Edge\";v=\"105\", \" Not;A Brand\";v=\"99\", \"Chromium\";v=\"105\"",
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": "\"Windows\"",
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-origin",
            "x-fb-lsd": "AVoWN9dj_eI",
            "cookie":
            "wa_lang_pref=pt_br; wa_ul=bf660112-58bc-4987-b2f0-ad53d37f230a; wa_csrf=AXp1yyyUxoNTykan6ResRG",
            "Referer":
            "https://www.whatsapp.com/contact/?lang=pt_br&subject=messenger",
            "Referrer-Policy": "origin-when-cross-origin"
        }

        data = f"jazoest=2959&lsd=AVoWN9dj_eI&email=kauannre%2B{token}%40gmail.com&email_confirm=kauannre%2B{token}%40gmail.com&your_message={msg}&phone_number={numero}&country_selector=BR&platform=WHATS_APP_WEB_DESKTOP&step=submit&__user=0&__a=1&__dyn=7wKwkHgmwn8K2WnFwn84a2i5U4e1Fx-ewSwMxW0SU1nEhwem0nCq1ewcG0KE33w8G1nzU1vrzo5-0me220qu0L8ly82swdq0Ho2ewnE3fw6iw4vwbS1Lw&__csr=&__req=6&__hs=19244.BP%3Awhatsapp_www_pkg.2.0.0.0.0&dpr=1&__ccg=UNKNOWN&__rev=1006169347&__s=mw8cuv%3A1j1npk%3A49l3j9&__hsi=7141191074928423409&__comet_req=0"
        test = requests.post("https://www.whatsapp.com/contact/noclient/async/", headers=headers, data=data).text
        if "seu contato" in test:
            base = {}
            base['message'] = "email enviado para o suporte"
            base['status'] = 200
            return base
        else:
            base = {}
            base['message'] = "erro interno"
            base['status'] = 404
            return base
    else:
        base = {}
        base['message'] = "api key incorreta"
        base['status'] = 404
        return base


@app.route(f"/")
def ok():
    return "tem interesse na api? me chama no PV e adquira, meu número: +55 12 99222-5031"

@app.route(f"/checkstatus")
def pobre():
  return "Online"

@app.errorhandler(404)
def page_not_found(e):
    result = {}
    result['message'] = "url nao encontrado quer comprar a api, fale com o Paulo: wa.me/5511934713306"
    result['status'] = 404
    return result, 404


@app.route(f"/admin/reiniciar_logs/nexusadminn")
def reiniciar_logs():
    delLogs()
    result = {}
    result['message'] = "Logs reiniciados."
    result['status'] = 200
    return result


@app.route(f"/admin/reiniciar_users/nexusadminn")
def reiniciar_users():
    output = open(f"users.json", 'w+')
    output.write(f"")
    result = {}
    result['message'] = "users reiniciados"
    result['status'] = 200
    return result


@app.route(f"/admin/add_user/<usuario>/<senha>/<apikey>/nexusadminn")
def add_usuario(usuario, senha, apikey):
    f = open(f"users.json", 'r').read()
    if '<usuario>{usuario}<usuario>' not in f:
        result1 = {}
        result1['message'] = f"usuario {usuario} adicionado."
        result1['status'] = 200
        result = f"<id {usuario}>\n<usuario>{usuario}<usuario>\n<apikey >{apikey}< apikey>\n<senha>{senha}<senha>\n <{usuario} id>\n"
        output = open(f"users.json", "a")
        output.write(f"{result}")
        return result1
    else:
        result1 = {}
        result1['message'] = f"usuario {usuario} ja esta na minha db."
        result1['status'] = 200
        return


@app.route(f"/admin/see_usuarios/nexusadminn")
def ver_cliente1():
    f = open(f"users.json", 'r').read()
    result = {}
    result['message'] = f
    result['status'] = 200
    return result


@app.route(f"/admin/see_log/nexusadminn")
def ver_log():
    f = open(f"logs.json", 'r').read()
    result = {}
    result['message'] = f
    result['status'] = 200
    return result


@app.route(f"/api/check_user/<login>/<senha>")
def check_user(login, senha):
    f = open(f"users.json", 'r').read()
    base = {}
    if f'<usuario>{login}<usuario>' and f'<senha>{senha}<senha>' not in f:
        base['message'] = "invalido"
        base['status'] = 404
        return base
    else:
        re = f.split(f"<id {login}>")[1].split(f"<{login} id>\n")[0]
        re2 = re.split(f"<apikey >")[1].split(f"< apikey>")[0]
        base['message'] = f"{re2}"
        base['status'] = 200
        return base


@app.route(f"/admin/remove_user/<id>/nexusadminn")
def remover_cliente(id):
    testt = open(f"users.json", 'r').read()
    if f'<usuario>{id}<usuario>' in testt:
        f = open(f"users.json", 'r').read()
        b = open(f"users.json", 'r').read()
        re = f.split(f"<id {id}>")[0]
        re1 = b.split(f"<{id} id>\n")[1]
        re2 = f"{re}{re1}"
        output = open(f"users.json", "w+")
        output.write(f"{re2}")
        result = {}
        result['message'] = "usuario removido"
        result['status'] = 200
        return result
    else:
        result1 = {}
        result1['message'] = f"usuario {usuario} nao esta na minha fb."
        result1['status'] = 200
        return result1

    # CONSULTAS CPF base MK Buscas


@app.route(f"/api")
def teste():
    consult = request.args.get('consult')
    if consult:
        return consult
    else:
        return "status: ok"


@app.route(f"/api/consultas")
def consultas():
    consult = request.args.get('consult')
    apikey = request.args.get('apikey')
    msg = request.args.get('msg')
    bases_mk = [
        "cpf1", "cpf2", "cpf3", "cpf4", "score1", "score2", "parentes1", "rg1",
        "nascimento1", "vizinhos1", "tel1", "tel2", "tel3", "nome1", "nome2", "nome3", "placa1",
        "placa2"
    ]
    if consult and apikey and msg:
        if consult in bases_mk:
            # consultas mk buscas
            key1 = f"/{consult}_mk_buscas"
            result = consulta2(key1, msg, apikey)
            return result
        else:
            return "não existe essa base"
    else:
        return "falta alguns parametros ai"


# CONSULTA CNS


@app.route(f"/api/consultas/cns1/<cns>/<apikey>")
def cns1_acardian(cns, apikey):

    key = api_check(apikey)
    if "sim" in key:
        token = gen_cod(4)
        key = "/cns1_acardian"
        msg = cpf
        os.system("python3 scrapper.py %s %s %s" % (token, key, msg))
        with open(f'consultas/{token}-consulta.json') as f:
            resultado_consulta = json.load(f)
        return resultado_consulta
    else:
        base = {}
        base['message'] = "api key incorreta"
        base['status'] = 404
        return base


# CONSULTA DC


@app.route(f"/api/discord/msgsend/<msg>/<channelid>/<token>/<apikey>")
def spam_msgdc(msg, channelid, token, apikey):

    key = api_check(apikey)
    if "sim" in key:
        headers = {
            "content-type":
            "application/json",
            "authorization":
            token,
            "User-Agent":
            "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:77.0) Gecko/20190101 Firefox/77.0"
        }
        json = {"content": msg}
        re = requests.post(
            f"https://discordapp.com/api/v7/channels/{channelid}/messages",
            headers=headers,
            json=json).json()
        base = {}

        if 'message' in re:
            base['message'] = f"token/id nao encontrados"
            base['status'] = 404
            return base
        else:
            base[
                'message'] = f"MENSAGEM: {msg}\nID DO SERVER/PESSOA: {channelid}"
            base['status'] = 200
            return base
    else:
        base = {}
        base['message'] = "api key incorreta"
        base['status'] = 404
        return base


# ENVIAR EMAIL PRO ZAP


@app.route(f"/api/zap")
def zapzap():
    consult = request.args.get('consult')
    apikey = request.args.get('apikey')
    numero = request.args.get('numero')
    if consult and apikey and numero:
        if consult == "sendemail":
            msg = request.args.get('msg')
            if msg:
                result = emailzap(msg, numero, apikey)
                return result
            else:
                return "ta faltando um parametro ai"
        elif consult == "resetcod1":
            msg = f"Por favor desativem minha conta numero: {numero}"
            result = emailzap(msg, numero, apikey)
            return result
        elif consult == "deslog1":
            msg = f"Por favor desativem minha conta numero: {numero}"
            testee = {}
            txtt = ''
            for i in range(20):
              result = emailzap(msg, numero, apikey)
              resposta = result['message']
              txtt += f'{resposta} \n'
            txtt += '20 tentativas de deslogar esse numero, se não deslogou tente novamente'
            testee['message'] = txtt
            return testee
        elif consult == "analise1":
            msg = f"Hello whatsapp support! My account was deactivated unfairly, please reactivate my number: {numero}"
            result = emailzap(msg, numero, apikey)
            return result
        elif consult == "analise1":
            msg = f"Hello whatsapp support! My account was deactivated unfairly, please reactivate my number: {numero}"
            result = emailzap(msg, numero, apikey)
            return result
        elif consult == "ban1":
            alvo = request.args.get('alvo')
            if alvo:
                msg = f"Olá estou sofrendo ameaças de um usuário de whatsapp imune, {alvo} esse é o número do usuário, ele está me fazendo ameaças constantes e estou com medo de perder meu número ou até mesmo meu aparelho celular"
                testee = {}
                txtt = ''
                for i in range(20):
                  result = emailzap(msg, numero, apikey)
                  resposta = result['message']
                  txtt += f'{resposta} \n'
                txtt += '20 tentativas de banir esse numero, se não baniu tente novamente'
                testee['message'] = txtt
                return testee
            else:
                return "ta faltando um parametro ai"
        else:
            return "não existe essa base"
    else:
        return "ta daltando alguns parametros ai"


@app.route(f"/api/random/jidszap/<apikey>")
def gerar_jids(apikey):
    key = api_check(apikey)
    if "sim" in key:
        base = {}
        teste = ''
        for i in range(100000, 999999):
            teste += f'{i}@s.whatsapp.net,+'
        upp = teste.split('+')
        upi = ''.join(random.choice(upp)
                      for i in range(45000)) + '0@s.whatsapp.net'
        base['message'] = upi
        base['status'] = 200
        return base
    else:
        base = {}
        base['message'] = "api key incorreta"
        base['status'] = 404
        return base


@app.route(f"/api/random/dados/<apikey>")
def gerar_dados(apikey):

    key = api_check(apikey)
    if "sim" in key:
        data = 'gender=&country=BR'
        while True:
            re = requests.get("https://www.invertexto.com/gerador-de-pessoas",
                              data=data).text
            teste = base_rand(re, "CPF").count("-")
            if teste == 1:
                break
        data = {}
        # dados pessoais
        data['pessoal_nome'] = base_rand(re, "Nome")
        data['pessoal_cpf'] = base_rand(re, "CPF")
        data['pessoal_telefone'] = base_rand(re, "Telefone")
        # nascimento
        data['nasc_data_nasc'] = base_rand(re, "Data de Nascimento")
        # endereco
        data['endereco_cep'] = base_rand(re, "CEP")
        data['endereco_endereco'] = base_rand(re, "Endereço")
        data['endereco_cidade'] = base_rand(re, "Cidade")
        data['endereco_estado'] = base_rand(re, "Estado")
        # online
        data['online_email'] = base_rand(re, "E-Mail")
        data['online_nome_usuario'] = base_rand(re, "Nome de Usuário")
        data['online_senha'] = base_rand(re, "Senha")
        # cc
        data['cc_bandeira'] = base_rand(re, "Bandeira")
        data['cc_numero'] = base_rand(re, "Número")
        data['cc_data'] = base_rand(re, "Expiração")
        data['cc_cvv'] = base_rand(re, "CVV2")
        return data
    else:
        base = {}
        base['message'] = "api key incorreta"
        base['status'] = 404
        return base


app.run(host="0.0.0.0", port=2000, debug=True)
