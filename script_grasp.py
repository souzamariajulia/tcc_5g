import os

sementes = [
    141592, 653589, 793238, 462643, 383279,
    502884, 197169, 399375, 105820, 974944,
    592307, 816406, 286208, 998628, 34825,
    342117, 67982, 148086, 513282, 306647,
    93844, 609550, 582231, 725359, 408128,
    481117, 450284, 102701, 938521, 105559
]

instancias = sorted(
    arquivo for arquivo in os.listdir("instancias")
    if arquivo.endswith(".txt")
)

for i in instancias:
    for sem in sementes:
        print("./venv/bin/python main_grasp.py instancias/{} --iteracoes 150 --fator-aleatoriedade 0.3 --passo 10 --semente {}".format(i, sem))