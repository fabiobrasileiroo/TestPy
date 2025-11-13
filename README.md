# TestPy — Como criar o ambiente (Linux & Windows)

Este repositório contém código Python e testes. Abaixo estão instruções simples para criar um ambiente virtual, instalar dependências e executar os testes tanto em Linux (bash) quanto em Windows (PowerShell / cmd).

IMPORTANTE: não versionar (commit) ambientes virtuais. Use um arquivo `requirements.txt` para listar dependências.

## Recomendação
- Use `python3` / `python` (Python 3.8+) instalado no sistema.
- Crie um virtualenv no diretório do projeto, por exemplo `.venv`.

---

## Linux / macOS (bash)

1. Criar o virtualenv:

```bash
python3 -m venv .venv
```

2. Ativar o virtualenv:

```bash
source .venv/bin/activate
```

3. Atualizar pip e instalar dependências (se tiver `requirements.txt`):

```bash
python -m pip install --upgrade pip
# Se existir requirements.txt
pip install -r requirements.txt

# Caso não exista, instale o pytest para rodar os testes
pip install pytest
```

4. Rodar os testes:

```bash
pytest -q
```

5. Gerar um `requirements.txt` opcional (após instalar libs usadas no projeto):

```bash
pip freeze > requirements.txt
```

---

## Windows (PowerShell)

1. Criar o virtualenv:

```powershell
python -m venv .venv
```

2. Ativar (PowerShell):

```powershell
.\.venv\Scripts\Activate.ps1
# Se sua política de execução impedir, você pode executar (Administrador):
# Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

3. Atualizar pip e instalar dependências:

```powershell
python -m pip install --upgrade pip
pip install -r requirements.txt
pip install pytest
```

4. Rodar os testes:

```powershell
pytest -q
```

---

## Windows (cmd)

1. Criar o virtualenv:

```cmd
python -m venv .venv
```

2. Ativar (cmd):

```cmd
.venv\Scripts\activate.bat
```

3. Instalar deps e rodar testes (como acima):

```cmd
python -m pip install --upgrade pip
pip install -r requirements.txt
pip install pytest
pytest -q
```

---

## Notas e boas práticas
- Não commit o diretório do virtualenv — já está ignorado no `.gitignore`.
- Prefira gerenciar dependências com `requirements.txt` ou `pyproject.toml`/`poetry`.
- Se você tiver um ambiente criado dentro do repositório e quiser removê-lo antes de commitar, faça:

```bash
# Exemplo (remover .venv):
rm -rf .venv
```

Se precisar, posso adicionar um `requirements.txt` inicial ou um arquivo de configuração para CI (GitHub Actions) que rode os testes automaticamente.

---

Se quiser, eu crio também um `requirements.txt` mínimo com `pytest` e adiciono um workflow de testes no GitHub Actions.
