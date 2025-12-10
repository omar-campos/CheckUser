
import os
import subprocess
import sys
import socket
import urllib.request
import json

cor_vermelha = "\033[91m"
cor_verde = "\033[92m"
cor_amarela = "\033[93m"
cor_azul = "\033[94m"
cor_reset = "\033[0m"

def adicionar_ao_cache(chave, valor):
    cache = carregar_cache()  
    cache[chave] = valor
    salvar_cache(cache)  

def remover_do_cache(chave):
    cache = carregar_cache()  
    if chave in cache:
        del cache[chave]
        salvar_cache(cache) 

def obter_do_cache(chave):
    cache = carregar_cache()  
    return cache.get(chave)

def carregar_cache():
    try:
        with open('/root/checkuser/cache.json', 'r') as arquivo:
            return json.load(arquivo)
    except (FileNotFoundError, json.JSONDecodeError):
        return {} 
    
def salvar_cache(cache):
    with open('/root/checkuser/cache.json', 'w') as arquivo:
        json.dump(cache, arquivo)


def get_public_ip():
    try:
        url = "https://ipinfo.io"
        response = urllib.request.urlopen(url)
        if response.status == 200:
            data = json.loads(response.read().decode("utf-8"))
            if 'ip' in data:
                return data['ip']
            else:
                print("Endereço IP público não encontrado na resposta.")
                return None
        else:
            print("Falha na solicitação ao servidor.")
            return None
    except Exception as e:
        print("Não foi possível obter o endereço IP público:", str(e))
        return None




def verificar_processo(nome_processo):
    try:
        resultado = subprocess.check_output(["ps", "aux"]).decode()
        linhas = resultado.split('\n')
        for linha in linhas:
            if nome_processo in linha and "python" in linha:
                return True
    except subprocess.CalledProcessError as e:
        print(f"Erro ao verificar o processo: {e}")
    return False


nome_do_script = "/root/checkuser/checkuser.py"




