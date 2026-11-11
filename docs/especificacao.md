# Especificação: regras de futebol

Versão 1.0 · Autor: Carlos Neto

Regras simplificadas a partir das Regras do Jogo da IFAB. O objetivo é ter regras
com fronteiras claras para testar, e não reproduzir o livro de regras inteiro.

## Modelo

Todas as medidas são **números inteiros em centímetros**. Inteiros evitam erros de
arredondamento, e um teste de valor limite como "1 cm além da linha" fica exato.

| Constante | Valor | Significado |
|---|---|---|
| `COMPRIMENTO` | 10500 | campo de 105 m, eixo `x` |
| `LARGURA` | 6800 | campo de 68 m, eixo `y` |
| `MEIO_CAMPO` | 5250 | linha do meio, em `x` |
| `RAIO_BOLA` | 11 | raio da bola |
| `TRAVE_ESQ` / `TRAVE_DIR` | 3034 / 3766 | traves, em `y` (gol de 7,32 m centralizado) |
| `TRAVESSAO` | 244 | altura do travessão, em `z` |

**Coordenadas**
- `x` vai de 0 a 10500. O time **ATAQUE** ataca a linha de gol em `x = 10500`, defendida pelo time **DEFESA**.
- `y` vai de 0 a 6800. As linhas laterais ficam em `y = 0` e `y = 6800`.
- `z` é a altura do **centro** da bola.

**Simplificações**
- Só o gol em `x = 10500` é modelado. Uma bola com `x < 0` está fora do escopo (erro).
- Traves e travessão são verificados pelo **centro** da bola.
- A posição de um jogador é a parte do corpo mais adiantada que pode marcar gol, em `x`.

## Regras

### R1: Bola fora de jogo
A bola só saiu quando cruzou **totalmente** a linha: a borda mais próxima da bola já
passou dela. Em `x`: `x - RAIO_BOLA > COMPRIMENTO`. Em `y`: `y - RAIO_BOLA > LARGURA`
ou `y + RAIO_BOLA < 0`. A bola sobre a linha (ainda que só tocando) está em jogo.

### R2: Gol
A bola cruzou totalmente a linha de gol **entre as traves** (`TRAVE_ESQ ≤ y ≤ TRAVE_DIR`)
e **abaixo do travessão** (`z ≤ TRAVESSAO`). O gol é sempre do ATAQUE.

### R3: Gol contra
Se o último toque foi da DEFESA e a bola entrou no gol, é gol do ATAQUE.

### R4: Linha de fundo, fora do gol
A bola cruzou a linha de gol fora das traves ou acima do travessão:
- último toque do ATAQUE → **tiro de meta** para a DEFESA;
- último toque da DEFESA → **escanteio** para o ATAQUE.

### R5: Lateral
A bola cruzou totalmente uma linha lateral → **lateral** para o time que **não** tocou
por último. Se a bola cruzou a linha de gol e a lateral ao mesmo tempo, vale a linha de gol.

### R6: Gol direto de lateral não vale
Se a bola entra no gol direto de um arremesso lateral, sem tocar em ninguém:
- arremesso do ATAQUE (gol adversário) → **tiro de meta** para a DEFESA;
- arremesso da DEFESA (próprio gol) → **escanteio** para o ATAQUE.

### R7: Posição de impedimento
Um atacante está em posição de impedimento quando, ao mesmo tempo:
1. está no campo de ataque, **sem contar a linha do meio** (`x > MEIO_CAMPO`);
2. está mais perto da linha de gol adversária do que a **bola** (`x > x_bola`);
3. está mais perto da linha de gol adversária do que o **penúltimo defensor** (`x > x_penúltimo`).

**Na mesma linha** da bola ou do penúltimo defensor **não** é impedimento. O goleiro conta
como defensor. São necessários pelo menos 2 defensores (senão, erro).

### R8: Infração de impedimento
O atacante em posição de impedimento comete infração ao receber a bola, **exceto** se a
receber direto de **lateral**, **tiro de meta** ou **escanteio**.

## Fora do escopo
Pênalti, faltas, cartões, vantagem e a participação ativa no lance (o modelo considera
que o atacante sempre participa quando recebe a bola).
