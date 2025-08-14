import sys
import os
#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from console import Console
from simples_nacional import SimplesNacional

cs = Console("Divergência WebISS")
sn = SimplesNacional()
cs.exibir_mensagem("Consulta de lista de Débitos")
sn.ConsultaDebitos("01/2020", "12/2025", lista=True,
                                    cnpj="42107457000140",
                                    inicio=1, fim=133,
                                    arquivo_leitura="C:/Users/welton.rosa/Documents/WebISS/lista_erros.xlsx",
                                    arquivo_saida="C:/Users/welton.rosa/Documents/WebISS/Debitos-2025-erros3.xlsx", tempo_espera=9)
