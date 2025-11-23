import allure
import pytest
from pathlib import Path


def pytest_collection_modifyitems(config, items):
    """Modifica os itens coletados para adicionar labels do Allure baseadas na estrutura de pastas."""
    for item in items:
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

                    # Adiciona markers do pytest que serão capturados pelo allure
                    item.add_marker(pytest.mark.allure_suite(f"{owner.title()} - {suite_name}"))
                    item.add_marker(pytest.mark.allure_label(owner=owner))

        except Exception:
            # Não quebrar a coleta se algo sair errado
            pass
