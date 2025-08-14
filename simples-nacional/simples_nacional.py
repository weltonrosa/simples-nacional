###############################[  Cabeçalho  ]###################################|

'''

Descrição: Esta biblioteca possui um conjunto de funções que permitem automatizar consultas de informações
sobre débitos de empresas do Simples Nacional pelo site da Receita Federal.

Autor: Welton C. O. Rosa
Data: 05/05/2025

<<<<<<< HEAD
Ultima Atualização: 12/08/2025
=======
Ultima Atualização: 08/08/2025
>>>>>>> e77c940cafd5b1663f8aa221179b99075ca41f83
Atualizado por: Welton C. O. Rosa

Versão: 1.0
Python Version: 3.13.0
Bibliotecas: Console, Navegador, Planilha
Clases: SimplesNacional
Funções disponíveis: ConsultaDebitos, Valida_CNPJ, processar_dados
Requisitos:
* Navegador Chrome instalado;

Pendências: 
* Criar folha em planilha para CNPJs inválidos;
* Adicionar opções para salvar arquivo de saída nos formatos .xlsx e .csv;
* Adcionar opções para abrir arquivo de lista no formato .csv;
* Registrar o total de tempo da conclusão do processo.
* Adicionar funcionalidade de pausar e continuar o processo.
* Adicionar funcionalidade de cancelar o processo durante a execução com 
  possibilidade de salvar os dados capturados.
* Corrigir lista de erros a baixo.
* Total de CNPJs

Erros apresentados durante a execução:
* Alteração dos valores definidos na data final.
* Não segue realizando consultas após a apresentação do erro: 
  "Não existem débitos para este CNPJ".
* Campo CNPJ em branco durante o preechimento automatizado.
* Impossível interromper o script durante a execução.
* Impossível salvar os dados obtidos, se o processo não seguir até o final.

'''

###############################[ Bibliotecas ]###################################|

# -*- coding: utf-8 -*-
import os
import re
import openpyxl
import pandas as pd
import logging
from tabulate import tabulate
#from time import sleep
#from random import random
from console import Console
from navegadores import Navegador
# from planilhas import Planilha
from datetime import datetime
from selenium.webdriver.common.by import By

#################################[   Log   ]#####################################|

# Configuração do logger
log_file_path = os.path.join(os.getcwd(), 'simples_nacional.log')   # Caminho absoluto para o arquivo de log
logging.basicConfig(
    filename=log_file_path,                                         # Nome do arquivo de log
    level=logging.INFO,                                             # Nível mínimo de log
    format='%(asctime)s - %(levelname)s - %(message)s'
)

###############################[   Classes   ]###################################|

