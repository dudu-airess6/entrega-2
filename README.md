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

### 1. Criar e Ativar o Ambiente Virtual (`.venv`)

**No Windows (PowerShell):**

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

**No Linux:**

```bash
python3 -m venv .venv
source .venv/bin/activate
```

**No macOS (recomendado — com `uv`):**

O `python3` que acompanha o macOS é apenas um atalho que aciona o `xcode-select`. Se as *Command Line Tools* não estiverem instaladas, o comando falha com:

```
xcode-select: note: No developer tools were found, requesting install.
```

Nesse caso, use o [`uv`](https://docs.astral.sh/uv/), que dispensa as ferramentas da Apple:

```bash
# Instalar o uv (se ainda não tiver)
curl -LsSf https://astral.sh/uv/install.sh | sh

# Criar e ativar o ambiente virtual
uv venv .venv
source .venv/bin/activate
```

**No macOS (alternativa — com `python3` do sistema):**

```bash
# Instalar as Command Line Tools (necessário uma única vez)
xcode-select --install

# Criar e ativar o ambiente virtual
python3 -m venv .venv
source .venv/bin/activate
```

> Se a instalação das *Command Line Tools* falhar com a mensagem
> *"Não foi possível instalar o software porque no momento esse item não está disponível no servidor de Atualização de Software"*,
> baixe o pacote manualmente em [developer.apple.com/download/all](https://developer.apple.com/download/all/)
> (procure por "Command Line Tools for Xcode") ou utilize o `uv` como descrito acima.

### 2. Instalar Dependências

**Com `pip` (ambiente virtual ativado):**

```bash
pip install -r requirements.txt
```

**Com `uv`:**

```bash
uv pip install -r requirements.txt
```

### 3. Executar a Demonstração Funcional

```bash
python main.py
# ou, com uv (sem precisar ativar o ambiente)
uv run python main.py
```

### 4. Executar os Testes Automatizados

```bash
python -m unittest test_auth.py -v
# ou
pytest -v
# ou, com uv
uv run python -m unittest test_auth.py -v
```

---

## Alinhamento com Padrões e Normas

* **OWASP Top 10:2025:** Categoria **A07 (Falhas de Autenticação)** e **A04 (Falhas Criptográficas)**.
* **OWASP ASVS 5.0:** Requisitos **11.4.1 (L1)**, **11.4.2 (L2 - KDF lenta com Salt)**, **6.2.1 (L1)** e **6.2.12 (L2)**.
* **ISO/IEC 27002:2022:** Controles **5.17 (Informação de autenticação)** e **8.5 (Autenticação segura)**.
