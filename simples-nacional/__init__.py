################################[ Cabeçalho ]##################################
'''
Classe Console para exibir mensagens e opções no console. 
Esta classe é útil para criar interfaces de linha de comando mais amigáveis e organizadas.

Autor: Welton C. O. Rosa
Data: 02/04/2025

Ultima Atualização: 18/08/2025
Atualizado por: Welton C. O. Rosa

Versão: 1.0
Python Version: 3.9.7
Bibliotecas: os
Funções disponíveis: limpar_tela, exibir_titulo, exibir_mensagem, exibir_erro, exibir_opcoes
'''
###############################[ Bibliotecas ]##################################|
# -*- coding: utf-8 -*-
import sys
import os
from console import Console
from simples_nacional import SimplesNacional

cs = Console("Divergência WebISS")
sn = SimplesNacional()
cs.exibir_mensagem("Consulta de lista de Débitos")
sn.ConsultaDebitos("01/2020", "12/2025", 
                    lista=True,
                    cnpj="42107457000140",
                    inicio=1, fim=133,
                    arquivo_leitura="C:/Users/welton.rosa/Documents/WebISS/lista_erros.xlsx",
                    arquivo_saida="C:/Users/welton.rosa/Documents/WebISS/Debitos-2025-erros3.xlsx", 
                    tempo_espera=9)
