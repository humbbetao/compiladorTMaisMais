# -*- coding: utf-8 -*-
#-------------------------------------------------------------------------
# analiseLexica.py
# Analisador léxico para a linguagem T++
# Autores: Humberto Moreira Gonçalves
#-------------------------------------------------------------------------

import ply.lex as lex

class AnaliseLexica:
	
	def __init__(self):
       		self.lexer = lex.lex(debug=True, module=self, optimize=False)

	keywords = {
		u'se': 'se',
		u'então': 'entao',
		u'senão': 'senao',
		u'fim': 'fim',
		u'repita': 'repita',
		u'flutuante': 'flutuante',
		u'retorna': 'retorna',
		u'até': 'ate',
		u'leia': 'leia',
		u'escreve': 'escreve',
		u'inteiro': 'inteiro',
		}

	tokens = ['ADICAO', 'SUBTRACAO', 'MULTIPLICACAO', 'DIVISAO', 'IGUALDADE', 
				'VIRGULA', 'ATRIBUICAO', 'MENOR', 'MAIOR', 'MENORIGUAL', 'MAIORIGUAL',
				 'ABREPAR', 'FECHAPAR', 'DOISPONTOS','NUMERO', 'ID'] + list(keywords.values())

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
	t_NUMERO = r'[0-9]+(\.[0-9]+)?'

	def t_ID(self, t):
		r'[a-zA-Z][a-zA-Zá-ñÁ-Ñ0-9]*'
		t.type = self.keywords.get(t.value, 'ID')
		return t

	def t_COMMENT(self, t):
		r'{[^\{^\}]*}'
		pass

	def t_NEWLINE(self, t):
		r'\n+'
		t.lexer.lineno += len(t.value)
	
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
