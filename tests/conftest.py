import allure
from pathlib import Path


def pytest_runtest_setup(item):
    """Define suite e label 'owner' automaticamente com base na pasta do teste.

    Exemplo: tests/fabio-songs/... -> owner = 'fabio', suite = 'Fabio - Fabio-songs'
    A ideia é que a pasta siga o padrão '<owner>-<suite>' opcionalmente.
    """
    try:
        p = Path(str(item.fspath))
        parts = p.parts
        if 'tests' in parts:
            idx = parts.index('tests')
            if len(parts) > idx + 1:
                owner_dir = parts[idx + 1]
                # owner é a parte antes do primeiro '-' se existir
                owner = owner_dir.split('-')[0]
                suite_name = owner_dir.replace('-', ' ').title()
                # Aplica no Allure
                try:
                    allure.dynamic.suite(f"{owner.title()} - {suite_name}")
                    allure.dynamic.label("owner", owner)
                except Exception:
                    # Se allure não estiver disponível no momento da coleta, ignore silenciosamente
                    pass
    except Exception:
        # Não quebrar o setup se algo sair errado
        pass
