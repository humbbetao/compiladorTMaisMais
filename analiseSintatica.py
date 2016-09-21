# -*- coding: utf-8 -*-
#-------------------------------------------------------------------------
# lexer.py
# Analisador sintático e geração de uma árvore sintática abstrata para a
#   linguagem T++
# Autores:Humberto Gonçalves
#-------------------------------------------------------------------------

from ply import yacc
from AnaliseLexica import AnaliseLexica

class Tree:

    def __init__(self, type_node, child=[], value=''):
        self.type = type_node
        self.child = child
        self.value = value

    def __str__(self):

        return self.type

class Parser:

	def __init__(self, code):
	    lex = AnaliseLexica();
        self.tokens = lex.tokens
        self.precedence = (	('left', 'ELSE'),
                        	('left', 'IGUALDADE', 'MAIOR', 'MAIORIGUAL', 'MENOR', 'MENORIGUAL', 'ATRIBUICAO'),
                        	('left', 'ADICAO', 'SUBTRACAO'),
                        	('left', 'MULTIPLICACAO', 'DIVISAO'), );
        parser = yacc.yacc(debug = False, module = self, optimize = False)
        self.ast = parser.parse(code)

    def p_programa_1(p):
        'programa : principal'
        p[0] = Tree('programa_principal', [p[1]])

    #mais de uma funcao
    def p_programa_2(p):
        'programa : func_loop principal'
        p[0] = Tree('programa_funcao', [p[1],p[2]])

    #variavel global
    def p_programa_3(p):
        'programa : declara_var programa'
        p[0] = Tree('programa_varglobal', [p[1],p[2]])

    def p_principal(p):
        'principal:  VAZIO PRINCIPAL ABREPAR declaracao_param FECHAPAR NOVA_LINHA  sequencia_de_declaracao FIM'
        p[0] = Tree('principal', [p[1], p[4], p[7]], p[2])

    def p_func_loop_1(p):
        'func_loop : declaracao_de_funcao func_loop'
        p[0] = Tree('func_loop', [p[1], p[2]])

    def p_func_loop_2(p):
        'func_loop : declaracao_de_funcao'
        p[0] = Tree('func_loop',[p[1]])

    def p_declaracao_de_funcao(p):
        'declaracao_de_funcao : tipo IDENTIFICADOR ABREPAR declaracao_param FECHAPAR NOVALINHA sequencia_de_declaracao FIM'
        p[0] = Tree('declaracao_de_funcao', [p[1],p[4], p[7]], p[2])

    def p_declaracao_param_1(p):
        'declaracao_param : tipo DOISPONTOS IDENTIFICADOR declaracao_param'
        p[0] = Tree('declaracaod_param', [p[1], p[4]])

    def p_declaracao_param_2(p): 
        'declaracao_param : tipo DOISPONTOS IDENTIFICADOR'
        p[0] = Tree('declaracaod_param', [p[1]])

    def p_sequencia_de_declaracao_1(p):
        'sequencia_de_declaracao : sequencia_de_declaracao declaracao'
        p[0] = Tree('sequencia_de_declaracao',[p[1], p[2]])

     def p_sequencia_de_declaracao_2(p):
        'sequencia_de_declaracao : declaracao'
        p[0] = Tree('sequencia_de_declaracao', [p[1]])

    def p_declaracao_1(p):
        'declaracao : expressao_condicional'
        p[0] = Tree('declaracao', [p[1]])

    def p_declaracao_2(p):
        'declaracao : expressao_iteracao'
        p[0] = Tree('declaracao', [p[1]])

    def p_declaracao_3(p):
        'declaracao : expressao_atribuicao'
        p[0] = Tree('declaracao', [p[1]])
    
    def p_declaracao_4(p):
        'declaracao : expressao_leitura'
        p[0] = Tree('declaracao', [p[1]])

    def p_declaracao_5(p):
        'declaracao : expressao_escreva'
        p[0] = Tree('declaracao', [p[1]])

    def p_declaracao_6(p):
        'declaracao : declaracao_var'
        p[0] = Tree('declaracao', [p[1]])

    def p_expressao_condicional_1(p):
        'expressao_condicional : SE expressao ENTAO sequencia_de_declaracao SENAO sequencia_de_declaracao FIM'
        p[0] = Tree('expressao_condicional', [p[2],p[4], p[6]])

    def p_expressao_condicional_1(p):
        'expressao_condicional : SE expressao ENTAO sequencia_de_declaracao FIM'
        p[0] = Tree('expressao_condicional', [p[2],p[4]])

    def p_expressao_iteracao(p):
        'expressao_iteracao : REPITA sequencia_de_declaracao ATE expressao'
        p[0] =  Tree('expressao_iteracao', [p[2], p[4]])

    def p_expressao_atribuicao(p):
        'expressao_atribuicao : IDENTIFICADOR ATRIBUICAO expressao'
        p[0] =  Tree('expressao_atribuicao', [p[3]], p[1])

    def p_expressao_leitura(p):
        'expressao_leitura : LEIA ABREPAR IDENTIFICADOR FECHAPAR'
        p[0] = Tree('expressao_leitura', [], p[1])

    def p_expressao_escreva(p):
        'expressao_escreva : ESCREVA ABREPAR expressao FECHAPAR'
        p[0] = Tree('expressao_escreva', [p[3]])

    def p_expressao_1(p):
        'expressao : expressao_simples operador_logico expressao_simples'
        p[0] =  Tree('expressao', [p[1],p[2], p[3]])

    def p_expressao_2(p):
        'expressao : expressao_simples'
        p[0]  = Tree('expressao', [p[1]])

    def p_operador_logico_1(p):
        'operador_logico : MAIOR'
        p[0]  = Tree('operador_logico')

    def p_operador_logico_2(p):
        'operador_logico : MAIORIGUAL'
        p[0]  = Tree('operador_logico')

    def p_operador_logico_3(p):
        'operador_logico : MENOR'
        p[0]  = Tree('operador_logico')

    def p_operador_logico_4(p):
        'operador_logico : MENORIGUAL'
        p[0]  = Tree('operador_logico')
    
    def p_operador_logico_5(p):
        'operador_logico : IGUALDADE'
        p[0]  = Tree('operador_logico')


    def p_expressao_simples_1(p):
        'expressao_simples : expressao_simples operador_add termo'
        p[0]  = Tree('expressao_simples', [p[1], p[2], p[3]])

    def  p_expressao_simples_2(p):
        'expressao_simples : termo'
        p[0]  = Tree('expressao_simples', [p[1]]) 

    def p_operador_add_1(p):
        'operador_add : ADICAO'
        p[0]  = Tree('operador_add')

    def p_operador_add_1(p):
        'operador_add : SUBTRACAO'
        p[0]  =/ Tree('operador_add')

    def p_termo_1(p):
        'termo : termo operador_mult fator'
        p[0]  = Tree('termo', [p[1], p[2], p[3]])

    def p_termo_2(p):
        'termo : fator'
        p[0]  =Tree('termo', [p[1]])    

    def p_operador_mult_1(p):
        'operador_mult : MULTIPLICACAO'
        p[0] = Tree('operador_mult')



    def p_operador_mult_2(p):  
        'operador_mult : DIVISAO'
        p[0] = Tree('operador_mult')

    def p_fator_1(p):
        'fator : NUMERO'
        p[0] = Tree('fator', [p[1]])

    def p_fator_2(p):
        'fator : IDENTIFICADOR'
        p[0] = Tree('fator', [p[1]])


    def p_tipo_1(p):
        'tipo : VAZIO'
        p[0]  =Tree('tipo', [], p[1])

    def p_tipo_1(p):
        'tipo : INTEIRO'
        p[0]  =Tree('tipo', [], p[1])

    def p_tipo_1(p):
        'tipo : FLUTUANTE'
        p[0]  =Tree('tipo', [], p[1])

    def p_error(self, p):
        if p:
            print("Erro sintático: '%s', linha %d" % (p.value, p.lineno))
            exit(1)
        else:
            yacc.restart()
            print('Erro sintático: definições incompletas!')
            exit(1)

if __name__ == '__main__':
    from sys import argv, exit
    f = open(argv[1])
    Parser(f.read())


