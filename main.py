import json
import re
import http.client


arquivo_json = 'paciente.json'


def ler_arquivo_json(caminho):
    with open(caminho, 'r', encoding='utf-8') as file:
        dados = json.load(file)
        return dados


def limpar_cpf(cpf):
    return re.sub(r'\D', '', cpf)


paciente = ler_arquivo_json(arquivo_json)


print("Dados lidos do arquivo:", paciente) 
if 'firstName' not in paciente or 'lastName' not in paciente or 'cpf' not in paciente:
    print("Erro: Campos obrigatórios ausentes.")
else:
    
    paciente['fullName'] = paciente['firstName'] + " " + paciente['lastName']
    print("fullName criado:", paciente['fullName']) 

   
    paciente['cpf'] = limpar_cpf(paciente['cpf'])

   
    paciente.pop('firstName', None)  
    paciente.pop('lastName', None)   

   
    dados_json = json.dumps(paciente)

    
    host = 'localhost'
    port = 8080
    endpoint = '/cadastro-paciente'
    headers = {
        'Content-Type': 'application/json'
    }

    
    try:
        conn = http.client.HTTPConnection(host, port)

        
        conn.request("POST", endpoint, body=dados_json, headers=headers)

       
        response = conn.getresponse()
        response_data = response.read()

        
        if response.status == 200:
            print("Dados enviados com sucesso!")
            print("Resposta:", response_data.decode())
        else:
            print(f"Erro. Código: {response.status}")
            print("Resposta:", response_data.decode())
    except Exception as e:
        print(f"Erro na conexão: {e}")
    finally:
       
        conn.close()
