# -*- coding: utf-8 -*-
#-------------------------------------------------------------------------
# lexer.py
# Analisador sintático e geração de uma árvore sintática abstrata para a
#   linguagem T++
# Autores:Humberto Gonçalves
#-------------------------------------------------------------------------
from ply import yacc
from analiseLexica import AnaliseLexica

class Tree:

    def __init__(self, type_node, child=[], value=None):
        self.type = type_node
        self.child = child
        self.value = value

    def __str__(self):

        return self.type


    def __str__(self, level = 0 ):
        print("| " * level + self.type +"\n")
        ret = "| " * level + self.type +"\n"
        level = level+1
        for child in self.child :
            ret += child.__str__(level)
        return ret


class AnaliseSintatica:

    def __init__(self, code):
        lex = AnaliseLexica()
        self.tokens = lex.tokens
        self.precedence = (
            ('left', 'VAZIO', 'INTEIRO', 'FLUTUANTE'),
            ('left', 'SENAO'),
            ('left', 'ATRIBUICAO', 'MENORIGUAL', 'MAIORIGUAL', 'MAIOR', 'MENOR', 'IGUALDADE'),
            ('left', 'ADICAO', 'SUBTRACAO'),
            ('left', 'MULTIPLICACAO', 'DIVISAO'),
        )
        parser = yacc.yacc(debug=True,module=self, optimize=False)
        self.ast = parser.parse(code)
        print(self.ast)


   
    def p_programa_1(self,p):
        'programa : principal'
        p[0] = Tree('programa_principal', [p[1]])

    #mais de uma funcao
    def p_programa_2(self, p):
        'programa : func_loop principal'
        p[0] = Tree('programa_funcao', [p[1],p[2]])

    #variavel global
    def p_programa_3(self, p):
        'programa : declara_var programa'
        p[0] = Tree('programa_varglobal', [p[1],p[2]])

    def p_principal_1(self, p):
        'principal :  PRINCIPAL ABREPAR declaracao_param FECHAPAR  sequencia_de_declaracao FIM'
        p[0] = Tree('principal', [p[3], p[5]], p[1])

    def p_principal_2(self, p):
        'principal :  PRINCIPAL ABREPAR  FECHAPAR sequencia_de_declaracao FIM'
        p[0] = Tree('principal', [p[4]], p[1] )

    def p_func_loop_1(self, p):
        'func_loop : declaracao_de_funcao func_loop'
        p[0] = Tree('func_loop', [p[1], p[2]])

    def p_func_loop_2(self, p):
        'func_loop : declaracao_de_funcao'
        p[0] = Tree('func_loop',[p[1]])


    def p_chamada_de_funcao(self, p):
        'chamada_de_funcao :  IDENTIFICADOR ABREPAR expressao FECHAPAR'
        p[0] = Tree('chamada_de_funcao',[p[3]], p[1])


    def p_declaracao_de_funcao(self, p):
        'declaracao_de_funcao : tipo IDENTIFICADOR ABREPAR declaracao_param FECHAPAR sequencia_de_declaracao FIM'
        p[0] = Tree('declaracao_de_funcao', [p[1],p[4], p[6]], p[2])

    def p_declaracao_param_1(self, p):
        'declaracao_param : declaracao_param VIRGULA tipo DOISPONTOS IDENTIFICADOR'
        p[0] = Tree('declaracao_param_loop', [p[1],p[3]], p[5])

    def p_declaracao_param_2(self, p): 
        'declaracao_param : tipo DOISPONTOS IDENTIFICADOR'
        p[0] = Tree('declaracao_param', [p[1]], p[3])


    def p_sequencia_de_declaracao_1(self, p):
        'sequencia_de_declaracao : declaracao sequencia_de_declaracao'
        p[0] = Tree('sequencia_de_declaracao',[p[1], p[2]])

    def p_sequencia_de_declaracao_2(self, p):
        'sequencia_de_declaracao : declaracao'
        p[0] = Tree('sequencia_de_declaracao', [p[1]])

    def p_declaracao_1(self, p):
        'declaracao : expressao_condicional'
        p[0] = Tree('declaracao', [] , [p[1]])

    def p_declaracao_2(self, p):
        'declaracao : expressao_iteracao'
        p[0] = Tree('declaracao', [p[1]])

    def p_declaracao_3(self, p):
        'declaracao : expressao_atribuicao'
        p[0] = Tree('declaracao', [p[1]])
    
    def p_declaracao_4(self, p):
        'declaracao : expressao_leitura'
        p[0] = Tree('declaracao', [p[1]])

    def p_declaracao_5(self, p):
        'declaracao : expressao_escreva'
        p[0] = Tree('declaracao', [p[1]])

    def p_declaracao_6(self, p):
        'declaracao : declara_var'
        p[0] = Tree('declaracao', [p[1]])

    def p_declaracao_7(self, p):
        'declaracao : retorna'
        p[0] = Tree('declaracao', [p[1]])

    def p_declaracao_8(self, p):
        'declaracao : chamada_de_funcao'
        p[0] = Tree('declaracao', [p[1]])


    def p_declara_var1(self, p):
        'declara_var : tipo IDENTIFICADOR VIRGULA declara_var'
        p[0] = Tree('declara_var', [p[1], p[3]], p[2])

    def p_declara_var2(self, p):
        'declara_var : tipo IDENTIFICADOR ATRIBUICAO expressao_simples'
        p[0] = Tree('declara_var', [p[1], p[4]], p[2])

    # def p_declara_var2(self, p):
    #     'declara_var : tipo IDENTIFICADOR ATRIBUICAO expressao_simples'
    #     p[0] = Tree('declara_var', [p[1], p[4]], p[2])
    
    def p_declara_var3(self, p):
        'declara_var : tipo DOISPONTOS IDENTIFICADOR'
        p[0] = Tree('declara_var', [p[1]], p[3])

    def p_retorna(self, p):
        '''
        retorna : RETORNA ABREPAR IDENTIFICADOR FECHAPAR
                | RETORNA ABREPAR NUMERO FECHAPAR
        '''
        p[0] = Tree('retorna', [p[3]])

    def p_expressao_condicional_1(self, p):
        'expressao_condicional : SE expressao ENTAO sequencia_de_declaracao SENAO sequencia_de_declaracao FIM'
        p[0] = Tree('expressao_condicional', [p[2],p[4], p[6]])

    def p_expressao_condicional_2(self, p):
        'expressao_condicional : SE expressao ENTAO sequencia_de_declaracao FIM'
        p[0] = Tree('expressao_condicional', [p[2],p[4]])

    def p_expressao_iteracao(self, p):
        'expressao_iteracao : REPITA sequencia_de_declaracao ATE expressao'
        p[0] =  Tree('expressao_iteracao', [p[2], p[4]])

    def p_expressao_atribuicao(self, p):
        'expressao_atribuicao : IDENTIFICADOR ATRIBUICAO expressao'
        p[0] =  Tree('expressao_atribuicao', [p[3]], p[1])


    def p_expressao_leitura(self, p):
        'expressao_leitura : LEIA ABREPAR IDENTIFICADOR FECHAPAR'
        p[0] = Tree('expressao_leitura', [], p[1])



    # def p_expressao_escreva_1(self, p):
    #     'expressao_escreva : ESCREVE ABREPAR  FECHAPAR'
    #     p[0] = Tree('expressao_escreva', [p[3]])

    def p_expressao_escreva_1(self, p):
        'expressao_escreva : ESCREVE ABREPAR expressao FECHAPAR'
        p[0] = Tree('expressao_escreva', [p[3]])

    def p_expressao_1(self, p):
        'expressao : expressao_simples operador_logico expressao_simples'
        p[0] =  Tree('expressao', [p[1],p[2], p[3]])

    def p_expressao_2(self, p):
        'expressao : expressao_simples'
        p[0]  = Tree('expressao', [], [p[1]])

    def p_expressao_3(self, p):
        'expressao : chamada_de_funcao'
        p[0]  = Tree('expressao', [], [p[1]])

    def p_operador_logico_1(self, p):
        'operador_logico : MAIOR'
        p[0]  = Tree('operador_logico', [], p[1])

    def p_operador_logico_2(self, p):
        'operador_logico : MAIORIGUAL'
        p[0]  = Tree('operador_logico',[], p[1])

    def p_operador_logico_3(self, p):
        'operador_logico : MENOR'
        p[0]  = Tree('operador_logico',[], p[1])

    def p_operador_logico_4(self, p):
        'operador_logico : MENORIGUAL'
        p[0]  = Tree('operador_logico',[], p[1])
    
    def p_operador_logico_5(self, p):
        'operador_logico : IGUALDADE'
        p[0]  = Tree('operador_logico',[], p[1])


    def p_expressao_simples_1(self, p):
        'expressao_simples : expressao_simples operador_add termo'
        p[0]  = Tree('expressao_simples', [p[1], p[2], p[3]])

    def  p_expressao_simples_2(self, p):
        'expressao_simples : termo'
        p[0]  = Tree('expressao_simples',[p[1]]) 

    def p_operador_add_1(self, p):
        'operador_add : ADICAO'
        p[0]  = Tree('operador_add',[], p[1])

    def p_operador_add_2(self, p):
        'operador_add : SUBTRACAO'
        p[0]  = Tree('operador_add',[], p[1])

    def p_termo_1(self, p):
        'termo : termo operador_mult fator'
        p[0]  = Tree('termo', [p[1], p[2], p[3]])

    def p_termo_2(self, p):
        'termo : fator'
        p[0]  =Tree('termo', [p[1]])    

    def p_operador_mult_1(self, p):
        'operador_mult : MULTIPLICACAO'
        p[0] = Tree('operador_mult',[] ,p[1])

    def p_operador_mult_2(self, p):  
        'operador_mult : DIVISAO'
        p[0] = Tree('operador_mult',[], p[1])

    def p_fator_1(self, p):
        'fator : NUMERO'
        p[0] = Tree('fator', [p[1]])

    def p_fator_2(self, p):
        'fator : IDENTIFICADOR'
        p[0] = Tree('fator', [p[1]])


    # def p_tipo(self, p):
    #     '''
    #     tipo : VAZIO
    #          | INTEIRO
    #          | FLUTUANTE
    #     '''
    #     p[0] = Tree('tipo', [], p[1])

    def p_tipo_1(self, p):
        ' tipo : VAZIO'
        p[0]  =Tree('tipo_vazio', [], p[1])

    def p_tipo_2(self, p):
        'tipo : INTEIRO'
        p[0]  = Tree('tipo_inteiro', [], p[1])

    def p_tipo_3(self, p):
        'tipo : FLUTUANTE'
        p[0]  = Tree('tipo_flutuante', [], p[1])

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
    AnaliseSintatica(f.read())