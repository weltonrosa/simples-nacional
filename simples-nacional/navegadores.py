################################[ Cabeçalho ]##################################

'''
Módulo para abrir um website no navegador Chrome e autenticar-se nele.

Autor: Welton C. O. Rosa
Data: 02/04/2025

Ultima Atualização: 11/08/2025
Atualizado por: Welton C. O. Rosa

Versão: 1.0
Python Version: 3.9.7
Bibliotecas: selenium, webdriver_manager
Funções disponíveis: AbrirWebsite, autentica, fechar_navegador

Exemplo de uso:
    
        from navegador import Navegador
    
        # Cria uma instância da classe Navegador
        navegador = Navegador("chrome")
        
        # Abre o navegador e acessa o website
        navegador.abrir_navegador()
        
        # Fecha o navegador
        navegador.fechar_navegador() 
'''

###############################[ Bibliotecas ]##################################|

# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import logging
import os

#################################[   Log   ]#####################################|

# Configuração do logger
log_file_path = os.path.join(os.getcwd(), 'navegadores.log')    # Caminho absoluto para o arquivo de log
logging.basicConfig(
    filename=log_file_path,                                     # Nome do arquivo de log
    level=logging.INFO,                                         # Nível mínimo de log
    format='%(asctime)s - %(levelname)s - %(message)s'
)

#################################[ Classes ]####################################|

