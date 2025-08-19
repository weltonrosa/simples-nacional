import unittest
from simples_nacional import SimplesNacional

class TestSimplesNacional(unittest.TestCase):
    def setUp(self):
        """Configuração inicial para os testes."""
        self.sn = SimplesNacional()

    def test_valida_cnpj_valido(self):
        """Teste para validar um CNPJ válido."""
        cnpj = "12.345.678/0001-95"
        self.assertTrue(self.sn.Valida_CNPJ(cnpj))

    def test_valida_cnpj_invalido(self):
        """Teste para validar um CNPJ inválido."""
        cnpj = "00.000.000/0000-00"
        self.assertFalse(self.sn.Valida_CNPJ(cnpj))

    def test_consulta_debitos(self):
        """Teste para verificar a consulta de débitos."""
        # Exemplo de teste para a função ConsultaDebitos
        # Aqui você pode simular a entrada e verificar se a saída está correta.
        resultado = self.sn.ConsultaDebitos(
            data_inicio="01/2020",
            data_final="12/2025",
            lista=False,
            cnpj="42107457000140",
            arquivo_saida="test_output.xlsx"
        )
        self.assertIsNotNone(resultado)  # Verifica se o resultado não é None

if __name__ == "__main__":
    unittest.main()