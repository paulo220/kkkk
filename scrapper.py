import json
import time
import sys
import os
import random

from data import base_mk_buscas

from telethon import TelegramClient, connection, sync, events
from telethon.tl.functions.channels import JoinChannelRequest

#//--------------------------------------//#

def login(contas, contas_usadas = []):
  while len(contas_usadas) < len(contas):
    conta = random.choice(contas)
    try:
      if conta not in contas_usadas:
        print(conta)
        client = TelegramClient(conta["numero"], conta["api_id"], conta["api_hash"])
        client.start()
        return [client,
               conta]
    except Exception:
      if conta not in contas_usadas:
        contas_usadas.append(conta)

  return False

def reload(client, contas, conta):
  client.disconnect()
  return login(contas, contas_usadas = [conta])

def join(client, group):
  try:
    client(JoinChannelRequest(group))
  except Exception: return False
  return True

def leave(client, entity):
  try:
    client.delete_dialog(entity)
    client.disconnect()
  except Exception: return False
  return True

#//--------------------------------------//#

def main(token, key, message, group = [], bot_id = None, button_value = False, replace_value = False, replace_key = False):
  viewed = False
  message_sended = False
  process = True
  joined = False
  group = random.choice(group)

  errors = {
    '/foto': "Foto não encontrada!",
    '/cpf1_mk_buscas': "cpf não encontrado!",
    '/cpf2_mk_buscas': "cpf não encontrado!",
    '/cpf3_mk_buscas': "cpf não encontrado!",
    '/cpf4_mk_buscas': "cpf não encontrado!",
    '/score1_mk_buscas': "cpf não encontrado!",
    '/score2_mk_buscas': "cpf não encontrado!",
    '/parentes1_mk_buscas': "cpf não encontrado!",
    '/rg1_mk_buscas': "rg não encontrado!",
    '/vizinhos1_mk_buscas': "cpf não encontrado!",
    '/nascimento1_mk_buscas': "nascimento não encontrado!",
    '/tel1_mk_buscas': "número não encontrado!",
    '/tel2_mk_buscas': "número não encontrado!",
    '/tel3_mk_buscas': "número não encontrado!",
    '/nome1_mk_buscas': "nome não encontrado!",
    '/nome2_mk_buscas': "nome não encontrado!",
    '/placa1_mk_buscas': "placa não encontrada!",
    '/placa2_mk_buscas': "placa não encontrada!",
    '/cns1_acardian': "cns não encontradao",
    '/telefone_credilink': "Telefone não encontrado na base CREDILINK!"
  }

  obagui = message.split(" ")[1]
  if replace_value:
    message = message.replace(key, key+replace_value)
  if replace_key:
    message = message.replace(key, replace_key)
  #print(message)

  with open("login.json", "r") as f:
    _contas = f.read()
    contas = json.loads(_contas)

  response_login = login(contas)
  if not response_login:
    return {'status': 500, 'message': 'Erro no servidor!'}

  client = response_login[0]
  conta = response_login[1]

  while process:
    try:
      _join = join(client, group)
      if not _join:
        return {'status': 403, 'message': 'Erro ao entrar no grupo, verifique se sua conta foi banida mesmo. ( %s )' % group}

      entity = entity = client.get_entity(group)
      joined = True
    except Exception:
      response_login = reload(client, contas, conta)
      if not response_login:
        return {'status': 500, 'message': 'Erro no servidor!'}

      client = response_login[0]
      conta = response_login[1]

    if joined:
      try:
        client.send_message(entity = entity, message = message)
        message_sended = True
      except Exception:
        joined = False; message_sended = False

      if message_sended:
        try:
          timeout = time.time() + 30   # 30 segundos
          while True:
            messagess = client.get_messages(entity)
            if time.time() > timeout:
                msg = "tempo expirado tente novamente"
                break
            messages = client.get_messages(entity)[0]
            id = messages.from_id.user_id
            msg = messages.message
            if id == bot_id:
              if msg.__contains__(obagui.upper()):
               break
              elif msg.__contains__(obagui.lower()):
               break
              else:
               print(obagui)
               """
            for messages in messagess:
                id = messages.from_id.user_id
                msg = messages.message
                #print(msg)
                if message in msg:
                  print(msg)
                  if type(button_value) == int:
                    messages.click(button_value);time.sleep(3)
                    messagess = client.get_messages(entity)
                    for messages in messagess:
                        if message in msg:
                            msg = messages.message
                  break"""
          viewed = True
        except Exception:
          joined = False; message_sended = False

        if viewed:
          #match key:
            if key == "/foto":
              client.download_media(
                messages.media,
                "media/%s-foto.jpg" % token
              )
            #case "/telefone":
            #  client.download_media(
            #    messages.media,
            #    "media/%s-consulta.txt" % token
            #  )
          #try: messages.click(0)#;leave(client, entity)
          #except Exception: pass
        process = False
  try:
    #print(msg)
