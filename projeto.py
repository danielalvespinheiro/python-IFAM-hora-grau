import time as tm
import csv
import os
import matplotlib.pyplot as plt
#import pandas as pd

# Área de carregar arquivos e salvar arquivos
def carregar_bestiario():
    bestiario = {'especie': [], 'horas_grau': []}

    try:
        with open("bestiario.csv", "r", newline='') as arquivoBestiario:
            leitor = csv.reader(arquivoBestiario, delimiter=';')
            next(leitor)  
            for linha in leitor:
                if len(linha) == 3:
                    try:
                        hora_min = int(linha[1])
                        hora_max = int(linha[2])
                        bestiario['especie'].append(linha[0])
                        bestiario['horas_grau'].append((hora_min, hora_max))
                    except ValueError:
                        continue
    except FileNotFoundError:
        print(newCor("Arquivo 'bestiario.csv' não encontrado! Criando um novo arquivo.", "amarelo"))
        with open("bestiario.csv", "w", newline='') as arquivoBestiario:
            escritor = csv.writer(arquivoBestiario, delimiter=';')
            escritor.writerow(['especie', 'hora_min', 'hora_max'])

    return bestiario

def carregar_lixeira():
    lixeira = {'especie': [], 'horas_grau': []}

    try:
        with open("lixeira.csv", "r", newline='') as arquivo_lixeira:
            leitor = csv.reader(arquivo_lixeira, delimiter=';')
            next(leitor)  # Pula o cabeçalho
            for linha in leitor:
                if len(linha) == 3:
                    try:
                        hora_min = int(linha[1])
                        hora_max = int(linha[2])
                        lixeira['especie'].append(linha[0])
                        lixeira['horas_grau'].append((hora_min, hora_max))
                    except ValueError:
                        continue
    except FileNotFoundError:
        print(newCor("Arquivo 'lixeira.csv' não encontrado! Criando um novo arquivo.", "amarelo"))
        with open("lixeira.csv", "w", newline='') as arquivo_lixeira:
            escritor = csv.writer(arquivo_lixeira, delimiter=';')
            escritor.writerow(['especie', 'hora_min', 'hora_max'])

    return lixeira

def salvar_bestiario(bestiario):
    with open("bestiario.csv", "w", newline='') as arquivoBestiario:
        escritor = csv.writer(arquivoBestiario, delimiter=';')
        escritor.writerow(['especie', 'hora_min', 'hora_max'])
        for i in range(len(bestiario['especie'])):
            escritor.writerow([
                bestiario['especie'][i],
                bestiario['horas_grau'][i][0],
                bestiario['horas_grau'][i][1]
            ])

def salvar_lixeira(lixeira):
    with open("lixeira.csv", "w", newline='') as arquivo_lixeira:
        escritor = csv.writer(arquivo_lixeira, delimiter=';')
        escritor.writerow(['especie', 'hora_min', 'hora_max'])
        for i in range(len(lixeira['especie'])):
            escritor.writerow([
                lixeira['especie'][i],
                lixeira['horas_grau'][i][0],
                lixeira['horas_grau'][i][1]
            ])

# Área de listar especies, Modificar Especies e Deletar Especies

def listar_especies(bestiario, resp):
    
    if len(bestiario['especie']) == 0:
        print(newCor("\nNenhuma espécie cadastrada ainda", "amarelo"))
        return
    print(f"\nRegistros De Bestiário: ")
    for i in range(len(bestiario['especie'])):
        print(f"{bestiario['especie'][i]}: Horas Graus entre {bestiario['horas_grau'][i][0]} e {bestiario['horas_grau'][i][1]}")

    resp = input(newCor("\nPrecione qualquer tecla para voltar ao menu: ", "cyano_claro"))
    if(resp == ""):
        return 

