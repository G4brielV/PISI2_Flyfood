from typing import List, Tuple
from math import sqrt


def distancia_euclidiana(cidadeUm: Tuple[int, int], cidadeDois: Tuple[int, int]) -> float:
    return sqrt((((cidadeUm[0] - cidadeDois[0]) ** 2) + ((cidadeUm[1] - cidadeDois[1]) ** 2)))


def vizinho_mais_proximo(pontos: List[tuple[int, int]]) -> str:
    n_cidades = len(pontos)
    menor_distancia_total = float('inf')
    melhor_cidade_inicial = 0

    for cidade_inicio in range(n_cidades):
        caminho_guloso = [cidade_inicio]
        visitas = [False] * n_cidades
        visitas[cidade_inicio] = True
        distancia_total_atual = 0

        for _ in range(n_cidades - 1):
            ultimo = caminho_guloso[-1]
            prox_cidade = None
            menor_distancia = float('inf')

            for i in range(n_cidades):
                if not visitas[i]:
                    distancia = distancia_euclidiana(pontos[ultimo], pontos[i])
                    if distancia < menor_distancia:
                        menor_distancia = distancia
                        prox_cidade = i

            if prox_cidade is not None:
                caminho_guloso.append(prox_cidade)
                visitas[prox_cidade] = True
                distancia_total_atual += menor_distancia

        distancia_total_atual += distancia_euclidiana(pontos[caminho_guloso[-1]], pontos[cidade_inicio])
        caminho_guloso.append(cidade_inicio)

        if distancia_total_atual < menor_distancia_total:
            menor_distancia_total = distancia_total_atual
            melhor_cidade_inicial = cidade_inicio
            melhor_caminho = [i + 1 for i in caminho_guloso]

    string_retorno = f'A melhor cidade inicial é: {melhor_cidade_inicial + 1}. Distância total: {menor_distancia_total :.4f} \nCaminho: {melhor_caminho}'

    return string_retorno


def principal():
    """função principal"""
    # Lendo entrada
    pontos = []
    while True:
        linha = input().strip()
        if linha == "EOF":  # Condição de parada
            break
        dados = linha.split()
        _, x, y = dados
        pontos.append((float(x), float(y)))

    print(vizinho_mais_proximo(pontos))


if __name__ == '__main__':
    principal()