import argparse
import csv
import math
import random
import time
from pathlib import Path

from avaliacao import ler_instancia


from grasp import (
    criar_candidatos, obter_mascara, construir_solucao, busca_local
)


def executar_grasp(caminho_instancia, iteracoes=100, fator_aleatoriedade=0.3,
                   passo=10, semente=141592, parada_antecipada=False):
    if iteracoes <= 0 or not 0 <= fator_aleatoriedade <= 1 or not math.isfinite(passo) or passo <= 0:
        raise ValueError('Parâmetros inválidos: verifique iterações, fator de aleatoriedade e passo.')
    largura, altura, quantidade_antenas, _, hosts, raio = ler_instancia(caminho_instancia)
    if quantidade_antenas < 0 or not math.isfinite(raio) or raio < 0:
        raise ValueError('Quantidade de antenas ou raio inválido.')

    inicio = time.perf_counter()
    gerador_aleatorio = random.Random(semente)
    candidatos = criar_candidatos(hosts, largura, altura)
    if quantidade_antenas > len(candidatos):
        raise ValueError('Posições candidatas distintas insuficientes para a instância.')
    raio_quadrado = raio * raio
    cache_cobertura = {}
    mascaras_cobertura = [obter_mascara(posicao, hosts, raio_quadrado, cache_cobertura)
                          for posicao in candidatos]
    melhor_solucao = []
    melhor_cobertura = -1

    for _ in range(iteracoes):
        solucao = construir_solucao(candidatos, mascaras_cobertura, quantidade_antenas,
                                    fator_aleatoriedade, gerador_aleatorio)
        solucao, hosts_cobertos = busca_local(solucao, hosts, raio_quadrado, largura, altura,
                                       passo, cache_cobertura)
        if hosts_cobertos > melhor_cobertura:
            melhor_solucao, melhor_cobertura = solucao.copy(), hosts_cobertos
        if parada_antecipada and melhor_cobertura == len(hosts):
            break

    duracao = time.perf_counter() - inicio
    return melhor_solucao, melhor_cobertura, duracao


def registrar_resultado(caminho_csv, resultado):
    caminho = Path(caminho_csv)
    caminho.parent.mkdir(parents=True, exist_ok=True)
    escrever_cabecalho = not caminho.exists() or caminho.stat().st_size == 0
    with caminho.open('a', newline='', encoding='utf-8') as arquivo:
        escritor = csv.DictWriter(arquivo, fieldnames=list(resultado))
        if escrever_cabecalho:
            escritor.writeheader()
        escritor.writerow(resultado)


def main():
    parser = argparse.ArgumentParser(description='GRASP para posicionamento de antenas 5G')
    parser.add_argument('instancia')
    parser.add_argument('--iteracoes', type=int, default=100)
    parser.add_argument('--fator-aleatoriedade', '--alpha', type=float, default=0.3)
    parser.add_argument('--passo', type=int, default=10)
    parser.add_argument('--semente', type=int, default=141592)
    parser.add_argument('--parada-antecipada', action='store_true')
    parser.add_argument('--saida', default='resultados_grasp.csv')
    argumentos = parser.parse_args()
    solucao, hosts_cobertos, duracao = executar_grasp(
        argumentos.instancia, argumentos.iteracoes, argumentos.fator_aleatoriedade,
        argumentos.passo, argumentos.semente, argumentos.parada_antecipada)
    registrar_resultado(argumentos.saida, {
        'instancia': argumentos.instancia,
        'semente': argumentos.semente,
        'iteracoes_maximas': argumentos.iteracoes,
        'fator_aleatoriedade': argumentos.fator_aleatoriedade,
        'passo': argumentos.passo,
        'parada_antecipada': argumentos.parada_antecipada,
        'hosts_cobertos': hosts_cobertos,
        'tempo_segundos': duracao,
        'coordenadas': solucao,
    })


if __name__ == '__main__':
    main()