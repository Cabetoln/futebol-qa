# Casos de Teste: regras de futebol

Resultado esperado derivado de `docs/especificacao.md`.
Técnicas: **PE** partição de equivalência, **VL** valor limite, **TD** tabela de decisão.

## Saída de bola, gol e reinício (R1 a R6)

Função: `decidir_reinicio(x, y, z, ultimo_toque, lance)`.
Salvo indicação, `y = 3400` (centro do gol), `z = 0` e `lance = BOLA_ROLANDO`.

| ID | Regra | Entrada | Esperado | Técnica |
|---|---|---|---|---|
| TC-01 | R1 | `x = 10511` (borda da bola sobre a linha) | bola em jogo | VL |
| TC-02 | R1, R2 | `x = 10512` (1 cm além) | gol do ATAQUE | VL |
| TC-03 | R1 | `x = 10500` (centro sobre a linha) | bola em jogo | VL |
| TC-04 | R2 | `x = 10512`, `y = 3034` (trave esquerda) | gol do ATAQUE | VL |
| TC-05 | R2, R4 | `x = 10512`, `y = 3033`, último toque ATAQUE | tiro de meta da DEFESA | VL |
| TC-06 | R2 | `x = 10512`, `y = 3766` (trave direita) | gol do ATAQUE | VL |
| TC-07 | R2, R4 | `x = 10512`, `y = 3767`, último toque ATAQUE | tiro de meta da DEFESA | VL |
| TC-08 | R2 | `x = 10512`, `z = 244` (altura do travessão) | gol do ATAQUE | VL |
| TC-09 | R2, R4 | `x = 10512`, `z = 245`, último toque DEFESA | escanteio do ATAQUE | VL |
| TC-10 | R3 | `x = 10512`, último toque DEFESA | gol do ATAQUE (gol contra) | TD |
| TC-11 | R4 | `x = 10512`, `y = 1000`, último toque ATAQUE | tiro de meta da DEFESA | TD |
| TC-12 | R4 | `x = 10512`, `y = 1000`, último toque DEFESA | escanteio do ATAQUE | TD |
| TC-13 | R5 | `x = 5000`, `y = 6812`, último toque ATAQUE | lateral da DEFESA | VL, TD |
| TC-14 | R1, R5 | `x = 5000`, `y = 6811` | bola em jogo | VL |
| TC-15 | R5 | `x = 5000`, `y = -12`, último toque DEFESA | lateral do ATAQUE | VL, TD |
| TC-16 | R1, R5 | `x = 5000`, `y = -11` | bola em jogo | VL |
| TC-17 | R5 | `x = 10512`, `y = 6812` (canto), último toque ATAQUE | tiro de meta da DEFESA (vale a linha de gol) | TD |
| TC-18 | R6 | entra no gol, `lance = LATERAL`, arremesso do ATAQUE | tiro de meta da DEFESA | TD |
| TC-19 | R6 | entra no gol, `lance = LATERAL`, arremesso da DEFESA | escanteio do ATAQUE | TD |
| TC-20 | R2, R6 | entra no gol, `lance = ESCANTEIO`, último toque ATAQUE | gol do ATAQUE (a exceção é só do lateral) | TD |
| TC-21 | Modelo | `x = 0` / `x = -1` | bola em jogo / erro com a mensagem exata `x negativo esta fora do modelo` | VL |

## Posição de impedimento (R7)

Função: `em_posicao_de_impedimento(x_jogador, x_bola, xs_defensores)`.
Salvo indicação, `xs_defensores = [10400, 8000, 7000]` (penúltimo = 8000) e `x_bola = 6000`.

| ID | Entrada | Esperado | Técnica |
|---|---|---|---|
| TC-22 | `x_jogador = 8500` | impedido | PE |
| TC-23 | `x_jogador = 8000` (mesma linha do penúltimo) | não impedido | VL |
| TC-24 | `x_jogador = 8001` | impedido | VL |
| TC-25 | `x_bola = 9000`, `x_jogador = 9000` (mesma linha da bola) | não impedido | VL |
| TC-26 | `x_bola = 9000`, `x_jogador = 9001` | impedido | VL |
| TC-27 | defensores `[10400, 5000]`, `x_bola = 4000`, `x_jogador = 5250` / `5251` | não impedido / impedido (linha do meio) | VL |
| TC-28 | `x_bola = 9000`, `x_jogador = 8500` (atrás da bola) | não impedido | PE |
| TC-29 | defensores `[6000, 8000, 9000]` (goleiro adiantado), `x_jogador = 8500` | impedido (penúltimo = 8000) | PE |
| TC-30 | defensores `[9000]` | erro com a mensagem exata `sao necessarios pelo menos 2 defensores` | PE |

## Infração de impedimento (R8)

Função: `cometeu_impedimento(x_jogador, x_bola, xs_defensores, lance)`.

| ID | Entrada | Esperado | Técnica |
|---|---|---|---|
| TC-31 | em posição de impedimento, `lance = BOLA_ROLANDO` | infração | TD |
| TC-32 | em posição de impedimento, `lance` = LATERAL, TIRO_DE_META ou ESCANTEIO | sem infração | TD |
| TC-33 | fora de posição de impedimento, `lance = BOLA_ROLANDO` | sem infração | TD |
