# TestPy — Configurando o Ambiente (Linux e Windows)

Este repositório contém alguns códigos Python e testes para atividade da facul. Aqui está um guia simples para configurar um ambiente virtual, instalar dependências e executar testes no Linux (bash) ou Windows (PowerShell/cmd).

Ponto chave: Não faça commit de ambientes virtuais. Use um arquivo `requirements.txt` para listar suas dependências.

## Execução Rápida

Para collections-fabio:

```bash
.venv/bin/pytest --collect-only -q tests/fabio-songs/test_get_songs.py
```

## Relatório Allure

### Localmente

Instale o Allure:

```bash
npm install -g allure-commandline --save-dev
```

Em seguida, execute o relatório:

``` bash
python -m pytest --alluredir allure-results
``` 
ou 
``` 
python -m pytest --alluredir=allure-results tests/ -v
``` 

```bash
allure serve allure-results
```

O relatório será aberto automaticamente no navegador (exceto em alguns ambientes Linux).

### GitHub Actions

O projeto inclui workflows automatizados do GitHub Actions:

- **`test.yml`**: Executa os testes com Allure em cada push/PR e faz upload dos resultados como artefatos
- **`ci.yml`**: Executa os testes e publica o relatório Allure na branch `main` (pasta `docs/`)

Para visualizar o relatório no GitHub:
1. Vá para a aba "Actions" do repositório
2. Clique no workflow executado
3. Baixe o artefato "allure-results" ou veja o relatório publicado em `docs/`

## Dicas

- Certifique-se de ter o Python 3.8+ instalado (use `python3` ou `python`).
- Crie um virtualenv na pasta do projeto, como `.venv`, ou tente o Poetry se preferir.

---

## Usando Poetry

Se o Poetry parecer bom para você gerenciar suas dependências, aqui está como começar.

- Instale o Poetry (pipx é uma boa maneira):

```bash
python3 -m pip install --user pipx
python3 -m pipx ensurepath
pipx install poetry
```

Ou use o instalador oficial:

```bash
curl -sSL https://install.python-poetry.org | python3 -
```

- Verifique se está instalado:

```bash
poetry --version
```

- Trabalhando com o projeto:

```bash
# Instalar dependências do pyproject.toml
poetry install || poetry install --no-root # caso seu linux reclame rode --no-root, o meu reclamou ;(

# Adicionar uma dependência e atualizar pyproject.toml
poetry add requests@2.32.5

# Bloquear dependências (atualiza poetry.lock)
poetry lock

# Entrar no shell do Poetry
poetry shell

# Executar um comando no ambiente
poetry run pytest -q
```

- Exportar para `requirements.txt` para CI:

```bash
poetry export -f requirements.txt --output requirements.txt --without-hashes
```

Notas:

- O Poetry gerencia virtualenvs para você — não há necessidade de criar `.venv` manualmente.
- O projeto já tem `pyproject.toml`, então apenas execute `poetry install` para corresponder à configuração atual.

---

## Linux / macOS (bash)

1. Crie o virtualenv:

```bash
python3 -m venv .venv
```

2. Ative-o:

```bash
source .venv/bin/activate
```

3. Atualize o pip e instale dependências (se você tiver `requirements.txt`):

```bash
python -m pip install --upgrade pip
# Se requirements.txt existir
pip install -r requirements.txt

# Caso contrário, apenas instale pytest para testes
pip install pytest
```

4. Execute testes:

```bash
pytest -q
```

5. Opcionalmente, gere `requirements.txt` após instalar suas bibliotecas:

```bash
pip freeze > requirements.txt
```

## Windows (PowerShell)

1. Crie o virtualenv:

```powershell
python -m venv .venv
```

2. Ative no PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
# Se a política de execução bloquear, execute como admin:
# Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

3. Atualize pip e instale deps:

```powershell
python -m pip install --upgrade pip
pip install -r requirements.txt
pip install pytest
```

4. Execute testes:

```powershell
pytest -q
```

---

## Windows (cmd)

1. Crie o virtualenv:

```cmd
python -m venv .venv
```

2. Ative no cmd:

```cmd
.venv\Scripts\activate.bat
```

3. Instale deps e execute testes (mesmo que acima):

```cmd
python -m pip install --upgrade pip
pip install -r requirements.txt
pip install pytest
pytest -qll
```

---

## Notas e Melhores Práticas

- Não faça commit da pasta virtualenv — ela já está em `.gitignore`.
- Use `requirements.txt` ou `pyproject.toml`/`poetry` para dependências.
- Se precisar remover um ambiente existente antes de fazer commit:

```bash
# Exemplo: remover .venv
rm -rf .venv
```