class Navegador:
    #def __init__(self, browser, url, login, senha):
    def __init__(self, navegador="chrome"):
        
        """
        Inicializa uma instância da classe Navegador.

        Parâmetros:
        browser (str): Nome do navegador a ser aberto.
        url (str): URL do website a ser aberto.
        login (str): Nome de usuário para autenticação.
        senha (str): Senha para autenticação.
        """
       
        self.navegador = navegador
        self.driver = None
        self.servico = None
        self.url = 'https://portal.uberaba.mg.gov.br/'
        self.login = None
        self.senha = None        

    def abrir_navegador(self):
        """
        Abre o navegador especificado
        """

        self.navegador = self.navegador.lower()

        # Verifica se o navegador é suportado
        if self.navegador not in ["chrome", "firefox", "edge", "opera","safari"]:
            print("Navegador não suportado.")
            logging.error(f"Navegador não suportado: {self.navegador}")
            return None
        
        # Verifica se o navegador já está aberto
        if self.driver is not None:
            print("O navegador já está aberto.")
            logging.warning("O navegador já está aberto.")
            return self.driver

        else:
            match self.navegador:
                case "chrome":
                    print(f"Iniciando o navegador {self.navegador}...")
                    logging.info(f"Iniciando o navegador {self.navegador}...")
                    # Configuração do ChromeOptions
                    #self.opcoes = webdriver.ChromeOptions()
                    self.opcoes = Options()                    
                    #self.opcoes.add_argument("--disable-gpu")  # Desativa o uso da GPU
                    #self.opcoes.add_argument("--disable-software-rasterizer")  # Desativa o rasterizador de software
                    #self.opcoes.add_argument("--disable-dev-shm-usage")  # Evita problemas de memória compartilhada
                    #self.opcoes.add_argument("--no-sandbox")  # Desativa o sandboxing
                    #self.opcoes.add_argument("--headless=new")  # Executa o navegador no modo headless (opcional)
                    self.opcoes.add_argument("--start-maximized")
                    self.opcoes.add_experimental_option("detach", True)                    
                    self.servico = Service(ChromeDriverManager().install()) # Configuração do serviço do ChromeDriver

                    # Inicialização do navegador Chrome
                    try:
                        self.driver = webdriver.Chrome(service=self.servico, options=self.opcoes)
                        print("Navegador iniciado com sucesso.")
                        logging.info("Navegador iniciado com sucesso.")
                        self.driver.get(self.url)  # Acessa a URL especificada
                        self.driver.implicitly_wait(10)  # Espera até 10 segundos para o website carregar
                    except Exception as e:
                        print(f"Erro ao inicializar o navegador: {e}")
                        logging.error(f"Erro ao inicializar o navegador: {e}")
                        self.driver = None
                    return self.driver
                

                case "firefox":
                    print(f"Iniciando o navegador {self.navegador}...")
                    logging.info(f"Iniciando o navegador {self.navegador}...")
                    self.opcoes = webdriver.FirefoxOptions()    # Configuração do FirefoxOptions
                    self.opcoes.add_argument("--start-maximized")
                    self.opcoes.add_argument("--disable-notifications")  # Desabilita notificações
                    self.opcoes.add_argument("--disable-default-apps")  # Desabilita aplicativos padrão
                    self.opcoes.add_argument("--disable-application-cache")  # Desabilita o cache de aplicações
                    self.opcoes.add_argument("--disable-translate")  # Desabilita a tradução

                    # Inicialização do navegador Firefox
                    try:
                        self.driver = webdriver.Firefox(service=self.servico, options=self.opcoes)
                        print(f"Navegador {self.navegador} iniciado com sucesso.")
                        logging.info(f"Navegador {self.navegador} iniciado com sucesso.")
                        self.opcoes.add_argument("--disable-sync")  # Desabilita a sincronização
                        self.driver.get(self.url)  # Acessa a URL especificada
                        self.driver.implicitly_wait(10)  # Espera até 10 segundos para o website carregar
                    except Exception as e:
                        print(f"Erro ao inicializar o navegador: {e}")
                        logging.warning(f"Erro ao inicializar o navegador {self.navegador}: {e}")
                        self.driver = None
                    return self.driver            

                case "edge":
                    print(f"Iniciando o navegador {self.navegador}...")
                    logging.info(f"Iniciando o navegador {self.navegador}...")
                    self.opcoes = webdriver.EdgeOptions()   # Configuração do EdgeOptions
                    self.opcoes.add_argument("--start-maximized")   # Maximiza a janela do navegador
                    self.opcoes.add_argument("--disable-notifications")  # Desabilita notificações
                    self.opcoes.add_experimental_option("detach", True) # Permite que o navegador permaneça aberto após o término do script
                    self.opcoes.add_argument("--disable-sync")  # Desabilita a sincronização

                    # Inicialização do navegador Edge
                    try:
                        self.driver = webdriver.Edge(options=self.opcoes)                        
                        print(f"Navegador {self.navegador} iniciado com sucesso.")
                        logging.info(f"Navegador {self.navegador} iniciado com sucesso.")
                        self.driver.get(self.url)  # Acessa a URL especificada
                        self.driver.implicitly_wait(10)  # Espera até 10 segundos para o website carregar
                    except Exception as e:
                        print(f"Erro ao inicializar o navegador: {e}")
                        logging.error(f"Erro ao inicializar o navegador {self.navegador}: {e}")
                        self.driver = None
                    return self.driver

                # Inicialização do navegador Opera
                case "opera":
                    print(f"Iniciando o navegador {self.navegador}...")
                    logging.info(f"Iniciando o navegador {self.navegador}...")
                    # Configuração do OperaOptions
                    self.opcoes = webdriver.OperaOptions()
                    self.opcoes.add_argument("--start-maximized")
                    self.opcoes.add_experimental_option("detach", True)

                    # Inicialização do navegador Opera
                    try:
                        self.driver = webdriver.Opera(options=self.opcoes)
                        print(f"Navegador {self.navegador} iniciado com sucesso.")
                        logging.info(f"Navegador {self.navegador} iniciado com sucesso.")
                        self.driver.get(self.url)  # Acessa a URL especificada
                        self.driver.implicitly_wait(10)  # Espera até 10 segundos para o website carregar
                    except Exception as e:
                        print(f"Erro ao inicializar o navegador: {e}")
                        logging.error(f"Erro ao inicializar o navegador {self.navegador}: {e}")
                        self.driver = None
                    return self.driver
                
                # Inicialização do navegador Safari
                case "safari":
                    print(f"Iniciando o navegador {self.navegador}...")
                    logging.info(f"Iniciando o navegador {self.navegador}...")
                    # Configuração do SafariOptions
                    self.opcoes = webdriver.SafariOptions()
                    self.opcoes.add_argument("--start-maximized")
                    self.opcoes.add_experimental_option("detach", True)

                    # Inicialização do navegador Safari
                    try:
                        self.driver = webdriver.Safari(options=self.opcoes)
                        print(f"Navegador {self.navegador} iniciado com sucesso.")
                        logging.info(f"Navegador {self.navegador} iniciado com sucesso.")
                        self.driver.get(self.url)  # Acessa a URL especificada
                        self.driver.implicitly_wait(10)  # Espera até 10 segundos para o website carregar
                    except Exception as e:
                        print(f"Erro ao inicializar o navegador: {e}")
                        logging.error(f"Erro ao inicializar o navegador {self.navegador}: {e}")
                        self.driver = None
                    return self.driver
    
    def fechar_navegador(self):
        """
        Função para fechar o navegador.

        Parâmetros:
        None

        Retorna:
        None
        """
        if self.driver is not None:
            self.driver.quit()
            print(f"Navegador {self.navegador} fechado com sucesso.")
            logging.warning(f"Navegador {self.navegador} fechado com sucesso.")
            self.driver = None
        else:
            print("O navegador não está aberto.")
            logging.warning("O navegador não está aberto.")
        return None
    
    def acessar_pagina(self, url):
        """
        Função para acessar uma página específica no navegador.

        Parâmetros:
        url (str): URL da página a ser acessada.

        Retorna:
        None
        """
        if self.driver is not None:
            self.driver.get(url)
            print(f"Acessando a página: {url}")
            logging.info(f"Acessando a página: {url}")
        else:
            print("O navegador não está aberto.")
            logging.warning("O navegador não está aberto.")
        return None
    
    def maximizar(self):
        """
        Função para maximizar a janela do navegador.

        Parâmetros:
        None

        Retorna:
        None
        """
        if self.driver is not None:
            self.driver.maximize_window()
            print("Janela do navegador maximizada.")
            logging.info("Janela do navegador maximizada.")
        else:
            print("O navegador não está aberto.")
            logging.warning("O navegador não está aberto.")
        return None
    
    def aguardar(self, segundos):
        """
        Função para aguardar um determinado número de segundos.

        Parâmetros:
        segundos (int): Número de segundos a aguardar.

        Retorna:
        None
        """
        if self.driver is not None:
            self.driver.implicitly_wait(segundos)
            print(f"Aguardando {segundos} segundos.")
            logging.info(f"Aguardando {segundos} segundos.")
        else:
            print("O navegador não está aberto.")
            logging.warning("O navegador não está aberto.")
        return None
    
    def clicar(self, by, valor):
        """
        Função para clicar em um elemento na página.

        Parâmetros:
        by (str): Método de localização do elemento (ID, XPATH, etc.).
        valor (str): Valor do método de localização.

        Retorna:
        None
        """
        if self.driver is not None:
            elemento = self.driver.find_element(by, valor)
            elemento.click()
            print(f"Clicando no elemento: {valor}")
            logging.info(f"Clicando no elemento: {valor}")
        else:
            print("O navegador não está aberto.")
            logging.warning("O navegador não está aberto.")
        return None
    
    def preencher(self, by, valor, texto):
        """
        Função para preencher um campo de texto na página.

        Parâmetros:
        by (str): Método de localização do elemento (ID, XPATH, etc.).
        valor (str): Valor do método de localização.
        texto (str): Texto a ser inserido no campo.

        Retorna:
        None
        """
        if self.driver is not None:
            elemento = self.driver.find_element(by, valor)
            elemento.send_keys(texto)
            print(f"Preenchendo o campo: {valor} com o texto: {texto}")
            logging.info(f"Preenchendo o campo: {valor} com o texto: {texto}")
        else:
            print("O navegador não está aberto.")
            logging.warning("O navegador não está aberto.")
        return None
    
    def mudar_frame(self, frame):
        """
        Função para mudar para um frame específico na página.

        Parâmetros:
        frame (str): Nome ou ID do frame a ser acessado.

        Retorna:
        None
        """
        if self.driver is not None:
            self.driver.switch_to.frame(frame)
            print(f"Mudando para o frame: {frame}")
            logging.info(f"Mudando para o frame: {frame}")
        else:
            print("O navegador não está aberto.")
            logging.warning("O navegador não está aberto.")
        return None

    def voltar_frame(self):
        """
        Função para voltar para o frame pai.

        Parâmetros:
        None

        Retorna:
        None
        """
        if self.driver is not None:
            self.driver.switch_to.default_content()
            print("Voltando para o frame pai.")
            logging.info("Voltando para o frame pai.")
        else:
            print("O navegador não está aberto.")
            logging.warning("O navegador não está aberto.")
        return None

    def aguardar_elemento(self, by, valor, timeout=10):
        """
        Aguarda até que um elemento esteja presente na página.

        Parâmetros:
        by (str): Método de localização do elemento (ex.: By.ID, By.CLASS_NAME, etc.).
        valor (str): Valor do método de localização (ex.: ID ou classe do elemento).
        timeout (int): Tempo máximo de espera em segundos. Padrão é 10 segundos.

        Retorna:
        WebElement: O elemento localizado, se encontrado dentro do tempo limite.
        """
        if self.driver is not None:
            try:
                wait = WebDriverWait(self.driver, timeout)
                elemento = wait.until(EC.presence_of_element_located((by, valor)))
                print(f"Elemento localizado: {valor}")
                logging.info(f"Elemento localizado: {valor}")
                return elemento
            except Exception as e:
                print(f"Erro ao localizar o elemento: {valor}. Detalhes: {e}")
                logging.error(f"Erro ao localizar o elemento: {valor}. Detalhes: {e}")
                return None
        else:
            print("O navegador não está aberto.")
            return None

    def encontrar_elemento(self, by, valor, multiplo=False):
        """
        Encontra um elemento na página.

        Parâmetros:
        by (str): Método de localização do elemento (ex.: By.ID, By.CLASS_NAME, etc.).
        valor (str): Valor do método de localização (ex.: ID ou classe do elemento).

        Retorna:
        WebElement: O elemento localizado.
        """
        if multiplo:
            #total_elementos += 1
            elementos = self.driver.find_elements(by, valor)
            print(f"Elementos encontrados: {valor}")
            logging.info(f"Elementos encontrados: {valor}")
            return elementos
        else:
            if self.driver is not None:
                elemento = self.driver.find_element(by, valor)
                print(f"Elemento encontrado: {valor}")
                logging.info(f"Elemento encontrado: {valor}")
                return elemento
            else:
                print("Elemento não encontrado ou o navegador não está aberto.")
                logging.warning("Elemento não encontrado ou o navegador não está aberto.")
                return None

