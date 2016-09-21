# -*- coding: utf-8 -*-
#-------------------------------------------------------------------------
# analiseLexica.py
# Analisador léxico para a linguagem T++
# Autores: Humberto Moreira Gonçalves
#-------------------------------------------------------------------------

import ply.lex as lex

class AnaliseLexica:
	
	def __init__(self):
       		self.lexer = lex.lex(debug=False, module=self, optimize=False)	

    # Dicionario reservadas
	keywords = {
		u'se': 'SE',
		u'então': 'ENTAO',
		u'senão': 'SENAO',
		u'fim': 'FIM',
		u'repita': 'REPITA',
		u'flutuante': 'FLUTUANTE',
		u'retorna': 'RETORNA',
		u'até': 'ATE',
		u'leia': 'LEIA',
		u'escreva': 'ESCREVE',
		u'inteiro': 'INTEIRO',
		u'principal': 'PRINCIPAL',
		u'vazio': 'VAZIO',
		u'retorna' : 'RETORNA',

		}

	# Lista de Tokens
	tokens = ['ADICAO', 'SUBTRACAO', 'MULTIPLICACAO', 'DIVISAO', 'IGUALDADE', 
				'VIRGULA', 'ATRIBUICAO', 'MENOR', 'MAIOR', 'MENORIGUAL', 'MAIORIGUAL',
				 'ABREPAR', 'FECHAPAR', 'DOISPONTOS','NUMERO', 'IDENTIFICADOR', 'ERRO'] + list(keywords.values())

	# Expressões simples
	t_ADICAO = r'\+'
	t_SUBTRACAO = r'\-'
	t_MULTIPLICACAO = r'\*'
	t_DIVISAO = r'/'
	t_IGUALDADE = r'='
	t_VIRGULA = r','
	t_ATRIBUICAO = r':='
	t_MENOR  = r'<'
	t_MAIOR = r'>'
	t_MENORIGUAL = r'<='
	t_MAIORIGUAL = r'>='
	t_ABREPAR = r'\('
	t_FECHAPAR = r'\)'
	t_DOISPONTOS = r':'
	t_NUMERO = r'[+-]?[0-9]+(\.[0-9]+)?([eE][+-]?[0-9]+)?'


	def t_IDENTIFICADOR(self, t):
		r'[a-zA-Zà-ÿÀ-Ÿ][a-zA-Zà-ÿÀ-Ÿ0-9]*'
		t.type = self.keywords.get(t.value, 'IDENTIFICADOR')
		return t

	def t_COMENTARIO(self, t):
		r'({(.|\n)*?\})'
		pass

	def t_NOVALINHA(self, t):
		r'\n+'
		t.lexer.lineno += len(t.value)
	#Ignora tabs e espacos
	t_ignore = ' \t'

	def t_error(self, t):
		print("Item ilegal: '%s', linha %d, coluna %d" % (t.value[0], t.lineno, t.lexpos))
		t.lexer.skip(1)

	def test(self, code):
		lex.input(code)
		while True:
		    t = lex.token()
		    if not t:
		        break
		    print(t)

if __name__ == '__main__':
	from sys import argv
	lexer = AnaliseLexica()
	f = open(argv[1])
	lexer.test(f.read())