class SimplesNacional():
    def __init__(self):
        console = Console("Simples Nacional")
        logging.info("Iniciando a classe SimplesNacional.")
        pass

    def Valida_CNPJ(cnpj):
        logging.info(f"Validando CNPJ: {cnpj}")
        cnpj = re.sub(r'[^0-9]', '', cnpj)   # Remove caracteres não numéricos
        sequencia = cnpj[0] * len(cnpj)      # Cria uma sequência de números iguais
        REGRESSIVOS = [6, 5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]

        if sequencia == cnpj or len(cnpj) != 14:
            return False

        # Calcula o primeiro dígito verificador
        soma = 0
        for i in range(12):
            soma += int(cnpj[i]) * REGRESSIVOS[i + 1]
        resto = soma % 11
        digito1 = 0 if resto < 2 else 11 - resto
        if int(cnpj[12]) != digito1:
            return False

        # Calcula o segundo dígito verificador
        soma = 0
        for i in range(13):
            soma += int(cnpj[i]) * REGRESSIVOS[i]
        resto = soma % 11
        digito2 = 0 if resto < 2 else 11 - resto
        if int(cnpj[13]) != digito2:
            logging.warning(f"CNPJ {cnpj} é inválido.")
            return False
        logging.info(f"CNPJ {cnpj} é válido.")
        return True
    
    def Processar_Dados(self, dados_brutos, arquivo_saida):
        logging.info("Iniciando o processamento dos dados coletados.")
        # Cria o DataFrame
        df = pd.DataFrame(dados_brutos, columns=['CNPJ', 'Apuração', 'Vencimento', 
                                                 'Inclusão', 'VL. Originário(R$)', 
                                                 'Saldo Devedor(R$)', 'Parcelamento', 
                                                 'Ind CT Exc'])

        # Exclui as linhas onde a coluna 'Inclusão' que contém 'Total:'
        df_filtrado = df[~df['Inclusão'].str.contains('Total:', na=False)]

        # Exclui todas as linhas onde a coluna 'Saldo Devedor(R$)' = 0 e 'Parcelamento' =''
        df_filtrado['VL. Originário(R$)'] = df_filtrado['VL. Originário(R$)'].str.replace('.', '', regex=False).str.replace(',','.',regex=False).astype(float).round(2)
        df_filtrado['Saldo Devedor(R$)'] = df_filtrado['Saldo Devedor(R$)'].str.replace('.', '', regex=False).str.replace(',','.',regex=False).astype(float).round(2)
        df_filtrado = df_filtrado[(df_filtrado['Saldo Devedor(R$)'] >= 0.00)]
        df_filtrado = df_filtrado[(df_filtrado['Saldo Devedor(R$)'] > 0.00) | (df_filtrado['Parcelamento'] != '')]

        total_valor_originario = sum(df_filtrado['VL. Originário(R$)'].round(2))
        total_saldo_devedor = sum(df_filtrado['Saldo Devedor(R$)'].round(2))

        # Formata os valores para exibição com separadores de milhares
        df_filtrado_tela = df_filtrado.copy()
        df_filtrado_tela['VL. Originário(R$)'] = df_filtrado['Saldo Devedor(R$)'].apply(lambda x: f"{x:,.2f}")
        df_filtrado_tela['Saldo Devedor(R$)'] = df_filtrado['Saldo Devedor(R$)'].apply(lambda x: f"{x:,.2f}")

        console = Console("Simples Nacional")
        console.limpar_tela()
        console.exibir_mensagem("\nDados filtrados:")
        console.exibir_mensagem(tabulate(df_filtrado_tela, headers=df.columns, tablefmt='psql', showindex=False), 0)
        console.exibir_mensagem(f"Total VL. Originário: R$ {total_valor_originario:.2f}", 0)
        console.exibir_mensagem(f"Total Saldo Devedor: R$ {total_saldo_devedor:.2f}", 1)
        logging.info(f"Total VL. Originário: R$ {total_valor_originario:.2f}")
        logging.info(f"Total Saldo Devedor: R$ {total_saldo_devedor:.2f}")

        resposta = ""
        while resposta not in ["S", "N"]:
            resposta = input(f"Deseja salvar a pesquisa? <S/N>: ").upper()
            if resposta == "S":
                df_filtrado.to_excel(arquivo_saida, index=False)
                console.exibir_mensagem(f"Planilha salva com sucesso em {os.path.abspath(arquivo_saida)}", 1)
                logging.info(f"Planilha salva com sucesso em {os.path.abspath(arquivo_saida)}")
            elif resposta == "N":
                console.exibir_mensagem("Planilha não salva.", 1)
                logging.warning("Planilha não salva.")
                df_filtrado = pd.DataFrame()  # Limpa o DataFrame filtrado
            else:
                console.exibir_mensagem("Resposta inválida. Digite S ou N.", 1)
                logging.warning("Resposta inválida fornecida pelo usuário.")

        return df_filtrado  # Retorna o DataFrame filtrado para uso posterior


    def ConsultaDebitos(self, data_inicio=None, data_final=None, lista=None, cnpj=None,
                         inicio=0, fim=0, arquivo_leitura=None, arquivo_saida=None, tempo_espera=5):
        data_inicio = data_inicio if data_inicio is not None else datetime.now().strftime("%m/%Y")   # Se a data de início for None, define como mês e ano atual
        data_final = data_final if data_final is not None else datetime.now().strftime("%m/%Y")      # Se a data final for None, define como mês e ano atual
        lista = lista if lista is not None else False                                                # Se a lista for None, define como False do contrário True
        cnpj = cnpj if cnpj is not None else False                                                   # Se o cnpj for None, define como False do contrário True
        inicio = inicio if inicio is not None else 0                                                 # Se o inicio for None, define como 0 do contrário 0
        fim = fim if fim is not None else 0                                                          # Se o fim for None, define como 0 do contrário 0
        arquivo_leitura = arquivo_leitura if arquivo_leitura is not None else "CNPJs.xlsx"           # Se o arquivo de leitura for None, define como "CNPJs.xlsx" do contrário "CNPJs.xlsx"
        arquivo_saida = arquivo_saida if arquivo_saida is not None else "Debitos.xlsx"               # Se o arquivo de saída for None, define como "Debitos.xlsx" do contrário "Debitos.xlsx"
        tempo_espera = tempo_espera if tempo_espera is not None else 5

        console = Console("Simples Nacional")
        dados_coletados = []
        dados = []
        cnpj_invalidos = []
        total_elementos = 0
        logado = False

        # Abre navegador e acessa página de consulta
        navegador = Navegador("chrome")
        navegador.abrir_navegador()
        navegador.acessar_pagina("https://www10.receita.fazenda.gov.br/login/publico/bemvindo/")
        navegador.aguardar(tempo_espera)
        navegador.clicar(By.ID, "linkFormSubmit")
        try:
            # Acessa página de consulta
            navegador.acessar_pagina("https://www10.receita.fazenda.gov.br/entessn/aplicacoes.aspx?id=51")
            navegador.aguardar(tempo_espera)
            navegador.mudar_frame("frame")
            navegador.aguardar(tempo_espera)            

            # Verifica se a consulta é individual ou em lista
            match lista:
                case False:
                    # Preenche os campos de consulta
                    navegador.aguardar_elemento(By.ID, "ctl00_ContentPlaceHolderPrincipal_tbCnpj", timeout=15)                   
                    navegador.preencher(By.ID, "ctl00_ContentPlaceHolderPrincipal_tbCnpj", cnpj)
                    navegador.preencher(By.ID, "ctl00_ContentPlaceHolderPrincipal_tbDataInicial", data_inicio)
                    navegador.preencher(By.ID, "ctl00_ContentPlaceHolderPrincipal_tbDataFinal", data_final)
                    navegador.clicar(By.ID, "ctl00_ContentPlaceHolderPrincipal_btnFiltrar")
                    navegador.aguardar(tempo_espera)
                    logado = True

                    # Coleta dados da tabela
                    navegador.voltar_frame()
                    navegador.mudar_frame("frame")
                    try:
                        navegador.aguardar_elemento(By.CLASS_NAME, "GridViewStyle", timeout=15)
                        tabela = navegador.encontrar_elemento(By.CLASS_NAME, "GridViewStyle")
                        linhas = tabela.find_elements(By.TAG_NAME, "tr")

                        # Verifica se a tabela está vazia
                        if not linhas:
                            console.exibir_mensagem("Tabela vazia! Nenhum dado encontrado.", 1)
                            logging.warning(f"Tabela vazia para o CNPJ {cnpj}. Nenhum dado encontrado.")
                            navegador.fechar_navegador()
                            return
                        else:
                            console.exibir_mensagem("Tabela encontrada!", 1)
                            logging.info(f"Tabela encontrada para o CNPJ {cnpj}.")
                            
                            # Coleta os dados da tabela
                            for linha in linhas:
                                total_elementos +=1                                                                
                                colunas = linha.find_elements(By.TAG_NAME, "td")                                
                                linha_dados = [cnpj] + [coluna.text.strip() for coluna in colunas]
                                dados.append(linha_dados)
                                console.exibir_mensagem(f"Dados coletados: {linha_dados}", 0)

                            console.exibir_mensagem(f"Total: {total_elementos}", 1)
                            logging.info(f"Total de registros coletados: {total_elementos}")

                        # Adiciona os dados coletados na lista    
                        dados_coletados.extend(dados)
                        console.exibir_mensagem(f"Dados coletados com sucesso para o CNPJ {cnpj}!", 1)
                        console.exibir_mensagem(f"Dados coletados: {dados_coletados}", 0)

                    except Exception as e:
                        print(f"Erro ao coletar dados {cnpj}: {e}")
                        logging.exception(f"Erro ao coletar dados para o CNPJ {cnpj}: {e}")
                        if len(total_elementos) != 0:
                            dados_coletados.extend(dados)
                            console.exibir_mensagem(f"Dados coletados com sucesso para o CNPJ {cnpj}!", 1)
                            logging.info(f"Dados coletados com sucesso para o CNPJ {cnpj}!")
                            console.exibir_mensagem(f"Dados coletados: {dados_coletados}", 0)
                            logging.info(f"Dados coletados: {dados_coletados}")
                            self.Processar_Dados(dados_coletados, arquivo_saida)
                        
                case True:
                    planilha = openpyxl.load_workbook(arquivo_leitura)          # Abre o arquivo de leitura
                    folha1 = planilha.active                                    # Seleciona a primeira planilha do arquivo
                    logado = True

                    # Inicia a leitura da lista de CNPJs
                    console.limpar_tela()
                    console.exibir_mensagem("Consulta de débitos para uma lista de CNPJs.", 1)
                    for i in range(inicio, fim):
                        cnpj = folha1.cell(row=i, column=1).value                        
                        console.exibir_mensagem(f"Processando CNPJ: {cnpj}", 0)
                        logging.info(f"Processando CNPJ: {cnpj}")
                        if cnpj:
                            validar_cnpj = SimplesNacional.Valida_CNPJ(cnpj)  # Valida o CNPJ
                            if not validar_cnpj:
                                cnpj_invalidos.append(cnpj)
                                console.exibir_mensagem(f"CNPJ adicionado a lista de inválidos!", 1)
                                logging.info(f"CNPJ adicionado a lista de inválidos: {cnpj}")
                        console.exibir_mensagem(f"CNPJ válido!", 1)
                        logging.info(f"CNPJ válido: {cnpj}")
                        cnpj = re.sub(r'[^0-9]', '', cnpj)  # Remove caracteres não numéricos
                        console.exibir_mensagem(f"CNPJ formatado: {cnpj}", 0)
                        logging.info(f"CNPJ formatado: {cnpj}")

                        # Preenche os campos de consulta
                        navegador.aguardar_elemento(By.ID, "ctl00_ContentPlaceHolderPrincipal_tbCnpj", timeout=15)                   
                        navegador.preencher(By.ID, "ctl00_ContentPlaceHolderPrincipal_tbCnpj", cnpj)
                        navegador.preencher(By.ID, "ctl00_ContentPlaceHolderPrincipal_tbDataInicial", data_inicio)
                        navegador.preencher(By.ID, "ctl00_ContentPlaceHolderPrincipal_tbDataFinal", data_final)
                        navegador.clicar(By.ID, "ctl00_ContentPlaceHolderPrincipal_btnFiltrar")
                        navegador.aguardar(tempo_espera)

                        # Coleta dados da tabela
                        navegador.voltar_frame()
                        navegador.mudar_frame("frame")
                        try:
                            navegador.aguardar_elemento(By.CLASS_NAME, "GridViewStyle", timeout=15)
                            tabela = navegador.encontrar_elemento(By.CLASS_NAME, "GridViewStyle")
                            linhas = tabela.find_elements(By.TAG_NAME, "tr")

                            # Verifica se a tabela está vazia
                            if not linhas:
                                console.exibir_mensagem("Tabela vazia! Nenhum dado encontrado.", 1)
                                logging.warning(f"Tabela vazia para o CNPJ {cnpj}. Nenhum dado encontrado.")
                                navegador.fechar_navegador()
                                return
                            else:
                                console.exibir_mensagem("Tabela encontrada!", 1)
                                logging.info(f"Tabela encontrada para o CNPJ {cnpj}.")
                                # Coleta os dados da tabela
                                for linha in linhas:
                                    total_elementos +=1                                                                
                                    colunas = linha.find_elements(By.TAG_NAME, "td")                                
                                    linha_dados = [cnpj] + [coluna.text.strip() for coluna in colunas]
                                    dados.append(linha_dados)
                                    console.exibir_mensagem(f"Dados coletados: {linha_dados}", 0)
                                    logging.info(f"Dados coletados: {linha_dados}")

                                console.exibir_mensagem(f"Total: {total_elementos}", 1)
                                logging.info(f"Total de elementos coletados para o CNPJ {cnpj}: {total_elementos}")

                                # Adiciona os dados coletados na lista
                                dados_coletados.extend(dados)
                                console.exibir_mensagem(f"Dados coletados com sucesso para o CNPJ {cnpj}!", 1)
                                logging.info(f"Dados coletados com sucesso para o CNPJ {cnpj}!")
                                console.exibir_mensagem(f"Dados coletados: {dados_coletados}", 0)
                                logging.info(f"Dados coletados: {dados_coletados}")
                                dados = []

                                # Acessa página de consulta
                                navegador.acessar_pagina("https://www10.receita.fazenda.gov.br/entessn/aplicacoes.aspx?id=51")
                                navegador.aguardar(tempo_espera)
                                navegador.mudar_frame("frame")
                                navegador.aguardar(tempo_espera)
                                
                        except Exception as e:
                            print(f"Erro ao coletar dados {cnpj}: {e}")
                            logging.exception(f"Erro ao coletar dados para o CNPJ {cnpj}: {e}")

                case _:
                    pass

            if logado:
                self.Processar_Dados(dados_coletados, arquivo_saida)
                console.exibir_mensagem("Consulta finalizada com sucesso!", 1)
                logging.info("Consulta finalizada com sucesso!")
                navegador.fechar_navegador()
                
                # Libera os recursos
                dados_coletados = []
                dados = []
                cnpj_invalidos = []
                total_elementos = 0
                logado = False
                logging.info("Recursos Liberados(dados_coletados, dados, cnpj_invalidos, total_elementos, logado).")
                return

        except Exception as e:
            console.exibir_mensagem_piscando(f"Erro ao logar-se: {e}", 0)
            console.exibir_mensagem("Verifique se o token com certificado digital\nfoi inserido na porta USB e tente novamente.", 0)
            console.exibir_mensagem("Encerrando navegador, aguarde....", 1)
            logging.exception(f"Erro ao logar-se: {e}")
            navegador.fechar_navegador()
            logado = False
            #logging.info(f"Planilha salva com sucesso em {os.path.abspath(arquivo_saida)}")
            return 
        
