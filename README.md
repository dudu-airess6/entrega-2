# Entrega 2 — Hash e Autenticação Segura

Este repositório contém a implementação da **Entrega 2** do Projeto Integrador de Segurança da Informação (Universidade Tiradentes — UNIT).

## Escopo do Projeto

O objetivo desta entrega é implementar um mecanismo seguro de **cadastramento e autenticação de usuários**, eliminando o armazenamento de senhas em texto puro ou o uso de hashes vulneráveis (como SHA-256 simples).

### Tecnologias e Algoritmos

* **Linguagem:** Python 3.12+
* **Módulo de Segurança:** `auth_service.py`
* **Algoritmo KDF:** `scrypt` (OWASP ASVS 5.0 — Requisito 11.4.2) / `cryptography`
* **Tamanho do Salt:** 16 bytes (128 bits) aleatórios gerados via CSPRNG (`os.urandom`)
* **Comparação Segura:** `hmac.compare_digest` para prevenção de *Timing Attacks*.
* **Suíte de Testes:** `unittest` / `pytest`

---

## Estrutura do Repositório

```
entrega2/
├── .gitignore          # Filtro de arquivos locais (.venv, __pycache__, .pytest_cache)
├── requirements.txt    # Dependências externas (cryptography, argon2-cffi)
├── auth_service.py     # Serviço central de cadastro, geração de salt/hash e login
├── main.py             # Script de demonstração funcional
├── test_auth.py        # Suíte de testes automatizados de segurança
└── README.md           # Documentação técnica do repositório

```

---

## Como Executar

### 1\. Criar e Ativar o Ambiente Virtual (`.venv`)

**No Windows (PowerShell):**

```
python -m venv .venv
.\.venv\Scripts\Activate.ps1

```

**No Linux/macOS:**

```
python3 -m venv .venv
source .venv/bin/activate

```

### 2\. Instalar Dependências

```
pip install -r requirements.txt

```

### 3\. Executar a Demonstração Funcional

```
python main.py

```

### 4\. Executar os Testes Automatizados

```
python -m unittest test_auth.py -v
# ou
pytest -v

```

---

## Alinhamento com Padrões e Normas

* **OWASP Top 10:2025:** Categoria **A07 (Falhas de Autenticação)** e **A04 (Falhas Criptográficas)**.
* **OWASP ASVS 5.0:** Requisitos **11.4.1 (L1)**, **11.4.2 (L2 - KDF lenta com Salt)**, **6.2.1 (L1)** e **6.2.12 (L2)**.
* **ISO/IEC 27002:2022:** Controles **5.17 (Informação de autenticação)** e **8.5 (Autenticação segura)**.