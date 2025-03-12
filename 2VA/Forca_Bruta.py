from math import sqrt
from typing import List, Tuple, Dict, Any


def melhor_caminho(pontos: Dict[str, Tuple[int, int]], entrada: List[str], pos: int = 0, melhor_preco = float("inf"), caminho = "") -> str:

    # Caso base: quando a posição chega ao final da lista, temos uma permutação completa
    if pos == len(entrada) - 1:
        preco_caminho = calcular_caminho(pontos, entrada)
        if preco_caminho < melhor_preco:
            melhor_preco = preco_caminho
            caminho = " ".join(map(str, entrada))
        if pos == 0:
            return caminho

        return melhor_preco, caminho


    for i in range(pos, len(entrada)):
        # Troca o elemento atual com o elemento da posição `pos`
        entrada[pos], entrada[i] = entrada[i], entrada[pos]

        # Faz a chamada recursiva para a próxima posição
        melhor_preco, caminho = melhor_caminho(pontos, entrada, pos + 1, melhor_preco, caminho)

        # Reverte a troca para restaurar o estado original da lista
        entrada[pos], entrada[i] = entrada[i], entrada[pos]

    if pos == 0:
        return caminho

    return melhor_preco, caminho


def distancia_euclidiana(cidadeUm: Tuple[float, float], cidadeDois: Tuple[float, float]) -> float:
    return sqrt((((cidadeUm[0] - cidadeDois[0]) ** 2) + ((cidadeUm[1] - cidadeDois[1]) ** 2)))


def calcular_caminho(pontos: Dict[str, Tuple[int, int]], caminho:List[str]) -> int:
    percurso = 0
    for c in range(len(caminho)-1):
        percurso += distancia_euclidiana(pontos[caminho[c]], pontos[caminho[c+1]])  # ponto 1 ate n

    # volta
    percurso += distancia_euclidiana(pontos[caminho[-1]], pontos[caminho[0]])


    return percurso

def principal():
    # Lendo entrada
    # Iniciado o mapa dos pontos
    mapa_pontos = {}
    n_cidades = 0
    while True:
        linha = input().strip()
        if linha == "EOF":  # Condição de parada
            break
        n_cidades += 1
        dados = linha.split()
        chave = int(dados[0])
        valor = (float(dados[1]), float(dados[2]))
        mapa_pontos[chave] = valor

    # Extraindo os pontos
    chave_pontos = list(mapa_pontos.keys()) # Obtem uma lista com todos os pontos de entrega que devem sofrer permutações

    print(melhor_caminho(mapa_pontos, chave_pontos))


if __name__ == "__main__":
    principal()