if __name__ == "__main__":
    while True:
        os.system('clear')


        if verificar_processo(nome_do_script):
            status = f'{cor_verde}ativo{cor_reset} - {cor_amarela}porta em uso : {cor_reset}{cor_vermelha}{obter_do_cache("porta")}{cor_reset}'
        else:
            status = f'{cor_vermelha}parado{cor_reset} - {cor_amarela}porta em uso : {cor_reset}{cor_vermelha}{obter_do_cache("porta")}{cor_reset}'
       
        print(f"{cor_amarela}Status: {status}{cor_reset}")

        print(f"")

        print(f" {cor_vermelha}Selecione uma opção :{cor_reset}")
        print(f" {cor_verde} 1 - Matar porta 5454{cor_reset}")
        print(f" {cor_verde} 2 - Iniciar checkuser{cor_reset}")
        print(f" {cor_verde} 3 - Parar checkuser{cor_reset}")
        print(f" {cor_verde} 4 - Pegar o Link{cor_reset}")
        print(f" {cor_verde} 5 - Sobre{cor_reset}")
        print(f" {cor_verde} 6 - Desinstalar checkUser{cor_reset}")
        print(f" {cor_vermelha} 0 - Sair do menu{cor_reset}")
        print("")

        
        print(f" {cor_amarela} Digite a opção : {cor_reset}")
        option = input()

        if option == "1":
            print(f"\n {cor_vermelha} Porta 5454 liberada, volte ao menu e inicie o checkUser na porta 5454 {cor_reset}")
            command = "sudo kill -9 $(lsof -t -i:5454)"
            subprocess.run(command, shell=True)
            print(f"{cor_vermelha}\nPressione a tecla enter para voltar ao menu\n{cor_reset}")
            input()

        elif option == "2":
            print(f" {cor_vermelha} Observação: Para funcionar com security use a porta 5454 ! {cor_reset}")
            adicionar_ao_cache('porta', input("\n Digite a porta que deseja usar e de enter : "))
            os.system('clear')
            print(f'Porta escolhida: {obter_do_cache("porta")}')
            os.system(f'nohup python3 {nome_do_script} --port {obter_do_cache("porta")} & ')
            print(f"\n {cor_vermelha} Pressione a tecla enter para voltar ao menu\n\n {cor_reset}")
            input()

        elif option == "3":
            if verificar_processo(nome_do_script):
                try:
                    subprocess.run(f'pkill -9 -f "/root/checkuser/checkuser.py"', shell=True)
                except subprocess.CalledProcessError:
                    print("Erro ao executar o comando.")
                remover_do_cache("porta")
            else: 
                print(" {cor_vermelha} O Checkuser não está ativo.{cor_reset}")
            input(f" {cor_vermelha} Pressione a tecla enter para voltar ao menu {cor_reset}")

        elif option == "4":
            os.system('clear')
            if verificar_processo(nome_do_script):
                print(f" {cor_vermelha} Abaixo os apps, e os links para cada um : {cor_reset}")
                print("")
                ip = get_public_ip()
                porta = obter_do_cache("porta")
                print(f" {cor_amarela} Conecta4G/5G - http://{ip}:{porta}/checkUser{cor_reset} ")
                print(f" {cor_amarela} DtunnelMod - http://{ip}:{porta}/dtmod{cor_reset}  ")
                print(f" {cor_amarela} GltunnelMod - http://{ip}:{porta}/gl{cor_reset} ")
                print(f" {cor_amarela} AnyVpnMod - http://{ip}:{porta}/anymod{cor_reset} ")
                print(f" {cor_amarela} AtxTunnel - http://{ip}:{porta}/atx{cor_reset} ")
                print("")
                print(f" {cor_vermelha} Para usar com security (por favor, use apenas esses links com security e conexões que não usam cloudflare para não sobrecarregar nossos servidores){cor_reset}")
                print("")
                print(f" {cor_amarela}Link Conecta4G/5G abaixo :{cor_reset} ")
                print("")
                print(f"  {cor_verde}https://painelconecta5g.com/checkuser.php?url=http://{ip}:{porta}/checkUser{cor_reset} ")
                print("")
                print(f" {cor_amarela}Link DtunnelMod abaixo :{cor_reset} ")
                print("")
                print(f"  {cor_verde}https://painelconecta5g.com/checkuser.php?url=http://{ip}:{porta}/dtmod{cor_reset}  ")
                print("")
                print(f" {cor_amarela}Link GltunnelMod abaixo :{cor_reset} ")
                print("")
                print(f"  {cor_verde}https://painelconecta5g.com/checkuser.php?url=http://{ip}:{porta}/gl{cor_reset} ")
                print("")
                print(f" {cor_amarela}Link AnyVpnMod abaixo :{cor_reset} ")
                print("")
                print(f"  {cor_verde}https://painelconecta5g.com/checkuser.php?url=http://{ip}:{porta}/anymod{cor_reset} ")
                print("")
                print(f" {cor_amarela}Link AtxTunnel abaixo :{cor_reset} ")
                print("")
                print(f"  {cor_verde}https://painelconecta5g.com/checkuser.php?url=http://{ip}:{porta}/atx{cor_reset} ")
                print("")
                input(f" {cor_vermelha} Pressione a tecla enter para voltar ao menu {cor_reset}")
            else:
                print("\nInicie o serviço primeiro\n")
                print(f"\n {cor_vermelha} Pressione a tecla enter para voltar ao menu\n\n {cor_reset}")
            input()

        elif option == "5":
            os.system('clear')
            print(f"{cor_amarela}Olá, esse é um multi-checkuser criado por : {cor_reset}{cor_vermelha}@UlekBR{cor_reset}{cor_amarela} e melhorado por : {cor_reset} {cor_vermelha}\n@donomodderajuda{cor_reset}")
            print(f"{cor_amarela} Com esse checkuser venho trazendo a possibilidade de usar em diversos apps{cor_reset}")
            print(f"{cor_vermelha} Apps como : {cor_reset}")
            print(f" - Conecta4G/5G")
            print(f" - DtunnelMod")
            print(f" - GlTunnelMod")
            print(f" - AnyVpnMod")
            print(f"")
            print(f"{cor_vermelha} Pressione a tecla enter para voltar ao menu {cor_reset}")
            input()

        elif option == "6":
            os.system('clear')
            print(f"\n {cor_vermelha} checkUser Desinstalado {cor_reset}")
            commands = [
                "rm -rf /root/checkuser/",
                "rm -f /usr/local/bin/iniciar",
                "sudo kill -9 $(lsof -t -i:5454)",
                "pkill -9 -f /root/checkuser/checkuser.py"
                "cd"
            ]
            
            for command in commands:
                subprocess.run(command, shell=True)
            
            sys.exit(0)
        
        elif option == "0":
            sys.exit(0)
        
        else:
            os.system('clear')
            print(f"Selecionada uma opção inválida, tente novamente!")
            input(f"Pressione a tecla enter para voltar ao menu")
