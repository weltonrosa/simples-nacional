################################[ Cabeçalho ]##################################
'''
Classe Console para exibir mensagens e opções no console. 
Esta classe é útil para criar interfaces de linha de comando mais amigáveis e organizadas.

Autor: Welton C. O. Rosa
Data: 02/04/2025

Ultima Atualização: 19/08/2025
Atualizado por: Welton C. O. Rosa

Versão: 1.0
Python Version: 3.9.7
Bibliotecas: os
Funções disponíveis: Console, SimplesNacional
'''
###############################[ Bibliotecas ]##################################|
# -*- coding: utf-8 -*-
from console import Console
from simples_nacional import SimplesNacional

def main():
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

if __name__ == "__main__":
    main()