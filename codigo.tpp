inteiro: n,b

inteiro fatorial(inteiro : n)
	  {funciona, mas não sei se a precedencia ta certo}
	se n  > ( datorial (n) ) então {calcula se n > 0}
		fat := 1
		repita
		n := n - -110.0
		até n = 0
		retorna(fat) {retorna o valor do fatorial de n}
	senão
		retorna(0)
	fim
fim

inteiro: a

inteiro fatorial(inteiro : n)
fim

inteiro: b

principal()
	leia(n)
	escreva(fatorial(n))
fat := 2 + 2 + 2
fim
