import argparse
import math
import random
import time

from avaliacao import ler_instancia


def criar_candidatos(hosts, largura, altura):
    return list(dict.fromkeys(
        (float(x), float(y)) for x, y in hosts
        if 0 <= x <= largura and 0 <= y <= altura
    ))


def mascara_cobertura(posicao, hosts, raio_quadrado):
    x, y = posicao
    mascara = 0
    for i, (hx, hy) in enumerate(hosts):
        if (x - hx) ** 2 + (y - hy) ** 2 <= raio_quadrado + 1e-9:
            mascara |= 1 << i
    return mascara


def construir_solucao(candidatos, mascaras, quantidade_antenas, alpha, rng):
    solucao = []
    cobertura = 0
    disponiveis = list(range(len(candidatos)))

    for _ in range(min(quantidade_antenas, len(disponiveis))):
        ganhos = [(mascaras[i] & ~cobertura).bit_count() for i in disponiveis]
        maior, menor = max(ganhos), min(ganhos)
        limite = maior - alpha * (maior - menor)
        lrc = [i for i, ganho in zip(disponiveis, ganhos) if ganho >= limite]
        escolhido = rng.choice(lrc)
        solucao.append(candidatos[escolhido])
        cobertura |= mascaras[escolhido]
        disponiveis.remove(escolhido)

    return solucao


def busca_local(solucao, hosts, raio_quadrado, largura, altura, passo):
    mascaras = [mascara_cobertura(p, hosts, raio_quadrado) for p in solucao]
    cobertura = 0
    for m in mascaras:
        cobertura |= m
    fitness = cobertura.bit_count()
    movimentos = [(dx, dy) for dx in (-passo, 0, passo)
                  for dy in (-passo, 0, passo) if dx or dy]

    while True:
        melhor_movimento = None
        melhor_fitness = fitness
        for indice, (x, y) in enumerate(solucao):
            cobertura_outras = 0
            for j, m in enumerate(mascaras):
                if j != indice:
                    cobertura_outras |= m

            for dx, dy in movimentos:
                nova_posicao = (x + dx, y + dy)
                nx, ny = nova_posicao
                if not (0 <= nx <= largura and 0 <= ny <= altura):
                    continue
                nova_mascara = mascara_cobertura(nova_posicao, hosts, raio_quadrado)
                novo_fitness = (cobertura_outras | nova_mascara).bit_count()
                if novo_fitness > melhor_fitness:
                    melhor_fitness = novo_fitness
                    melhor_movimento = (indice, nova_posicao, nova_mascara)

        if melhor_movimento is None:
            return solucao, fitness

        indice, nova_posicao, nova_mascara = melhor_movimento
        solucao[indice] = nova_posicao
        mascaras[indice] = nova_mascara
        fitness = melhor_fitness


def executar_grasp(caminho_instancia, iteracoes=100, alpha=0.3,
                    passo=10.0, semente=141592):
    if iteracoes <= 0 or not 0 <= alpha <= 1 or passo <= 0:
        raise ValueError('Use iteracoes > 0, 0 <= alpha <= 1 e passo > 0.')

    largura, altura, quantidade_antenas, _, hosts, raio = ler_instancia(caminho_instancia)
    if quantidade_antenas < 0 or raio < 0:
        raise ValueError('Quantidade de antenas e raio devem ser nao negativos.')
    if quantidade_antenas and not hosts:
        raise ValueError('A instancia nao possui hosts para gerar candidatos.')

    rng = random.Random(semente)
    inicio = time.perf_counter()