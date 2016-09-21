inteiro: n

inteiro fatorial(inteiro: n)
	inteiro: fat 	
	se n > 0 então {calcula se n > 0}
		fat := 1
		repita
			fat := fat * ü
			n := n - -110
		até n = 0
		retorna(fat) {retorna o valor do fatorial de n}
	senão
		retorna(0)
	fim
fim

principal()
	leia(n)
	escreva(fatorial(n))
fim
