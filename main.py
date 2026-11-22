
import argparse
from pathlib import Path
import time
import random

from algoritmo_genetico import (
    crossover_media,
    crossover_um_ponto,
    crossover_uniforme,
    inicializar_populacao,
    mutacao,
    selecionar_roleta,
    selecionar_torneio,
)
from avaliacao import avaliar, ler_instancia


def executar(
    caminho_instancia,
    tamanho_populacao=50,
    geracoes=100,
    taxa_mutacao=0.1,
    metodo_selecao="torneio",
    metodo_crossover="uniforme",
    raio_cobertura=20,
    mostrar_visualizacao=True,
):
    if tamanho_populacao < 1:
        raise ValueError("O tamanho da população deve ser pelo menos 1.")
    if geracoes < 0:
        raise ValueError("O número de gerações não pode ser negativo.")

    largura, altura, quantidade_antenas, quantidade_hosts, hosts, raio_cobertura = ler_instancia(
        caminho_instancia
    )

    populacao = inicializar_populacao(
        tamanho_populacao,
        quantidade_antenas,
        largura,
        altura,
    )

    seletores = {
        "roleta": selecionar_roleta,
        "torneio": selecionar_torneio,
    }
    cruzamentos = {
        "um_ponto": crossover_um_ponto,
        "uniforme": crossover_uniforme,
        "media": crossover_media,
    }
    if metodo_selecao not in seletores:
        raise ValueError("Seleção deve ser 'roleta' ou 'torneio'.")
    if metodo_crossover not in cruzamentos:
        raise ValueError("Crossover deve ser 'um_ponto', 'uniforme' ou 'media'.")

    selecionar = seletores[metodo_selecao]
    cruzar = cruzamentos[metodo_crossover]

    inicio = time.perf_counter()

    for _ in range(geracoes):
        fitnesses = [avaliar(individuo, hosts, raio_cobertura) for individuo in populacao]
        indice_melhor = max(range(len(populacao)), key=fitnesses.__getitem__)
        nova_populacao = [populacao[indice_melhor].copy()]

        while len(nova_populacao) < tamanho_populacao:
            if metodo_selecao == "roleta":
                soma_fitness = sum(fitnesses)
                indice_pai1 = selecionar(populacao, fitnesses, soma_fitness)
                indice_pai2 = selecionar(populacao, fitnesses, soma_fitness)
            else:
                indice_pai1 = selecionar(populacao, fitnesses)
                indice_pai2 = selecionar(populacao, fitnesses)

            filhos = cruzar(populacao[indice_pai1], populacao[indice_pai2])
            for filho in filhos:
                filho_mutado = mutacao(
                    filho,
                    taxa_mutacao,
                    largura,
                    altura,
                )
                nova_populacao.append(filho_mutado)
                if len(nova_populacao) == tamanho_populacao:
                    break

        populacao = nova_populacao

    fim = time.perf_counter()
    duracao = fim - inicio

    fitnesses = [avaliar(individuo, hosts, raio_cobertura) for individuo in populacao]
    indice_melhor = max(range(len(populacao)), key=fitnesses.__getitem__)
    melhor_individuo = populacao[indice_melhor]
    melhor_fitness = fitnesses[indice_melhor]


    return melhor_individuo, melhor_fitness, duracao


def main():
    parser = argparse.ArgumentParser(description="Executa o algoritmo genético de cobertura.")
    parser.add_argument(
        "instancia",
        nargs="?",
        default="instancias/t1000n0u2.txt",
        help="Caminho do arquivo da instância (ignorado com --todas).",
    )
    parser.add_argument(
        "--todas",
        action="store_true",
        help="Executa todas as instâncias .txt da pasta instancias.",
    )
    parser.add_argument("--populacao", type=int, default=50)
    parser.add_argument("--geracoes", type=int, default=100)
    parser.add_argument("--taxa-mutacao", type=float, default=0.1)
    parser.add_argument("--raio", type=float, default=20)
    parser.add_argument("--selecao", choices=("roleta", "torneio"), default="torneio")
    parser.add_argument("--semente", type=int, default=141592)
    parser.add_argument(
        "--crossover",
        choices=("um_ponto", "uniforme", "media"),
        default="uniforme",
    )
    argumentos = parser.parse_args()

    instancias = (
        sorted(Path("instancias").glob("*.txt"))
        if argumentos.todas
        else [Path(argumentos.instancia)]
    )
    if not instancias:
        parser.error("Nenhuma instância .txt foi encontrada na pasta instancias.")

    random.seed(argumentos.semente)

    for instancia in instancias:
        _, cobertura, duracao = executar(
            str(instancia),
            argumentos.populacao,
            argumentos.geracoes,
            argumentos.taxa_mutacao,
            argumentos.selecao,
            argumentos.crossover,
            argumentos.raio,
            mostrar_visualizacao=False,
        )
        print(
            f"{argumentos.semente};{argumentos.selecao};{argumentos.crossover};"
            f"{instancia};{cobertura};{duracao}",
            flush=True,
        )


if __name__ == "__main__":
    main()

