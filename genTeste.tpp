inteiro: n

inteiro fatorial(inteiro: n)
    inteiro: fat
    se n > 0 então {não calcula se n > 0}
        fat := 1
    senão
    	fat:=2
    fim
    retorna(fat)
fim

inteiro principal()
    leia(n)
    escreva(fatorial(n))
    retorna(0)
fim