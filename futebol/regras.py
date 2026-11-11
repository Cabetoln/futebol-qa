"""Regras de futebol simplificadas.

A especificacao completa esta em docs/especificacao.md (regras R1 a R8).
Medidas em centimetros inteiros. O ATAQUE ataca a linha de gol em x = COMPRIMENTO.
"""
from enum import Enum
from typing import Optional

COMPRIMENTO = 10500
LARGURA = 6800
MEIO_CAMPO = 5250
RAIO_BOLA = 11
TRAVE_ESQ = 3034
TRAVE_DIR = 3766
TRAVESSAO = 244


class Time(Enum):
    ATAQUE = "ataque"
    DEFESA = "defesa"

    def adversario(self) -> "Time":
        return Time.DEFESA if self is Time.ATAQUE else Time.ATAQUE


class Lance(Enum):
    """Como a bola chegou ao lance."""
    BOLA_ROLANDO = "bola rolando"
    LATERAL = "lateral"
    TIRO_DE_META = "tiro de meta"
    ESCANTEIO = "escanteio"


class Reinicio(Enum):
    EM_JOGO = "em jogo"
    GOL = "gol"
    LATERAL = "lateral"
    TIRO_DE_META = "tiro de meta"
    ESCANTEIO = "escanteio"


# --- R1: bola fora de jogo --------------------------------------------------

def cruzou_linha_de_gol(x: int) -> bool:
    """A borda mais proxima da bola ja passou da linha de gol."""
    return x - RAIO_BOLA > COMPRIMENTO


def cruzou_linha_lateral(y: int) -> bool:
    """A bola passou totalmente por uma das linhas laterais."""
    return y - RAIO_BOLA > LARGURA or y + RAIO_BOLA < 0


# --- R2: gol ----------------------------------------------------------------

def entre_as_traves(y: int, z: int) -> bool:
    """Centro da bola entre as traves e abaixo do travessao."""
    return TRAVE_ESQ <= y <= TRAVE_DIR and z <= TRAVESSAO


# --- R2 a R6: decisao do reinicio --------------------------------------------

def decidir_reinicio(
    x: int,
    y: int,
    z: int,
    ultimo_toque: Time,
    lance: Lance = Lance.BOLA_ROLANDO,
) -> tuple[Reinicio, Optional[Time]]:
    """Devolve o reinicio e o time que o executa (ou marca o gol).

    Bola em jogo devolve (Reinicio.EM_JOGO, None).
    """
    if x < 0:
        raise ValueError("x negativo esta fora do modelo")

    if cruzou_linha_de_gol(x):
        # R2 e R3: gol (inclusive gol contra). R6: lateral direto no gol nao vale
        # e e tratado como bola que saiu pela linha de fundo.
        if entre_as_traves(y, z) and lance is not Lance.LATERAL:
            return Reinicio.GOL, Time.ATAQUE
        # R4: linha de fundo
        if ultimo_toque is Time.ATAQUE:
            return Reinicio.TIRO_DE_META, Time.DEFESA
        return Reinicio.ESCANTEIO, Time.ATAQUE

    # R5: lateral (a linha de gol tem prioridade, por isso vem depois)
    if cruzou_linha_lateral(y):
        return Reinicio.LATERAL, ultimo_toque.adversario()

    return Reinicio.EM_JOGO, None


# --- R7 e R8: impedimento ----------------------------------------------------

LANCES_SEM_IMPEDIMENTO = frozenset(
    {Lance.LATERAL, Lance.TIRO_DE_META, Lance.ESCANTEIO}
)


def em_posicao_de_impedimento(
    x_jogador: int, x_bola: int, xs_defensores: list[int]
) -> bool:
    """R7: no campo de ataque e a frente da bola e do penultimo defensor.

    Na mesma linha nao e impedimento. O goleiro conta como defensor.
    """
    if len(xs_defensores) < 2:
        raise ValueError("sao necessarios pelo menos 2 defensores")
    penultimo = sorted(xs_defensores, reverse=True)[1]
    return x_jogador > MEIO_CAMPO and x_jogador > x_bola and x_jogador > penultimo


def cometeu_impedimento(
    x_jogador: int,
    x_bola: int,
    xs_defensores: list[int],
    lance: Lance = Lance.BOLA_ROLANDO,
) -> bool:
    """R8: infracao ao receber a bola, exceto de lateral, tiro de meta ou escanteio."""
    if lance in LANCES_SEM_IMPEDIMENTO:
        return False
    return em_posicao_de_impedimento(x_jogador, x_bola, xs_defensores)