def modificar_especie(bestiario):
    print(newCor("\nEspécies disponíveis para modificação:", "azul"))
    for especie in bestiario['especie']:
        print(f"- {especie}")
    nome_modificar = input("\nDigite o nome da espécie que deseja modificar: ").lower()
    indice = -1
    
    for i in range(len(bestiario['especie'])):
        especie = bestiario['especie'][i]
        if len(nome_modificar) == len(especie):
            iguais = True
            for j in range(len(nome_modificar)):
                letra1 = nome_modificar[j]
                letra2 = especie[j]

                if letra1 != letra2:
                    if (letra1 >= "A" and letra1 <= "Z" and letra1 != letra2.upper()) or \
                       (letra1 >= "a" and letra1 <= "z" and letra1 != letra2.lower()):
                        iguais = False
                        break

            if iguais:
                indice = i
                break

    if indice >= 0:
        hg_min_atual, hg_max_atual = bestiario['horas_grau'][indice]
        print(f"\nValores atuais para {especie}:")
        print(f"Hora-grau mínima: {hg_min_atual}")
        print(f"Hora-grau máxima: {hg_max_atual}")
        horamin = input(newCor("\nDigite a nova hora-grau mínima: ", "azul"))
        horamax = input(newCor("Digite a nova hora-grau máxima: ", "azul"))
        for digito in horamin + horamax:
            if digito < '0' or digito > '9':
                print(newCor("Por favor, digite apenas números! ", "vermelho"))
                return
        bestiario['horas_grau'][indice] = (int(horamin), int(horamax))
        salvar_bestiario(bestiario)
        print(f"\nHoras-grau da espécie {especie} modificadas com sucesso!")
        print(f"Novos valores: mínima = {horamin}, máxima = {horamax}")
    else:
        print(f"\nEspécie {nome_modificar} não encontrada!")

def deletar_especie(bestiario, lixeira):
    if len(bestiario['especie']) == 0:
        print(newCor("\nNenhuma espécie cadastrada para deletar! ", "amarelo"))
        return
    
    print(newCor("\nEspécies disponíveis: ", "amarelo"))
    for i in range(len(bestiario['especie'])):
        print(f"{i+1}. {bestiario['especie'][i]}")
    
    try:
        nome_deletar = input(newCor("\nDigite o nome da espécie para deletar: ", "azul")).lower()
        indice = -1
        
        for i in range(len(bestiario['especie'])):
            especie = bestiario['especie'][i]
            if len(nome_deletar) == len(especie):
                iguais = True
                for j in range(len(nome_deletar)):
                    letra1 = nome_deletar[j]
                    letra2 = especie[j]

                    if letra1 != letra2:
                        if (letra1 >= "A" and letra1 <= "Z" and letra1 != letra2.upper()) or \
                           (letra1 >= "a" and letra1 <= "z" and letra1 != letra2.lower()):
                            iguais = False
                            break

                if iguais:
                    indice = i
                    break

        if indice >= 0:
            especie = bestiario['especie'][indice]
            horas_grau = bestiario['horas_grau'][indice]
            lixeira['especie'].append(especie)
            lixeira['horas_grau'].append(horas_grau)
            nova_lista_especies = []
            nova_lista_horas = []
            
            for i in range(len(bestiario['especie'])):
                if i != indice:
                    nova_lista_especies.append(bestiario['especie'][i])
                    nova_lista_horas.append(bestiario['horas_grau'][i])
            
            bestiario['especie'] = nova_lista_especies
            bestiario['horas_grau'] = nova_lista_horas
            
            print(newCor(f"\nEspécie {especie} deletada com sucesso!", "verde "))
            salvar_bestiario(bestiario)
            salvar_lixeira(lixeira)
        else:
            print(f"\nEspécie {nome_deletar} não encontrada!")
    except ValueError:
        print("\nPor favor, digite um nome válido!")

