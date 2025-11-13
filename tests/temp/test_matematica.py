from app.matematica import Matematica


def test_soma():
    assert Matematica.soma(1, 2) == 3
