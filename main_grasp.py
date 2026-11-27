import sys
import csv
import math
import random
import time
from pathlib import Path

from avaliacao import ler_instancia
from grasp import (
    busca_local,
    calcular_cobertura,
    construir_solucao,
    criar_candidatos,
)


def executar_grasp(caminho_instancia, iteracoes=100, passo=10,
                   semente=141592, parada_antecipada=False):
    if iteracoes <= 0 or not math.isfinite(passo) or passo <= 0:
        raise ValueError('Verifique o número de iterações e o passo.')

    largura, altura, quantidade_antenas, _, hosts, raio = ler_instancia(
        caminho_instancia
    )
    if quantidade_antenas < 0 or not math.isfinite(raio) or raio < 0:
        raise ValueError('Quantidade de antenas ou raio inválido.')

    inicio = time.perf_counter()
    gerador_aleatorio = random.Random(semente)
    raio_quadrado = raio * raio

    candidatos = criar_candidatos(hosts, largura, altura)
    cobertura_candidatos = {
        posicao: calcular_cobertura(posicao, hosts, raio_quadrado)
        for posicao in candidatos
    }

    melhor_solucao = []
    melhor_cobertura = -1

    for _ in range(iteracoes):
        solucao = construir_solucao(
            cobertura_candidatos, quantidade_antenas, gerador_aleatorio
        )
        solucao, cobertura = busca_local(
            solucao, hosts, raio_quadrado, largura, altura, passo
        )

        if cobertura > melhor_cobertura:
            melhor_solucao = solucao
            melhor_cobertura = cobertura

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
    if len(sys.argv) != 2:
        sys.exit('Uso: python main_grasp.py caminho_da_instancia')

    instancia = sys.argv[1]
    iteracoes = 100
    passo = 10
    semente = 141592
    parada_antecipada = False

    solucao, hosts_cobertos, duracao = executar_grasp(
        instancia,
        iteracoes=iteracoes,
        passo=passo,
        semente=semente,
        parada_antecipada=parada_antecipada,
    )

    print(f'{semente};{instancia};{hosts_cobertos};{duracao}')


if __name__ == '__main__':
    main()