################################[ Cabeçalho ]##################################
'''
Classe Console para exibir mensagens e opções no console. 
Esta classe é útil para criar interfaces de linha de comando mais amigáveis e organizadas.

Autor: Welton C. O. Rosa
Data: 02/04/2025

Ultima Atualização: 11/08/2025
Atualizado por: Welton C. O. Rosa

Versão: 1.0
Python Version: 3.9.7
Bibliotecas: os
Funções disponíveis: limpar_tela, exibir_titulo, exibir_mensagem, exibir_erro, exibir_opcoes
'''
###############################[ Bibliotecas ]##################################|
# -*- coding: utf-8 -*-

import os
import time
import logging

#################################[   Log   ]#####################################|

# Configuração do logger
log_file_path = os.path.join(os.getcwd(), 'consoles.log')  # Caminho absoluto para o arquivo de log
logging.basicConfig(
    filename=log_file_path,                                 # Nome do arquivo de log
    level=logging.INFO,                                     # Nível mínimo de log
    format='%(asctime)s - %(levelname)s - %(message)s'
)

#################################[ Classes ]####################################|

class Console:
    def __init__(self, titulo):
        self.titulo = titulo
        self.largura = 80  # Largura padrão do console
        self.limpar_tela()

    def limpar_tela(self):
        """Limpa a tela do console."""
        os.system('cls' if os.name == 'nt' else 'clear')

    def exibir_titulo(self):
        """Exibe o título formatado no console."""
        self.limpar_tela()
        print("=" * self.largura)
        print(f"{self.titulo:^{self.largura}}")
        print("=" * self.largura)
        print("\n")

    def exibir_mensagem(self, mensagem, linhas=0):
        """Exibe uma mensagem no console."""
        print(mensagem)
        if linhas > 0:
            for _ in range(linhas):
                print("\n")

    def exibir_mensagem_piscando(self, mensagem, duracao=5, intervalo=0.5):
        """
        Exibe uma mensagem piscando no console.

        Parâmetros:
        mensagem (str): A mensagem a ser exibida.
        duracao (int): Duração total em segundos que a mensagem ficará piscando.
        intervalo (float): Intervalo em segundos entre cada piscada.
        """
        tempo_inicial = time.time()
        while time.time() - tempo_inicial < duracao:
            # Exibe a mensagem
            print(mensagem, end="\r", flush=True)
            time.sleep(intervalo)  # Aguarda o intervalo
            # Apaga a mensagem
            print(" " * len(mensagem), end="\r", flush=True)
            time.sleep(intervalo)  # Aguarda o intervalo
        print(f"{mensagem}\n")  # Move para a próxima linha após terminar 
    
    def exibir_erro(self, erro):
        """Exibe uma mensagem de erro no console."""
        print(f"Erro: {erro}")
        print("\n")
        logging.error(f"Erro: {erro}")


#################################[ Testes ]####################################|
#Exemplo de uso da classe Console
#if __name__ == "__main__":

    #console = Console("Teste")  # Cria uma instancia e atribui o título do console
    #console.exibir_titulo()     # Exibe o título formatado no console
    #console.exibir_mensagem("Bem-vindo ao meu console!")    # Exibe uma mensagem no console
    #console.exibir_opcoes(["Opção 1", "Opção 2", "Opção 3", "Opção 4"])  # Exibe opções no console
    #console.exibir_erro("Você selecionou a opção errada!")  # Exibe uma mensagem de erro no console
    #console.exibir_mensagem_piscando("Esta mensagem piscará durante 5 segundos!", duracao=5, intervalo=0.5) # Exibe uma mensagem piscando no console
    #input("Pressione Enter para continuar...")
    #console.limpar_tela()       # Limpa a tela do console

    #console = Console("Menu de Opções")  # Cria uma instância da classe Console
    #console.exibir_titulo()  # Exibe o título formatado no console

    # Define as opções disponíveis
    #opcoes = ["Cadastrar usuário", "Listar usuários", "Excluir usuário", "Sair"]

    # Exibe as opções no console
    #console.exibir_opcoes(opcoes)

    # Obtém a opção escolhida pelo usuário
    #opcao_escolhida = console.obter_opcao(opcoes, mensagem="Digite o número da opção desejada: ")

    # Exibe a opção escolhida
    #console.exibir_mensagem(f"Você escolheu: {opcao_escolhida}")
