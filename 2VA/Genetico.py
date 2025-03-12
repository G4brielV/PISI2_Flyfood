"""AG"""
from typing import List, Tuple, Callable, Dict
from random import randint, random, sample, shuffle
from math import sqrt

"""Calculo da distância entre 2 pontos"""
def distancia_euclidiana(cidadeUm: Tuple[float, float], cidadeDois: Tuple[float, float]) -> float:
    return sqrt((((cidadeUm[0] - cidadeDois[0]) ** 2) + ((cidadeUm[1] - cidadeDois[1]) ** 2)))


"""Calculo do custo do caminho"""
def aptidao_individuo(cromossomo: int, n_genes: int, pontos: Dict[int, Tuple[float, float]]) -> float:
    """cálculo da aptidão de um único indivíduo"""
    custo = 0
    # Calculo da ida A->B->C->D...
    for i in range(len(cromossomo) - 1):
        custo += distancia_euclidiana(pontos[cromossomo[i]], pontos[cromossomo[i + 1]])

    # Calculo da volta
    custo += distancia_euclidiana(pontos[cromossomo[n_genes - 1]], pontos[cromossomo[0]])

    return custo


"""Aptidão = Custo dos caminhos"""
def aptidao(pop: List[List[int]], n_genes: int, pontos: Dict[int, Tuple[float, float]]) -> List[float]:
    """aptidão de uma população"""
    lista_aptidao: List[float] = [None] * len(pop)
    for i, ind in enumerate(pop):
        lista_aptidao[i] = aptidao_individuo(ind, n_genes, pontos)
    return lista_aptidao


def cruzamento_pais(pai1: List[int], pai2: List[int], taxa_cruzamento: float) -> Tuple[List[int], List[int]]:
    """cruzamento de dois individuos"""
    if random() <= taxa_cruzamento:
        ponto_cruzamento = randint(len(pai1)//2,len(pai1))
        inicio_filho_1 = pai1[:ponto_cruzamento]
        inicio_filho_2 = pai2[ponto_cruzamento:]

        for c in range(len(pai1)):
            if pai2[c] not in inicio_filho_1:
                inicio_filho_1.append(pai2[c])

            if pai1[c] not in inicio_filho_2:
                inicio_filho_2.append(pai1[c])

        return inicio_filho_1, inicio_filho_2
    return pai1, pai2


def cruzamento(pais: List[List[int]], taxa_cruzamento: float) -> List[int]:
    """cruzamento de todos os pais"""
    lista_filhos: List[int] = [None] * len(pais)
    for i in range(0, len(pais) - 1, 2):
        filho1, filho2 = cruzamento_pais(pais[i], pais[i + 1], taxa_cruzamento)
        lista_filhos[i] = filho1
        lista_filhos[i + 1] = filho2

    # Se o número de pais for ímpar, o último pai será adicionado sem cruzamento
    if len(pais) % 2 == 1:
        lista_filhos[-1] = pais[-1]  # Mantém o último pai na próxima geração

    return lista_filhos


def mutacao_individuo(filho: List[int], taxa_mutacao: float, n_genes: int) -> List[int]:
    """mutação de um individuo"""
    for i in range(n_genes - 1):
        # pra cada gene
        if random() <= taxa_mutacao:
            gene_trocado = randint(0, n_genes - 1)
            filho[i], filho[gene_trocado] = filho[gene_trocado], filho[i]
    return filho


def mutacao(filhos: List[List[int]], taxa_mutacao: float, n_genes: int) -> List[List[int]]:
    """Mutação de todos os filhos"""
    for i, ind in enumerate(filhos):
        filhos[i] = mutacao_individuo(ind, taxa_mutacao, n_genes)
    return filhos


def roleta(apts: List[float]) -> int:
    """Seleção por roleta para problemas de minimização"""
    apt_inversa = [1 / apt for apt in apts]  # Inversão para favorecer custos menores
    soma_roleta: float = sum(apt_inversa)
    n_sorteado: float = random() * soma_roleta
    soma_atual: float = 0

    for i, apt in enumerate(apt_inversa):
        soma_atual += apt
        if soma_atual >= n_sorteado:
            return i


def torneio(apt: List[float]) -> int:
    """Seleção por torneio"""
    pai1 = randint(0, len(apt) - 1)
    pai2 = randint(0, len(apt) - 1)
    return pai1 if apt[pai1] < apt[pai2] else pai2


def selecao_pais(pop: List[List[int]], apt: List[float], sel_func: Callable) -> List[List[int]]:
    """Seleção dos pais"""
    lista_pais: List[int] = [None] * len(pop)
    for i in range(len(pop)):
        idx_selecionado = sel_func(apt)
        lista_pais[i] = pop[idx_selecionado]
    return lista_pais


def selecao_sobreviventes(
        pop: List[List[int]], apt_pop: List[float], filhos: List[List[int]], apt_filhos: List[float]) -> Tuple[
    List[List[int]], List[float]]:
    """Definição da próxima geração - Substituição geracional sem elitismo"""
    for c in range(len(pop)):
        if apt_filhos[c] < apt_pop[c]:
            pop[c] = filhos[c]
            apt_pop[c] = apt_filhos[c]
    return pop, apt_pop


def populacao_inicial(tamanho_pop: int, n_genes: int) -> List[List[int]]:
    """Crição de população inicial"""
    # Iniciando a população
    pop: List[List[int]] = [None] * tamanho_pop

    for i in range(tamanho_pop):
        individuo = sample(range(1, n_genes + 1), n_genes)
        pop[i] = individuo

    return pop


def evolucao(
        n_pop: int,
        n_genes: int,
        taxa_cruzamento: float,
        taxa_mutacao: float,
        n_geracoes: int,
        sel_func: Callable,
        pontos: Dict[int, Tuple[float, float]]
) -> Tuple[List[List[int]], list[float]]:
    """Algoritmo genético"""
    pop = populacao_inicial(n_pop, n_genes)
    apt: List[float] = aptidao(pop, n_genes, pontos)
    for geracao in range(n_geracoes):
        pais = selecao_pais(pop, apt, sel_func)
        filhos = cruzamento(pais, taxa_cruzamento)
        filhos = mutacao(filhos, taxa_mutacao, n_genes)
        apt_filhos = aptidao(filhos, n_genes, pontos)
        pop, apt = selecao_sobreviventes(pop, apt, filhos, apt_filhos)
    return pop, apt


def principal():
    """função principal"""
    # Lendo entrada
    pontos = {}
    n_genes = 0
    while True:
        linha = input().strip()
        if linha == "EOF":  # Condição de parada
            break
        n_genes += 1
        dados = linha.split()
        chave = int(dados[0])
        valor = (float(dados[1]), float(dados[2]))
        pontos[chave] = valor
    taxa_cruzamento = 1
    taxa_mutacao = 0.01
    n_pop = 50
    n_geracoes = 700
    sel_func = roleta
    pop, apt = evolucao(
        n_pop, n_genes, taxa_cruzamento, taxa_mutacao, n_geracoes, sel_func, pontos
    )
    melhor_aptidao = min(apt)
    print(
        f"\n\n>>>Melhor solução encontrada é {pop[apt.index(melhor_aptidao)]}"
        f"\nFunção objetivo de {melhor_aptidao}\n\n"
    )


if __name__ == "__main__":
    principal()