#    match key:
      if key == "/foto":
        response = foto.consulta(token, msg)
      elif key == "/cpf1_mk_buscas":
        response = base_mk_buscas.consulta(msg)
      elif key == "/cpf2_mk_buscas":
        response = base_mk_buscas.consulta(msg)
      elif key == "/cpf3_mk_buscas":
        response = base_mk_buscas.consulta(msg)
      elif key == "/cpf4_mk_buscas":
        response = base_mk_buscas.consulta(msg)
      elif key == "/score1_mk_buscas":
        response = base_mk_buscas.consulta(msg)
      elif key == "/score2_mk_buscas":
        response = base_mk_buscas.consulta(msg)
      elif key == "/parentes1_mk_buscas":
        response = base_mk_buscas.consulta(msg)
      elif key == "/rg1_mk_buscas":
        response = base_mk_buscas.consulta(msg)
      elif key == "/vizinhos1_mk_buscas":
        response = base_mk_buscas.consulta(msg)
      elif key == "/nascimento1_mk_buscas":
        response = base_mk_buscas.consulta(msg)
      elif key == "/tel1_mk_buscas":
        response = base_mk_buscas.consulta(msg)
      elif key == "/tel2_mk_buscas":
        response = base_mk_buscas.consulta(msg)
      elif key == "/tel3_mk_buscas":
        response = base_mk_buscas.consulta(msg)
      elif key == "/nome1_mk_buscas":
        response = base_mk_buscas.consulta(msg)
      elif key == "/nome2_mk_buscas":
        response = base_mk_buscas.consulta(msg)
      elif key == "/placa1_mk_buscas":
        response = base_mk_buscas.consulta(msg)
      elif key == "/placa2_mk_buscas":
        response = base_mk_buscas.consulta(msg)
      elif key == "/cns1_acardian":
        response = cns1_acardian.consulta(msg)
      elif key == "/telefone_credilink":
        return {"status": 500, "message": "Consulta Offline!"}
      msg = {"status": 200}
      msg["message"] = response
  except Exception as e:
    print("Erro no scrapper: %s" %e)
    msg = {'status': 400, 'message': errors[key]}

  return msg

