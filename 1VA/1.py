from typing import List, Tuple, Dict, Any


def Flyfood():
    # Lendo as dimensões da matriz
    linhas, colunas = map(int, input().split())

    # Iniciado o mapa dos pontos
    pontos = {}

    # Lendo a matriz
    for i in range(linhas):
        linha = input().split()
        for j in range(colunas):
            if linha[j] != "0":  # Se não for um espaço vazio
                pontos[linha[j]] = (i, j)

    # Extraindo os pontos
    mapa_pontos = pontos.copy() # Obtem um dic com as coordenadas de todos os pontos
    pontos.pop("R") # Remove o ponto R (restaurante)
    pontos_entrega = list(pontos.keys()) # Obtem uma lista com todos os pontos de entrega que devem sofrer permutações

    return melhor_caminho(mapa_pontos, pontos_entrega)




def melhor_caminho(pontos: Dict[str, Tuple[int, int]], entrada: List[str], pos: int = 0, melhor_preco = float("inf"), caminho = "") -> str:

    # Caso base: quando a posição chega ao final da lista, temos uma permutação completa
    if pos == len(entrada) - 1:
        preco_caminho = calcular_caminho(pontos, entrada)

        if preco_caminho < melhor_preco:
            melhor_preco = preco_caminho
            caminho = " ".join(entrada)

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


def distancia_Manhattan(ponto1: Tuple[int, int], ponto2: Tuple[int, int]) -> int:
    distancia = 0
    if ponto1[0] >= ponto2[0]:
        distancia += ponto1[0] - ponto2[0]

    else:
        distancia += ponto2[0] - ponto1[0]

    if ponto1[1] >= ponto2[1]:
        distancia += ponto1[1] - ponto2[1]

    else:
        distancia += ponto2[1] - ponto1[1]

    return int(distancia)


def calcular_caminho(pontos: Dict[str, Tuple[int, int]], caminho:List[str]) -> int:
    percurso = 0
    for c in range(len(caminho)):
        if c == 0:
            percurso += distancia_Manhattan(pontos["R"], pontos[caminho[c]])  # Restaurante -> 1 ponto
            percurso += distancia_Manhattan(pontos[caminho[c]], pontos[caminho[c + 1]])  # 1 ponto ate o 2

        elif c == len(caminho) - 1:
            percurso += distancia_Manhattan(pontos["R"], pontos[caminho[-1]])  # Último ponto -> restaurante

        else:
            percurso += distancia_Manhattan(pontos[caminho[c]],
                                                  pontos[caminho[c + 1]])  # De um ponto ate o próximo


    return percurso




if __name__ == "__main__":
    print(Flyfood())