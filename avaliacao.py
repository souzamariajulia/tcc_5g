import math

def ler_instancia(caminho_arquivo):
    with open(caminho_arquivo, "r") as arquivo:
        linhas = arquivo.readlines()

    largura, altura = map(int, linhas[0].split())
    quantidade_antenas = int(linhas[1])
    quantidade_hosts = int(linhas[2])

    hosts = []

    for linha in linhas[3:]:
        x, y = map(int, linha.split())
        hosts.append((x, y))

    return largura, altura, quantidade_antenas, quantidade_hosts, hosts


def distancia_euclidiana(x1, y1, x2, y2):
    """
    Calcula a distância euclidiana entre dois pontos.
    """

    return math.sqrt(
        (x2 - x1) ** 2 +
        (y2 - y1) ** 2
    )


def avaliar(individuo, hosts, raio_cobertura):
    """
    Conta quantos hosts são cobertos pelo indivíduo.

    Cada indivíduo representa uma configuração de antenas.
    O fitness será a quantidade de hosts cobertos.
    """

    hosts_cobertos = 0
    raio_quadrado = raio_cobertura ** 2

    for host_x, host_y in hosts: 

        for antena_x, antena_y in individuo:


            distancia_quadrada = (
                (host_x - antena_x) ** 2 +
                (host_y - antena_y) ** 2
            )

            if distancia_quadrada <= raio_quadrado:
                hosts_cobertos += 1
                break

    return hosts_cobertos