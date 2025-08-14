# -*- coding: utf-8 -*-
<<<<<<< HEAD
""" from console import Console
=======
from console import Console
>>>>>>> e77c940cafd5b1663f8aa221179b99075ca41f83
from simples_nacional import SimplesNacional

ce = Console("Divergencia_WebIss")
ce.exibir_titulo()
ce.exibir_mensagem("Teste de Validação de CNPJ")
sn = SimplesNacional

if __name__ == "__main__":
    ce.exibir_mensagem("Teste de Consulta de lista de Débitos")
    sn.ConsultaDebitos("12/2025", "01/2020", lista=True, 
                       cnpj="", 
                       inicio=2, fim=100, 
<<<<<<< HEAD
                       arquivo_leitura="D:\\Meu Drive\\pmu\\2025\\WebISS\\lista_consulta.xlsx", 
                       arquivo_saida="D:\\Meu Drive\\pmu\\2025\\WebISS\\Debitos-2025.xlsx") """
=======
                       arquivo_leitura="D:/Meu Drive/pmu/2025/WebISS/lista_consulta.xlsx", 
                       arquivo_saida="D:/Meu Drive/pmu/2025/WebISS/Debitos-2025.xlsx")
>>>>>>> e77c940cafd5b1663f8aa221179b99075ca41f83
