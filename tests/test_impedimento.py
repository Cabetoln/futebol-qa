"""Posicao e infracao de impedimento (R7 e R8).

Os IDs (TC-xx) apontam para docs/casos-de-teste.md.
"""
import pytest

from futebol.regras import Lance, cometeu_impedimento, em_posicao_de_impedimento

# Goleiro em 10400, penultimo defensor em 8000.
DEFENSORES = [10400, 8000, 7000]
BOLA = 6000


@pytest.mark.parametrize(
    "x_jogador, x_bola, defensores, esperado",
    [
        pytest.param(8500, BOLA, DEFENSORES, True, id="TC-22-a-frente-de-todos"),
        pytest.param(8000, BOLA, DEFENSORES, False, id="TC-23-mesma-linha-penultimo"),
        pytest.param(8001, BOLA, DEFENSORES, True, id="TC-24-um-cm-a-frente"),
        pytest.param(9000, 9000, DEFENSORES, False, id="TC-25-mesma-linha-da-bola"),
        pytest.param(9001, 9000, DEFENSORES, True, id="TC-26-um-cm-a-frente-da-bola"),
        pytest.param(5250, 4000, [10400, 5000], False, id="TC-27-sobre-a-linha-do-meio"),
        pytest.param(5251, 4000, [10400, 5000], True, id="TC-27-um-cm-apos-o-meio"),
        pytest.param(8500, 9000, DEFENSORES, False, id="TC-28-atras-da-bola"),
        pytest.param(8500, BOLA, [6000, 8000, 9000], True, id="TC-29-goleiro-adiantado"),
    ],
)
def test_em_posicao_de_impedimento(x_jogador, x_bola, defensores, esperado):
    assert em_posicao_de_impedimento(x_jogador, x_bola, defensores) is esperado


def test_tc30_menos_de_dois_defensores_e_erro():
    with pytest.raises(ValueError, match=r"^sao necessarios pelo menos 2 defensores$"):
        em_posicao_de_impedimento(9500, BOLA, [9000])


def test_tc31_infracao_com_bola_rolando():
    assert cometeu_impedimento(8500, BOLA, DEFENSORES, Lance.BOLA_ROLANDO) is True


@pytest.mark.parametrize(
    "lance",
    [
        pytest.param(Lance.LATERAL, id="TC-32-lateral"),
        pytest.param(Lance.TIRO_DE_META, id="TC-32-tiro-de-meta"),
        pytest.param(Lance.ESCANTEIO, id="TC-32-escanteio"),
    ],
)
def test_tc32_sem_infracao_em_bola_parada(lance):
    assert cometeu_impedimento(8500, BOLA, DEFENSORES, lance) is False


def test_tc33_sem_infracao_fora_de_posicao():
    assert cometeu_impedimento(7500, BOLA, DEFENSORES, Lance.BOLA_ROLANDO) is False
