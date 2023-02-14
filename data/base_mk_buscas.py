def consulta(msg):
  #dados = {}
  dados = ""
  ################
  #dados["result"] = msg.split("• USUÁRIO:")[0]
  dados += msg.split("👤 BY:")[0].split("BY:")[0].split("👤 USUÁRIO:")[0]

  ################
  return dados
