import math

def ler_instancia(caminho_arquivo):
    with open(caminho_arquivo, "r") as arquivo:
        linhas = arquivo.readlines()

    largura, altura = map(int, linhas[0].split())
    quantidade_antenas = int(linhas[1])
    quantidade_hosts = int(linhas[2])

    if largura ==  1000:
        raio_cobertura = 300
    else:
        raio_cobertura = 3000


    hosts = []

    for linha in linhas[3:]:
        x, y = map(int, linha.split())
        hosts.append((x, y))

    return largura, altura, quantidade_antenas, quantidade_hosts, hosts, raio_cobertura


def distancia_euclidiana(x1, y1, x2, y2):
    return math.sqrt(
        (x2 - x1) ** 2 +
        (y2 - y1) ** 2
    )


def avaliar(individuo, hosts, raio_cobertura):
    hosts_cobertos = 0
    raio_quadrado = raio_cobertura

    for host_x, host_y in hosts: 

        for antena_x, antena_y in individuo:


            distancia_quadrada = math.sqrt (
                (host_x - antena_x) ** 2 +
                (host_y - antena_y) ** 2
            )

            if distancia_quadrada <= raio_quadrado:
                hosts_cobertos += 1
                break

    return hosts_cobertos