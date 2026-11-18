import unittest
import hashlib
import time
from auth_service import AuthService

class TestAuthService(unittest.TestCase):
    """
    Suíte de Testes Automatizados para a Entrega 2 (Hash e Autenticação Segura)
    Covers: OWASP Top 10 A07/A04, OWASP ASVS 5.0 (11.4.1, 11.4.2) e ISO/IEC 27002 (5.17, 8.5)
    """

    def setUp(self):
        self.auth = AuthService()

    def test_cadastro_autenticacao_sucesso(self):
        """Caso de Sucesso: Cadastra usuário e autentica com a senha correta."""
        self.auth.cadastrar_usuario("alice", "SenhaSegura!2026")
        resultado = self.auth.autenticar_usuario("alice", "SenhaSegura!2026")
        self.assertTrue(resultado, "A autenticação com a senha correta deve retornar True.")

    def test_falha_senha_incorreta(self):
        """Caso de Falha: Tentativa de login com senha incorreta deve ser rejeitada."""
        self.auth.cadastrar_usuario("bob", "SenhaValida123")
        resultado = self.auth.autenticar_usuario("bob", "SenhaInvalida456")
        self.assertFalse(resultado, "A autenticação com senha incorreta deve retornar False.")

    def test_falha_usuario_inexistente(self):
        """Caso de Falha: Tentativa de login com usuário não cadastrado deve falhar."""
        resultado = self.auth.autenticar_usuario("nao_existe", "SenhaQualquer")
        self.assertFalse(resultado, "Usuário inexistente deve falhar na autenticação.")

    def test_unicidade_salts_e_hashes(self):
        """
        Garantia de Segurança: Duas contas cadastradas com a MESMA SENHA 
        devem possuir SALTS e HASHES DIFERENTES no banco de dados,
        invalidando ataques por Tabelas Rainbow / Pré-computadas.
        """
        senha_comum = "SenhaIgual123!"
        self.auth.cadastrar_usuario("user1", senha_comum)
        self.auth.cadastrar_usuario("user2", senha_comum)

        reg1 = self.auth.obter_registro_protegido("user1")
        reg2 = self.auth.obter_registro_protegido("user2")

        self.assertNotEqual(
            reg1["salt_hex"], reg2["salt_hex"],
            "Salts devem ser únicos e gerados aleatoriamente para cada usuário."
        )
        self.assertNotEqual(
            reg1["hash_hex"], reg2["hash_hex"],
            "Hashes derivados de senhas iguais devem ser diferentes devido ao salt."
        )

    def test_inadequacao_sha256_puro(self):
        """
        Fundamentação Teórica: Demonstra por que SHA-256 isolado sem KDF/salt é inadequado.
        SHA-256 é um hash genérico e ultrarrápido (vulnerável a ataques de força bruta/GPU).
        """
        senha = "senha_simples_123"
        
        # SHA-256 simples produz sempre o mesmo hash determinístico
        sha256_hash1 = hashlib.sha256(senha.encode()).hexdigest()
        sha256_hash2 = hashlib.sha256(senha.encode()).hexdigest()

        self.assertEqual(
            sha256_hash1, sha256_hash2,
            "SHA-256 puro é determinístico e vulnerável a tabelas pré-computadas."
        )

if __name__ == "__main__":
    unittest.main(verbosity=2)
