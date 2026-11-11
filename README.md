# Futebol QA

Regras de futebol (gol, lateral, tiro de meta, escanteio e impedimento) testadas com
valor limite, tabela de decisão e mutation testing.

| Métrica | Resultado |
|---|---|
| Testes | 39, todos passando |
| Cobertura de linhas e ramos | 100% (53 linhas, 14 ramos) |
| Mutation score (mutmut) | 100% (54 de 54 mutantes mortos) |

## Objetivo

Mostrar que cobertura alta não basta: os testes precisam **detectar defeitos**. Por isso o
projeto mede a qualidade da suíte com mutation testing, além da cobertura.

## As regras

Simplificadas a partir das Regras do Jogo da IFAB. Detalhes em
[docs/especificacao.md](docs/especificacao.md).

| ID | Regra |
|---|---|
| R1 | A bola só sai quando cruza **totalmente** a linha |
| R2 | Gol: cruza a linha de gol entre as traves e abaixo do travessão |
| R3 | Gol contra conta para o time que ataca |
| R4 | Linha de fundo fora do gol: tiro de meta ou escanteio, conforme o último toque |
| R5 | Lateral para o time que não tocou por último |
| R6 | Gol direto de lateral não vale |
| R7 | Posição de impedimento: à frente da bola e do penúltimo defensor, no campo de ataque |
| R8 | Não há impedimento em lateral, tiro de meta ou escanteio |

## Estrutura

```
futebol/regras.py         regras (funções puras)
tests/test_reinicio.py    gol, saída de bola e reinício (R1 a R6)
tests/test_impedimento.py impedimento (R7 e R8)
docs/especificacao.md     especificação
docs/casos-de-teste.md    33 casos de teste
```

## Como rodar

### Testes e cobertura (Windows, PowerShell)

Criar o ambiente, uma vez só:

```
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements-dev.txt
```

Rodar os testes:

```
.\.venv\Scripts\python.exe -m pytest -v
```

Rodar com cobertura de ramos:

```
.\.venv\Scripts\python.exe -m pytest --cov=futebol --cov-branch --cov-report=term-missing
```

### Mutation testing (Linux ou WSL)

O mutmut 3 não roda no Windows nativo. No Windows, use o WSL com Ubuntu.

Criar o ambiente no Linux, uma vez só (fora do OneDrive, para não sincronizar arquivos):

```
python3 -m venv ~/venvs/futebol-qa
~/venvs/futebol-qa/bin/pip install -r requirements-dev.txt mutmut==3.8.1
```

Rodar, de dentro da pasta do projeto:

```
~/venvs/futebol-qa/bin/mutmut run
~/venvs/futebol-qa/bin/mutmut results
```

`mutmut results` lista os mutantes que não morreram. `mutmut show <nome>` mostra o que
cada um alterou.

## Estratégia de teste

- **Valor limite:** cada fronteira da especificação tem um teste de cada lado. Exemplo:
  bola com a borda sobre a linha (`x = 10511`, em jogo) e 1 cm além (`x = 10512`, fora).
- **Tabela de decisão:** o reinício depende da linha cruzada, de a bola ter entrado no
  gol, de quem tocou por último e do tipo de lance.
- **Mutation testing:** o mutmut altera o código (troca `>` por `>=`, `ATAQUE` por
  `DEFESA`, constantes, mensagens) e confere se algum teste falha.
- **Rastreabilidade:** cada teste leva o ID do caso de teste (TC-xx) que verifica.

## Decisões

| Decisão | Por quê |
|---|---|
| Medidas em centímetros inteiros | Sem erro de arredondamento de `float`: "1 cm além" é exato |
| Enums para time, lance e reinício | Um erro de digitação vira erro de código, não um valor inválido silencioso |
| Config do pytest no `pyproject.toml` | O mutmut copia o projeto para `mutants/` e não copiava o `pytest.ini`; os testes rodavam contra o código **sem** mutação |
| Mensagem de erro exata nos testes (`match=r"^...$"`) | 6 mutantes sobreviviam alterando só o texto do erro; o `match` sem âncoras não os mataria |

## Limitações

- Modela um só gol (`x = 10500`) e verifica traves e travessão pelo centro da bola.
- Fora do escopo: pênalti, faltas, cartões, vantagem e participação ativa no lance.
