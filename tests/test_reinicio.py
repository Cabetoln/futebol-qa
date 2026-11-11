"""Saida de bola, gol e reinicio (R1 a R6).

Os IDs (TC-xx) apontam para docs/casos-de-teste.md.
"""
import pytest

from futebol.regras import Lance, Reinicio, Time, decidir_reinicio

A, D = Time.ATAQUE, Time.DEFESA
EM_JOGO = (Reinicio.EM_JOGO, None)
GOL = (Reinicio.GOL, A)
TIRO_DE_META = (Reinicio.TIRO_DE_META, D)
ESCANTEIO = (Reinicio.ESCANTEIO, A)

CENTRO_DO_GOL = 3400


@pytest.mark.parametrize(
    "x, y, z, ultimo, esperado",
    [
        # R1: bola so sai quando cruza totalmente a linha
        pytest.param(10511, CENTRO_DO_GOL, 0, A, EM_JOGO, id="TC-01-borda-na-linha"),
        pytest.param(10512, CENTRO_DO_GOL, 0, A, GOL, id="TC-02-um-cm-alem"),
        pytest.param(10500, CENTRO_DO_GOL, 0, A, EM_JOGO, id="TC-03-centro-na-linha"),
        # R2: traves e travessao
        pytest.param(10512, 3034, 0, A, GOL, id="TC-04-trave-esquerda"),
        pytest.param(10512, 3033, 0, A, TIRO_DE_META, id="TC-05-fora-da-trave-esquerda"),
        pytest.param(10512, 3766, 0, A, GOL, id="TC-06-trave-direita"),
        pytest.param(10512, 3767, 0, A, TIRO_DE_META, id="TC-07-fora-da-trave-direita"),
        pytest.param(10512, CENTRO_DO_GOL, 244, A, GOL, id="TC-08-altura-do-travessao"),
        pytest.param(10512, CENTRO_DO_GOL, 245, D, ESCANTEIO, id="TC-09-acima-do-travessao"),
        # R3: gol contra
        pytest.param(10512, CENTRO_DO_GOL, 0, D, GOL, id="TC-10-gol-contra"),
        # R4: linha de fundo fora do gol
        pytest.param(10512, 1000, 0, A, TIRO_DE_META, id="TC-11-fundo-toque-ataque"),
        pytest.param(10512, 1000, 0, D, ESCANTEIO, id="TC-12-fundo-toque-defesa"),
        # R5: lateral
        pytest.param(5000, 6812, 0, A, (Reinicio.LATERAL, D), id="TC-13-lateral-lado-maior"),
        pytest.param(5000, 6811, 0, A, EM_JOGO, id="TC-14-borda-na-lateral"),
        pytest.param(5000, -12, 0, D, (Reinicio.LATERAL, A), id="TC-15-lateral-lado-zero"),
        pytest.param(5000, -11, 0, D, EM_JOGO, id="TC-16-borda-na-lateral-zero"),
        pytest.param(10512, 6812, 0, A, TIRO_DE_META, id="TC-17-canto-vale-linha-de-gol"),
        # Modelo
        pytest.param(0, CENTRO_DO_GOL, 0, A, EM_JOGO, id="TC-21-x-zero"),
    ],
)
def test_decidir_reinicio(x, y, z, ultimo, esperado):
    assert decidir_reinicio(x, y, z, ultimo) == esperado


# --- R6: gol direto de lateral nao vale (mas de escanteio vale) -------------

@pytest.mark.parametrize(
    "lance, ultimo, esperado",
    [
        pytest.param(Lance.LATERAL, A, TIRO_DE_META, id="TC-18-lateral-no-gol-adversario"),
        pytest.param(Lance.LATERAL, D, ESCANTEIO, id="TC-19-lateral-no-proprio-gol"),
        pytest.param(Lance.ESCANTEIO, A, GOL, id="TC-20-escanteio-direto-vale"),
        pytest.param(Lance.TIRO_DE_META, A, GOL, id="tiro-de-meta-direto-vale"),
    ],
)
def test_gol_direto_de_bola_parada(lance, ultimo, esperado):
    assert decidir_reinicio(10512, CENTRO_DO_GOL, 0, ultimo, lance) == esperado


def test_tc21_x_negativo_e_erro():
    with pytest.raises(ValueError):
        decidir_reinicio(-1, CENTRO_DO_GOL, 0, A)


def test_adversario():
    assert A.adversario() is D
    assert D.adversario() is A
