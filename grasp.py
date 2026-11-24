

def criar_candidatos(hosts, largura, altura):
    """Seleciona coordenadas válidas e distintas dos hosts."""
    return list(dict.fromkeys(
        (x, y) for x, y in hosts
        if 0 <= x <= largura and 0 <= y <= altura
    ))


def mascara_cobertura(posicao, hosts, raio_quadrado):
    """Representa os hosts cobertos por uma posição usando bits."""
    x, y = posicao
    mascara = 0
    for indice, (host_x, host_y) in enumerate(hosts):
        distancia_x = x - host_x
        distancia_y = y - host_y
        if distancia_x * distancia_x + distancia_y * distancia_y <= raio_quadrado:
            mascara |= 1 << indice
    return mascara


def obter_mascara(posicao, hosts, raio_quadrado, cache_cobertura):
    """Calcula a cobertura somente para posições ainda não avaliadas."""
    if posicao not in cache_cobertura:
        cache_cobertura[posicao] = mascara_cobertura(posicao, hosts, raio_quadrado)
    return cache_cobertura[posicao]


def construir_solucao(candidatos, mascaras_cobertura, quantidade_antenas,
                      fator_aleatoriedade, gerador_aleatorio):
    """Constrói uma solução com escolhas gulosas e aleatoriedade controlada."""
    if not 0 <= quantidade_antenas <= len(candidatos):
        raise ValueError('Quantidade inválida de antenas ou candidatos insuficientes.')
    if not 0 <= fator_aleatoriedade <= 1:
        raise ValueError('O fator de aleatoriedade deve estar entre 0 e 1.')

    solucao = []
    cobertura_atual = 0
    indices_disponiveis = list(range(len(candidatos)))

    for _ in range(quantidade_antenas):
        hosts_nao_cobertos = ~cobertura_atual
        ganhos_cobertura = [
            (mascaras_cobertura[indice] & hosts_nao_cobertos).bit_count()
            for indice in indices_disponiveis
        ]
        maior_ganho = max(ganhos_cobertura)
        menor_ganho = min(ganhos_cobertura)
        limite_ganho = maior_ganho - fator_aleatoriedade * (maior_ganho - menor_ganho)
        lista_restrita_candidatos = [
            indice for indice, ganho in zip(indices_disponiveis, ganhos_cobertura)
            if ganho >= limite_ganho
        ]
        indice_escolhido = gerador_aleatorio.choice(lista_restrita_candidatos)
        solucao.append(candidatos[indice_escolhido])
        cobertura_atual |= mascaras_cobertura[indice_escolhido]
        indices_disponiveis.remove(indice_escolhido)

    return solucao


def unir_coberturas(mascaras):
    cobertura = 0
    for mascara in mascaras:
        cobertura |= mascara
    return cobertura


def busca_local(solucao, hosts, raio_quadrado, largura, altura, passo,
                cache_cobertura):
    """Aplica o melhor movimento até não existir melhoria na cobertura."""
    mascaras_antenas = [
        obter_mascara(posicao, hosts, raio_quadrado, cache_cobertura)
        for posicao in solucao
    ]
    hosts_cobertos = unir_coberturas(mascaras_antenas).bit_count()
    posicoes_ocupadas = set(solucao)
    movimentos = [
        (-passo, -passo), (-passo, 0), (-passo, passo),
        (0, -passo),                    (0, passo),
        (passo, -passo),  (passo, 0),  (passo, passo)
    ]

    while hosts_cobertos < len(hosts):
        melhor_movimento = None
        melhor_cobertura = hosts_cobertos

        for indice, (x, y) in enumerate(solucao):
            # Mantém fixas todas as antenas, exceto a que será movida.
            cobertura_outras = unir_coberturas(
                mascaras_antenas[:indice] + mascaras_antenas[indice + 1:]
            )

            for deslocamento_x, deslocamento_y in movimentos:
                nova_posicao = (x + deslocamento_x, y + deslocamento_y)
                novo_x, novo_y = nova_posicao

                if not (0 <= novo_x <= largura and 0 <= novo_y <= altura):
                    continue
                if nova_posicao in posicoes_ocupadas:
                    continue

                nova_mascara = obter_mascara(
                    nova_posicao, hosts, raio_quadrado, cache_cobertura
                )
                nova_cobertura = (cobertura_outras | nova_mascara).bit_count()

                if nova_cobertura > melhor_cobertura:
                    melhor_cobertura = nova_cobertura
                    melhor_movimento = (indice, nova_posicao, nova_mascara)

        if melhor_movimento is None:
            break

        # Aplica somente o melhor movimento encontrado na rodada.
        indice, nova_posicao, nova_mascara = melhor_movimento
        posicoes_ocupadas.remove(solucao[indice])
        posicoes_ocupadas.add(nova_posicao)
        solucao[indice] = nova_posicao
        mascaras_antenas[indice] = nova_mascara
        hosts_cobertos = melhor_cobertura

    return solucao, hosts_cobertos