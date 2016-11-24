flutuante: n

inteiro fatorial(inteiro: n, inteiro:d, inteiro:j)
    inteiro: fat
    se n > 0 então {não calcula se n > 0}
        fat := 1
        repita
            fat := fat * n
            n := n - 1.0
        até n = 0
        retorna(fat) {retorna o valor do fatorial de n}
    senão
        retorna(0)
    fim
fim

inteiro principal()
inteiro:m
flutuante : d
    leia(n)
    escreva(fatorial(n,m,d))
    retorna(0)
fim