# Área de cadastrar especies, calcular e tempo de desova e criar grafico
def cadastrar_especie(bestiario):
    respUso = "S"
    while respUso == 'S' or respUso == 's' or respUso == 'sim' or respUso == 'Sim' or respUso == 'SIM' or respUso == 'y' or respUso == 'yes' or respUso == 'Yes' or respUso == 'Y':
        peixe1 = input(newCor("Digite o nome da espécie: ", "azul"))

        if not peixe1.isalpha():
            print(newCor("Digite um valor válido para o nome do peixe, use letras e não números! ", "red"))
            continue
        
        if (peixe1.lower() in (especie.lower() for especie in bestiario['especie'])):
            print()
            print("O peixe que você digitou ja existe")
            continue

        horamin = input(newCor("Digite a hora-grau mínima: ", "azul_claro"))
        horamax = input(newCor("Digite a hora-grau máxima: ", "azul_claro"))
        
        if not (horamin.isdigit() and horamax.isdigit()):
            print(newCor("Por favor, digite apenas números para as horas-grau! " ,"amarelo"))
            return False
        
        bestiario['especie'].append(peixe1)
        bestiario['horas_grau'].append((int(horamin), int(horamax)))
        print(newCor(f"\nEspécie {peixe1} cadastrada com sucesso! ", "verde"))
        salvar_bestiario(bestiario)
        respUso = input(newCor("Quer continuar, digite S para sim ou N para não: ", "amarelo"))

    if(respUso == "N" or respUso == "n"):
        print("Ok, operação finalizada!")
        return

def calcular_tempo_desova(bestiario):
    if len(bestiario['especie']) == 0:
        print(newCor("Nenhuma espécie cadastrada ainda!\n ", "amarelo"))
        return
    
    print(newCor("\nEspécies disponíveis: ", "azul"))
    for especie in bestiario['especie']:
        print(f"\033[1;94m- {especie}\033[1;94m")
    
    nome = input(newCor("\nDigite o nome da espécie: ", "azul")).lower()
    indice = -1
    
    for i in range(len(bestiario['especie'])):
        especie = bestiario['especie'][i]
        if len(nome) == len(especie):
            iguais = True
            for j in range(len(nome)):
                letra1 = nome[j]
                letra2 = especie[j]

                if letra1 != letra2:
                    if (letra1 >= "A" and letra1 <= "Z" and letra1 != letra2.upper()) or \
                       (letra1 >= "a" and letra1 <= "z" and letra1 != letra2.lower()):
                        iguais = False
                        break

            if iguais:
                indice = i
                break
    
    if indice >= 0:
        hg_min, hg_max = bestiario['horas_grau'][indice]
        total_hora_grau = 0
        num_afericoes = 0
        
        temperaturas = []
        horas = []
        horas_grau_acumulado = []
        
        print(newCor(f"\nA hora-grau mínima para a espécie {nome} é {hg_min}. ", "verde"))
        
        while total_hora_grau < hg_min:
            num_afericoes += 1
            temperatura = input(newCor(f"Digite a temperatura da água na {num_afericoes}ª aferição (em °C): ", "azul"))
            
            if not temperatura.isdigit():
                print(newCor("\nTemperatura inválida! Digite apenas números. ", "vermelho"))
                return
            
            temperatura = int(temperatura)
            hora_grau = num_afericoes + temperatura  
            total_hora_grau += hora_grau
            
            temperaturas.append(temperatura)
            horas.append(num_afericoes)
            horas_grau_acumulado.append(total_hora_grau)
            
            print(f"\nAferição {num_afericoes}: Hora-grau = {hora_grau} (Temperatura: {temperatura}°C)")
            print(f"Total acumulado de Hora-Grau: {total_hora_grau}")

        print(newCor(f"Total de Hora-Grau para a espécie {nome}: {total_hora_grau} (mínimo: {hg_min})\n ", "azul"))
        print(newCor(f"A espécie {nome} atingiu um total de hora-grau de {total_hora_grau} e iniciou o período de reprodução.\n ", "verde"))

        while total_hora_grau < hg_max:
            num_afericoes += 1
            temperatura = input(newCor(f"Digite a temperatura da água na {num_afericoes}ª aferição (em °C): ", "azul"))
            if not temperatura.isdigit():
                print(newCor("\nTemperatura inválida! Digite apenas números. ", "vermelho"))
                return
            
            temperatura = int(temperatura)
            hora_grau = num_afericoes + temperatura  
            total_hora_grau += hora_grau
            
            temperaturas.append(temperatura)
            horas.append(num_afericoes)
            horas_grau_acumulado.append(total_hora_grau)
            
            print(f"\nAferição {num_afericoes}: Hora-grau = {hora_grau} (Temperatura: {temperatura}°C) ")
            print(f"Total acumulado de Hora-Grau: {total_hora_grau}")
            print(f"\nTotal de Hora-Grau para a espécie {nome}: {total_hora_grau} (maximo: {hg_max})")
        
        print(newCor(f"\nA espécie {nome} atingiu um total de hora-grau de {total_hora_grau} e finalizou o período de reprodução. ", "vermelho"))
        
        gerar_grafico_afericoes(nome, temperaturas, horas, horas_grau_acumulado, hg_min, hg_max)
    else:
        print(newCor(f"\nEspécie {nome} não encontrada! ", "vermelho"))

