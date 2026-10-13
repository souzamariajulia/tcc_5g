import argparse

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
from visualizacao import visualizar


def executar(
    caminho_instancia,
    tamanho_populacao=50,
    geracoes=100,
    taxa_mutacao=0.1,
    metodo_selecao="torneio",
    metodo_crossover="uniforme",
    raio_cobertura=20,
):
    if tamanho_populacao < 1:
        raise ValueError("O tamanho da população deve ser pelo menos 1.")
    if geracoes < 0:
        raise ValueError("O número de gerações não pode ser negativo.")

    largura, altura, quantidade_antenas, quantidade_hosts, hosts = ler_instancia(
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

    fitnesses = [avaliar(individuo, hosts, raio_cobertura) for individuo in populacao]
    indice_melhor = max(range(len(populacao)), key=fitnesses.__getitem__)
    melhor_individuo = populacao[indice_melhor]
    melhor_fitness = fitnesses[indice_melhor]

    print(
        f"Melhor indivíduo: {melhor_fitness}/{quantidade_hosts} hosts cobertos "
        f"({caminho_instancia})"
    )
    visualizar(
        melhor_individuo,
        hosts,
        raio_cobertura,
        largura,
        altura,
    )
    return melhor_individuo, melhor_fitness


def main():
    parser = argparse.ArgumentParser(description="Executa o algoritmo genético de cobertura.")
    parser.add_argument(
        "instancia",
        nargs="?",
        default="instancias/t1000n0u2.txt",
        help="Caminho do arquivo da instância.",
    )
    parser.add_argument("--populacao", type=int, default=50)
    parser.add_argument("--geracoes", type=int, default=100)
    parser.add_argument("--taxa-mutacao", type=float, default=0.1)
    parser.add_argument("--raio", type=float, default=20)
    parser.add_argument("--selecao", choices=("roleta", "torneio"), default="torneio")
    parser.add_argument(
        "--crossover",
        choices=("um_ponto", "uniforme", "media"),
        default="uniforme",
    )
    argumentos = parser.parse_args()

    executar(
        argumentos.instancia,
        argumentos.populacao,
        argumentos.geracoes,
        argumentos.taxa_mutacao,
        argumentos.selecao,
        argumentos.crossover,
        argumentos.raio,
    )


if __name__ == "__main__":
    main()