###############################[   Funções   ]###################################|

###############################[   Testes    ]###################################|
"""
# Testa a classe SimplesNacional
    if __name__ == "__main__":

    console = Console("Simples Nacional")
    console.exibir_titulo()
    console.exibir_mensagem("Teste de Validação de CNPJ")
    
    cnpj_valido = SimplesNacional.Valida_CNPJ("12.345.678/0001-95")
    console.exibir_mensagem(f"CNPJ Válido: {cnpj_valido}")
    
    cnpj_valido = SimplesNacional.Valida_CNPJ("04.252.011/0001-11")
    console.exibir_mensagem(f"CNPJ Inválido: {cnpj_valido}", 1)

    # Cria uma instância da classe SimplesNacional
    simples_nacional = SimplesNacional()

    # Testa a consulta de débitos individual
    console.exibir_mensagem("Teste de Consulta de Débitos")
    simples_nacional.ConsultaDebitos("01/2022", lista=False, 
                                     cnpj="42107457000140", 
                                     inicio=0, fim=0, 
                                     arquivo_saida="C:/Users/welton.rosa/Documents/Debitos.xlsx")
  """ 
cs = Console("Divergência WebISS")
sn = SimplesNacional()
cs.exibir_mensagem("Consulta de lista de Débitos")
sn.ConsultaDebitos("01/2020", "12/2025", lista=True,
                                    cnpj="42107457000140",
                                    inicio=1, fim=133,
                                    arquivo_leitura="C:/Users/welton.rosa/Documents/WebISS/lista_erros.xlsx",
                                    arquivo_saida="C:/Users/welton.rosa/Documents/WebISS/Debitos-2025-erros3.xlsx", tempo_espera=9)
