selecao = ["roleta", "torneio"]
crossover = ["um_ponto", "uniforme", "media"]
sementes = [141592, 653589, 793238, 462643, 383279, 
            502884, 197169, 399375, 105820, 974944, 
            592307, 816406, 286208, 998628,  34825, 
            342117,  67982, 148086, 513282, 306647, 
             93844, 609550, 582231, 725359, 408128, 
            481117, 450284, 102701, 938521, 105559] 

instancias = ["t100000n0u2.txt", "t100000n3u8.txt", "t100000n7u6.txt", "t10000n1u4.txt", "t10000n5u2.txt", "t10000n8u8.txt", "t1000n2u6.txt", "t1000n6u4.txt",
"t100000n0u4.txt", "t100000n4u2.txt", "t100000n7u8.txt", "t10000n1u6.txt", "t10000n5u4.txt", "t10000n9u2.txt", "t1000n2u8.txt", "t1000n6u6.txt",
"t100000n0u6.txt", "t100000n4u4.txt", "t100000n8u2.txt", "t10000n1u8.txt", "t10000n5u6.txt", "t10000n9u4.txt", "t1000n3u2.txt", "t1000n6u8.txt",
"t100000n0u8.txt", "t100000n4u6.txt", "t100000n8u4.txt", "t10000n2u2.txt", "t10000n5u8.txt", "t10000n9u6.txt", "t1000n3u4.txt", "t1000n7u2.txt",
"t100000n1u2.txt", "t100000n4u8.txt", "t100000n8u6.txt", "t10000n2u4.txt", "t10000n6u2.txt", "t10000n9u8.txt", "t1000n3u6.txt", "t1000n7u4.txt",
"t100000n1u4.txt", "t100000n5u2.txt", "t100000n8u8.txt", "t10000n2u6.txt", "t10000n6u4.txt", "t1000n0u2.txt", "t1000n3u8.txt", "t1000n7u6.txt",
"t100000n1u6.txt", "t100000n5u4.txt", "t100000n9u2.txt", "t10000n2u8.txt", "t10000n6u6.txt", "t1000n0u4.txt", "t1000n4u2.txt", "t1000n7u8.txt",
"t100000n1u8.txt", "t100000n5u6.txt", "t100000n9u4.txt", "t10000n3u2.txt", "t10000n6u8.txt", "t1000n0u6.txt", "t1000n4u4.txt", "t1000n8u2.txt",
"t100000n2u2.txt", "t100000n5u8.txt", "t100000n9u6.txt", "t10000n3u4.txt", "t10000n7u2.txt", "t1000n0u8.txt", "t1000n4u6.txt", "t1000n8u4.txt",
"t100000n2u4.txt", "t100000n6u2.txt", "t100000n9u8.txt", "t10000n3u6.txt", "t10000n7u4.txt", "t1000n1u2.txt", "t1000n4u8.txt", "t1000n8u6.txt",
"t100000n2u6.txt", "t100000n6u4.txt", "t10000n0u2.txt", "t10000n3u8.txt", "t10000n7u6.txt", "t1000n1u4.txt", "t1000n5u2.txt", "t1000n8u8.txt",
"t100000n2u8.txt", "t100000n6u6.txt", "t10000n0u4.txt", "t10000n4u2.txt", "t10000n7u8.txt", "t1000n1u6.txt", "t1000n5u4.txt", "t1000n9u2.txt",
"t100000n3u2.txt", "t100000n6u8.txt", "t10000n0u6.txt", "t10000n4u4.txt", "t10000n8u2.txt", "t1000n1u8.txt", "t1000n5u6.txt", "t1000n9u4.txt",
"t100000n3u4.txt", "t100000n7u2.txt", "t10000n0u8.txt", "t10000n4u6.txt", "t10000n8u4.txt", "t1000n2u2.txt", "t1000n5u8.txt", "t1000n9u6.txt",
"t100000n3u6.txt", "t100000n7u4.txt", "t10000n1u2.txt", "t10000n4u8.txt", "t10000n8u6.txt", "t1000n2u4.txt", "t1000n6u2.txt", "t1000n9u8.txt"]

for s in selecao:
    for c in crossover:
        for i in instancias:
            for sem in sementes:
                print("./venv/bin/python main.py instancias/{} --populacao 100 --selecao {} --crossover {} --geracoes 150 --semente {}".format(i, s, c, sem)) 
