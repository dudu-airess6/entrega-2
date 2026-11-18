import os
import hmac
import hashlib
from cryptography.hazmat.primitives.kdf.scrypt import Scrypt
from cryptography.exceptions import InvalidKey

class AuthService:
    """
    Serviço de Autenticação Segura (Entrega 2)
    Utiliza KDF lenta (scrypt / Argon2 / PBKDF2) com Salt aleatório por usuário 
    e verificação em tempo constante (proteção contra timing attacks).
    """

    def __init__(self):
        # Base de dados simulada em memória: { username: { "salt": bytes, "password_hash": bytes } }
        self._db = {}

    @staticmethod
    def _gerar_salt(tamanho: int = 16) -> bytes:
        """Gera um salt criptograficamente seguro utilizando CSPRNG."""
        return os.urandom(tamanho)

    @classmethod
    def derivar_hash_senha(cls, senha: str, salt: bytes) -> bytes:
        """
        Deriva o hash da senha utilizando scrypt (OWASP ASVS 5.0 - Requisito 11.4.2).
        Parâmetros de custo recomendados:
        - n=16384 (2^14): Custo de memória/CPU
        - r=8: Tamanho do bloco
        - p=1: Paralelização
        - length=32: Tamanho da chave derivada (256 bits)
        """
        kdf = Scrypt(
            salt=salt,
            length=32,
            n=16384,
            r=8,
            p=1
        )
        return kdf.derive(senha.encode('utf-8'))

    def cadastrar_usuario(self, username: str, senha: str) -> bool:
        """
        Cadastra um novo usuário armazenando o salt e o hash derivado (NUNCA a senha em texto puro).
        """
        if not username or not senha:
            raise ValueError("Nome de usuário e senha não podem ser vazios.")
        
        if username in self._db:
            raise ValueError(f"Usuário '{username}' já existe no sistema.")

        # Gerar salt exclusivo para este usuário
        salt = self._gerar_salt()
        # Derivar o hash da senha usando a KDF lenta
        password_hash = self.derivar_hash_senha(senha, salt)

        # Armazenar salt e hash
        self._db[username] = {
            "salt": salt,
            "password_hash": password_hash
        }
        return True

    def autenticar_usuario(self, username: str, senha: str) -> bool:
        """
        Autentica o usuário recalculando o hash com o mesmo salt e realizando 
        comparação em tempo constante para evitar ataques de temporização (Timing Attacks).
        """
        if username not in self._db:
            # Para evitar enumeração de usuários por timing, executamos uma comparação dummy
            self.derivar_hash_senha("dummy_password", b"dummy_salt_12345")
            return False

        registro = self._db[username]
        salt = registro["salt"]
        hash_esperado = registro["password_hash"]

        # Recalcular hash da senha fornecida
        hash_calculado = self.derivar_hash_senha(senha, salt)

        # Comparação em tempo constante via hmac.compare_digest
        return hmac.compare_digest(hash_calculado, hash_esperado)

    def obter_registro_protegido(self, username: str) -> dict:
        """Retorna o registro público/protegido do banco para fins de auditoria/evidência."""
        if username not in self._db:
            return None
        registro = self._db[username]
        return {
            "username": username,
            "salt_hex": registro["salt"].hex(),
            "hash_hex": registro["password_hash"].hex()
        }