def __init__(args):
  token = args[1]
  key = args[2]
  _message = ''
  for i in args[2:]:
    _message += (i + ' ')
  message = _message[:-1]

  #match key:
  if key == "/foto":
   _retorno = main(token, key, message, group = ["@consultas_fre"], bot_id = 5702074618, button_value = 0, replace_value = "@OnlyBuscasBot")
  elif key == "/cpf1_mk_buscas":
  	_retorno = main(token, key, message, group = ["@consultas_fre"], bot_id = 5702074618, button_value = False, replace_key = "/cpf1")
  elif key == "/cpf2_mk_buscas":
    _retorno = main(token, key, message, group = ["@consultas_fre"], bot_id = 5702074618, button_value = False, replace_key = "/cpf2")
  elif key == "/cpf3_mk_buscas":
    _retorno = main(token, key, message, group = ["@consultas_fre"], bot_id = 5702074618, button_value = False, replace_key = "/cpf3")
  elif key == "/cpf4_mk_buscas":
    _retorno = main(token, key, message, group = ["@consultas_fre"], bot_id = 5702074618, button_value = False, replace_key = "/cpf4")
  elif key == "/score1_mk_buscas":
    _retorno = main(token, key, message, group = ["@consultas_fre"], bot_id = 5702074618, button_value = False, replace_key = "/score")
  elif key == "/score2_mk_buscas":
    _retorno = main(token, key, message, group = ["@consultas_fre"], bot_id = 5702074618, button_value = False, replace_key = "/scorecpf")
  elif key == "/parentes1_mk_buscas":
    _retorno = main(token, key, message, group = ["@consultas_fre"], bot_id = 5702074618, button_value = False, replace_key = "/parentes")
  elif key == "/rg1_mk_buscas":
    _retorno = main(token, key, message, group = ["@consultas_fre"], bot_id = 5702074618, button_value = False, replace_key = "/rg")
  elif key == "/vizinhos1_mk_buscas":
    _retorno = main(token, key, message, group = ["@consultas_fre"], bot_id = 5702074618, button_value = False, replace_key = "/vizinhos")
  elif key == "/nascimento_mk_buscas":
    _retorno = main(token, key, message, group = ["@consultas_fre"], bot_id = 5702074618, button_value = False, replace_key = "/nascimento")
  elif key == "/tel1_mk_buscas":
    _retorno = main(token, key, message, group = ["@consultas_fre"], bot_id = 5702074618, button_value = False, replace_key = "/tel1")
  elif key == "/tel2_mk_buscas":
    _retorno = main(token, key, message, group = ["@consultas_fre"], bot_id = 5702074618, button_value = False, replace_key = "/tel2")
    elif key == "/tel3_mk_buscas":
    _retorno = main(token, key, message, group = ["@consultas_fre"], bot_id = 5702074618, button_value = False, replace_key = "/tel3")
  elif key == "/nome1_mk_buscas":
    _retorno = main(token, key, message, group = ["@consultas_fre"], bot_id = 5702074618, button_value = False, replace_key = "/nome")
  elif key == "/nome2_mk_buscas":
    _retorno = main(token, key, message, group = ["@consultas_fre"], bot_id = 5702074618, button_value = False, replace_key = "/nome1")
  elif key == "/nome3_mk_buscas":
    _retorno = main(token, key, message, group = ["@consultas_fre"], bot_id = 5702074618, button_value = False, replace_key = "/nome2")
  elif key == "/placa1_mk_buscas":
    _retorno = main(token, key, message, group = ["@consultas_fre"], bot_id = 5702074618, button_value = False, replace_key = "/placa1")
  elif key == "/placa2_mk_buscas":
    _retorno = main(token, key, message, group = ["@consultas_fre"], bot_id = 5702074618, button_value = False, replace_key = "/placa2")
  elif key == "/cns1_acardian":
    _retorno = main(token, key, message, group = ["@Consultas_Aqui","@Consultas4","@CONSULTAS_CADSUS"], bot_id = 1747207086, button_value = False, replace_key = "/cns1")
  elif key == "/telefone_credilink":
    _retorno = main(token, key, message, group = ["@tropadolux"], bot_id = 5225772947, button_value = 3, replace_value = "@OnlyBuscasBot", replace_key = "/telefone")
  else:
      _retorno = {'status': 402, 'message': 'Consulta Off-line!'}
  retorno = json.dumps(_retorno, indent = 4, sort_keys = True)

  with open("consultas/%s-consulta.json" % token, "w+") as f:
    return f.write(retorno)

#//--------------------------------------//#

if __name__ == '__main__':
  __init__(sys.argv)
 