def gerar_grafico_afericoes(especie, temperaturas, horas, horas_grau_acumulado, hg_min, hg_max):
    plt.style.use('default')
    plt.figure(figsize=(12, 6), facecolor='white')
    plt.gca().set_facecolor('white')
    plt.plot(horas, temperaturas, marker='o', color='blue', linewidth=2)
    plt.title(f'Temperatura da Água por Hora - {especie.capitalize()}', pad=20, fontsize=12)
    plt.xlabel('Hora da Aferição', fontsize=10)
    plt.ylabel('Temperatura (°C)', fontsize=10)
    plt.grid(True, linestyle='--', alpha=0.3)
    y_min = min(temperaturas) - 5
    y_max = max(temperaturas) + 5
    plt.ylim(y_min, y_max)
    plt.tight_layout()
    
    plt.show()

# Área De Padronização De Cores e Menu Inicial e Limpar Terminal
def newCor(palavras, cor):
    cores = {
        "azul":"\033[1;34m",
        "azul_claro":"\033[94m",
        "vermelho":"\033[31m",
        "verde":"\033[1;32m",
        "amarelo":"\033[1;33m",
        "cinza_escuro":"\033[1;90m",
        "cyano_claro":"\033[1;96m",
    }

    resetar_fonte = "\033[0m"
    return cores.get(cor.lower(), '') + palavras + resetar_fonte

# FUNÇÃO DE LIMPAR O TERMINAL AQUI
contador = 0

def limpar_terminal():
    os.system('cls' if os.name == 'nt' else 'clear')    

def menuInicial():
    while True:
        bestiario = carregar_bestiario()
        lixeira = carregar_lixeira()

        global contador
        contador = contador + 1
        # Limpa o terminal a cada 3 operações
        if(contador % 2 == 0):
            limpar_terminal()

        print()
        print(newCor(f"========= Menu =========", "verde"))
        print(" ----------------------------------------- ")
        print("|                                          |")
        print("|    1. Cadastrar Espécie                  |")
        print("|    2. Calcular Tempo de reprodução       |")
        print("|    3. Listar Espécie                     |")
        print("|    4. Modificar Espécie                  |")
        print("|    5. Deletar Espécie                    |")
        print("|    6. Sair                               |")
        print("|                                          |")
        print(" ----------------------------------------- ")    

        tm.sleep(0.5)
        print()
        opcao = input(newCor("Escolha uma opção: ", ""))

        if opcao == '1':
            tm.sleep(0.5)
            print()
            cadastrar_especie(bestiario)
            tm.sleep(0.5)
            
        elif opcao == '2':
            tm.sleep(0.5)
            calcular_tempo_desova(bestiario)
            tm.sleep(0.5)

        elif opcao == '3':
            respLista = ""
            tm.sleep(0.5)
            listar_especies(bestiario, respLista)
            tm.sleep(0.5)

        elif opcao == '4':
            tm.sleep(0.5)
            print()
            modificar_especie(bestiario)
            tm.sleep(0.5)

        elif opcao == '5':
            tm.sleep(0.5)
            print()
            deletar_especie(bestiario, lixeira)
            tm.sleep(0.5)

        elif opcao == '6':
            print()
            print(newCor("Finalizando o programa!", "verde"))
            print()
            break

        else:
            print()
            tm.sleep(0.5)
            print(newCor("Opção inválida! Tente novamente.", "vermelho"))
            tm.sleep(0.5)
            print()

menuInicial()