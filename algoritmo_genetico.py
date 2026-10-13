import random

def inicializar_populacao(tamanho_populacao, quantidade_antenas, largura, altura):

    populacao = []
    for _ in range(tamanho_populacao):

        individuo = []

        for _ in range(quantidade_antenas):

            x = random.uniform(0, largura)
            y = random.uniform(0, altura)

            individuo.append((x, y))

        populacao.append(individuo)

    return populacao


def selecionar_roleta(populacao, fitnesses, soma):
    """
    Seleciona um indivíduo utilizando o método da roleta.

    soma: soma do fitness de toda a população.
    aux: acumula os fitness dos indivíduos.
    op: número aleatório entre 0 e a soma dos fitness.
    """

    if not populacao:
        raise ValueError("A população não pode estar vazia.")
    if len(populacao) != len(fitnesses):
        raise ValueError("Deve haver um fitness para cada indivíduo.")
    if soma <= 0:
        return random.randrange(len(populacao))

    op = random.uniform(0, soma)

    aux = 0

    for i in range(len(populacao)):

        aux = aux + fitnesses[i]

        if op < aux:
            return i

    return len(populacao) - 1


def selecionar_torneio(populacao, fitnesses, tamanho_torneio=3):
    """
    Seleciona um indivíduo pelo método de torneio.

    tamanho_torneio:
        quantidade de indivíduos sorteados para competir.

    Retorna o índice do indivíduo com maior fitness.
    """

    participantes = []

    for _ in range(tamanho_torneio):
        indice = random.randint(0, len(populacao) - 1)
        participantes.append(indice)

    melhor = participantes[0]

    for indice in participantes:
        if fitnesses[indice] > fitnesses[melhor]:
            melhor = indice

    return melhor

## ENTREGA
def crossover_um_ponto(pai1, pai2):
    """Combina os pais dividindo a lista de antenas em um ponto."""

    if len(pai1) != len(pai2):
        raise ValueError("Os pais devem possuir a mesma quantidade de antenas.")

    if len(pai1) < 2:
        return pai1.copy(), pai2.copy()

    ponto = random.randint(1, len(pai1) - 1)
    filho1 = pai1[:ponto] + pai2[ponto:]
    filho2 = pai2[:ponto] + pai1[ponto:]
    return filho1, filho2


## ENTREGA
def crossover_uniforme(pai1, pai2):
    """Escolhe aleatoriamente de qual pai vem cada posição de antena."""

    if len(pai1) != len(pai2):
        raise ValueError("Os pais devem possuir a mesma quantidade de antenas.")

    filho1 = []
    filho2 = []

    for gene1, gene2 in zip(pai1, pai2):
        if random.random() < 0.5:
            filho1.append(gene1)
            filho2.append(gene2)
        else:
            filho1.append(gene2)
            filho2.append(gene1)

    return filho1, filho2


## ENTREGA
def crossover_media(pai1, pai2):
    """Gera filhos cujas posições são a média das posições dos pais."""

    if len(pai1) != len(pai2):
        raise ValueError("Os pais devem possuir a mesma quantidade de antenas.")

    filho = [
        ((x1 + x2) / 2, (y1 + y2) / 2)
        for (x1, y1), (x2, y2) in zip(pai1, pai2)
    ]
    return filho, filho.copy()


## ENTREGA
def mutacao(individuo, taxa_mutacao, largura, altura):
    """Reposiciona cada antena com a probabilidade indicada pela taxa."""

    if not 0 <= taxa_mutacao <= 1:
        raise ValueError("A taxa de mutação deve estar entre 0 e 1.")
    if largura < 0 or altura < 0:
        raise ValueError("Largura e altura devem ser não negativas.")

    individuo_mutado = individuo.copy()

    for indice in range(len(individuo_mutado)):
        if random.random() < taxa_mutacao:
            individuo_mutado[indice] = (
                random.uniform(0, largura),
                random.uniform(0, altura),
            )

    return individuo_mutado


#inicializar()
#selecionar_roleta()
#selecionar_torneio() 
#crossover()
#mutacao()
#executar_algoritmo()