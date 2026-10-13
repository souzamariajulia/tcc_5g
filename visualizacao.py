import matplotlib.pyplot as plt

def visualizar(individuo, hosts, raio_cobertura, largura, altura):
  
    fig, ax = plt.subplots()

    for x, y in hosts:
        ax.scatter(x, y)

    for x, y in individuo:
        ax.scatter(x, y, marker="^", s=100)

        cobertura = plt.Circle(
            (x, y),
            raio_cobertura,
            fill=False
        )

        ax.add_patch(cobertura)

    ax.set_xlim(0, largura)
    ax.set_ylim(0, altura)

    ax.set_xlabel("X")
    ax.set_ylabel("Y")

    ax.set_title("Posicionamento das Antenas")

    ax.set_aspect("equal")

    plt.show()