#################################[ Funções ]####################################|


#################################[ Testes ]####################################|
""" 
if __name__ == "__main__":
    from console import Console
    
    url ='https://uberabamg.webiss.com.br/simples-nacional/acoes-fiscais'

    # Testa o navegador Google Chrome
    console = Console("Teste do Navegador Google Chrome")
    console.limpar_tela()
    console.exibir_titulo()
    console.exibir_mensagem("Iniciando o navegador...")
    navegador = Navegador("chrome")
    if navegador is not None:
        navegador.abrir_navegador()
        navegador.aguardar(10)
        input("Pressione Enter para continuar...")
        navegador.fechar_navegador()
    else:
        console.exibir_erro("Erro ao abrir o navegador Chrome.")

    
    # Testa o navegador Edge
    console = Console("Teste do Navegador Microsoft Edge")
    console.limpar_tela()
    console.exibir_titulo()
    console.exibir_mensagem("Iniciando o navegador...")
    navegador = Navegador("edge")
    if navegador is not None:
        navegador.abrir_navegador()
        navegador.aguardar(10)
        input("Pressione Enter para continuar...")
        navegador.fechar_navegador()
    else:
        console.exibir_erro("Erro ao abrir o navegador Edge.")

    # Testa o navegador Firefox
    console = Console("Teste do Navegador Firefox")
    console.limpar_tela()
    console.exibir_titulo()
    console.exibir_mensagem("Iniciando o navegador...")
    navegador = Navegador("firefox")
    if navegador is not None:
        navegador.abrir_navegador()
        navegador.aguardar(10)
        input("Pressione Enter para continuar...")
        navegador.fechar_navegador()
    else:
        console.exibir_erro("Erro ao abrir o navegador Firefox.") """
