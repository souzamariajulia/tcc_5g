def criar_candidatos(hosts, largura, altura):
    return list(dict.fromkeys(
        (x, y) for x, y in hosts
        if 0 <= x <= largura and 0 <= y <= altura
    ))


def calcular_cobertura(posicao, hosts, raio_quadrado):
    x, y = posicao
    return {
        indice
        for indice, (host_x, host_y) in enumerate(hosts)
        if (x - host_x) ** 2 + (y - host_y) ** 2 <= raio_quadrado
    }


def construir_solucao(cobertura_candidatos, quantidade_antenas,
                      gerador_aleatorio):
    disponiveis = list(cobertura_candidatos)
    if not 0 <= quantidade_antenas <= len(disponiveis):
        raise ValueError('Quantidade inválida de antenas ou candidatos insuficientes.')

    solucao = []
    cobertos = set()

    for _ in range(quantidade_antenas):
        disponiveis.sort(
            key=lambda posicao: len(cobertura_candidatos[posicao] - cobertos),
            reverse=True,
        )

        posicao = gerador_aleatorio.choice(disponiveis[:3])
        solucao.append(posicao)
        cobertos.update(cobertura_candidatos[posicao])
        disponiveis.remove(posicao)

    return solucao


def busca_local(solucao, hosts, raio_quadrado, largura, altura, passo):
    estado_atual = [
        calcular_cobertura(posicao, hosts, raio_quadrado)
        for posicao in solucao
    ]
    total_coberto = len(set().union(*estado_atual))
    deslocamentos = (-passo, 0, passo)

    while total_coberto < len(hosts):
        melhor_movimento = None
        melhor_total = total_coberto

        for indice, (x, y) in enumerate(solucao):
            cobertura_outras = set().union(
                *estado_atual[:indice], *estado_atual[indice + 1:]
            )

            for dx in deslocamentos:
                for dy in deslocamentos:
                    nova_posicao = (x + dx, y + dy)
                    novo_x, novo_y = nova_posicao

                    if not (0 <= novo_x <= largura and 0 <= novo_y <= altura):
                        continue
                    if nova_posicao in solucao:
                        continue

                    nova_cobertura = calcular_cobertura(
                        nova_posicao, hosts, raio_quadrado
                    )
                    novo_total = len(cobertura_outras | nova_cobertura)

                    if novo_total > melhor_total:
                        melhor_total = novo_total
                        melhor_movimento = (indice, nova_posicao, nova_cobertura)

        if melhor_movimento is None:
            break

        indice, nova_posicao, nova_cobertura = melhor_movimento
        solucao[indice] = nova_posicao
        estado_atual[indice] = nova_cobertura
        total_coberto = melhor_total

    return solucao, total_coberto