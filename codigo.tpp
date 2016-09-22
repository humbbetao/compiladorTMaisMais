inteiro: n,b

inteiro fatorial(inteiro : n)
	fat := fat * (2 + 2) {funciona, mas não sei se a precedencia ta certo}
	se n > 0 então {calcula se n > 0}
		fat := 1
		repita
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
