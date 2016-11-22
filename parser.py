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


    # def __str__(self, level = 0 ):
    #     # print("| " * level + self.type +"\n")
    #    ret = "| " * level + self.type +"\n"
    #    level = level+1
    #    for child in self.child :
    #        ret += child.__str__(level)

    #    return ret


class AnaliseSintatica:

    def __init__(self):
        lex = AnaliseLexica()
        self.tokens = lex.tokens
        self.precedence = (
            ('left', 'ATRIBUICAO', 'MENORIGUAL', 'MAIORIGUAL', 'MAIOR', 'MENOR', 'IGUALDADE'),
            ('left', 'ADICAO', 'SUBTRACAO'),
            ('left', 'MULTIPLICACAO', 'DIVISAO'),
            ('left', 'ABREPAR','FECHAPAR'),
        )
        # parser = yacc.yacc(debug=True,module=self, optimize=False)
        # self.ast = parser.parse(code)



    # def sintatica(self,code):
    #     parser =  yacc.yacc(debug=True)
    #     return parser.parse(code)

        # print(self.ast)

    def p_programa_1(self,p):
        'programa : statement programa'
        p[0] = Tree('statement_loop', [p[1], p[2]])

    def p_programa_2(self,p):
        'programa : statement '
        p[0] = Tree('statement_sem_loop', [p[1]])

    #mais de uma funcao
    def p_statement_1(self, p):
        'statement : declaracao_de_funcao'
        p[0] = Tree('statement_declaracao_de_funcao', [p[1]])

    def p_statement_2(self, p):
        'statement : declara_var'
        p[0] = Tree('statement_declara_var', [p[1]])





    def p_declaracao_de_funcao_1(self, p):
        'declaracao_de_funcao : tipo IDENTIFICADOR ABREPAR declaracao_param FECHAPAR sequencia_de_declaracao FIM'
        p[0] = Tree('declaracao_de_funcao_td', [p[1],p[4], p[6]], p[2])

    def p_declaracao_de_funcao_2(self, p):
        'declaracao_de_funcao : tipo IDENTIFICADOR ABREPAR declaracao_param FECHAPAR  FIM'
        p[0] = Tree('declaracao_de_funcao_sem_corpo', [p[1],p[4]], p[2])

    def p_declaracao_de_funcao_3(self, p):
        'declaracao_de_funcao : tipo IDENTIFICADOR ABREPAR FECHAPAR  FIM'
        p[0] = Tree('declaracao_de_funcao_sem_corpo_sem_parametros', [p[1]], p[2])

    def p_declaracao_de_funcao_4(self, p):
        'declaracao_de_funcao : tipo IDENTIFICADOR ABREPAR FECHAPAR sequencia_de_declaracao FIM'
        p[0] = Tree('declaracao_de_funcao_sem_param_com_corpo', [p[1],p[5]], p[2])

    def p_declaracao_param_1(self, p):
        'declaracao_param : tipo DOISPONTOS IDENTIFICADOR VIRGULA declaracao_param '
        p[0] = Tree('declaracao_param_loop', [p[1],p[5]], p[3])

    def p_declaracao_param_2(self, p): 
        'declaracao_param : tipo DOISPONTOS IDENTIFICADOR'
        p[0] = Tree('declaracao_param', [p[1]], p[3])


    def p_sequencia_de_declaracao_1(self, p):
        'sequencia_de_declaracao : declaracao'
        p[0] = Tree('sequencia_de_declaracao_sem_loop', [p[1]])

    def p_sequencia_de_declaracao_2 (self, p):
        'sequencia_de_declaracao : declaracao sequencia_de_declaracao'
        p[0] = Tree('sequencia_de_declaracao_loop',[p[1], p[2]])

    # def p_declaracao(self, p):
    #     '''
    #         declaracao : expressao_condicional 
    #                    | expressao_iteracao
    #                    | expressao_atribuicao
    #                    | expressao_leitura
    #                    | expressao_escreva
    #                    | declara_var
    #                    | retorna
    #                    | chamada_de_funcao
                      
    #     '''
    #     p[0] = Tree('declaracao', [p[1]] )


    def p_declaracao_1(self, p):
        'declaracao : expressao_condicional '
        p[0] = Tree('declaracao_expressao_condicional', [p[1]] )


    def p_declaracao_2(self, p):
        'declaracao : expressao_iteracao '
        p[0] = Tree('declaracao_expressao_iteracao', [p[1]] )

    def p_declaracao_3(self, p):
        'declaracao : expressao_atribuicao '
        p[0] = Tree('declaracao_expressao_atribuicao', [p[1]] )


    def p_declaracao_4(self, p):
        'declaracao : expressao_leitura '
        p[0] = Tree('declaracao_expressao_leitura', [p[1]] )


    def p_declaracao_5(self, p):
        'declaracao : expressao_escreva '
        p[0] = Tree('declaracao_expressao_escreva', [p[1]] )


    def p_declaracao_6(self, p):
        'declaracao : declara_var '
        p[0] = Tree('declaracao_declara_var', [p[1]] )


    def p_declaracao_7(self, p):
        'declaracao : retorna '
        p[0] = Tree('declaracao_retorna', [p[1]] )


    def p_declaracao_8(self, p):
        'declaracao : chamada_de_funcao '
        p[0] = Tree('declaracao_chamada_de_funcao', [p[1]] )

    def p_expressao_condicional_1(self, p):
        'expressao_condicional : SE expressao ENTAO sequencia_de_declaracao SENAO sequencia_de_declaracao FIM'
        p[0] = Tree('expressao_condicional_com_senao', [p[2],p[4],p[6]])
    
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
        p[0] = Tree('expressao_leitura', [], p[3])

    def p_expressao_escreva_1(self, p):
        'expressao_escreva : ESCREVE ABREPAR expressao FECHAPAR'
        p[0] = Tree('expressao_escreva', [p[3]], p[1])

    def p_declara_var1(self, p):
        'declara_var : tipo DOISPONTOS IDENTIFICADOR VIRGULA declara_outra_var'
        p[0] = Tree('declara_var_loop', [p[1], p[5]], p[3])
    
    def p_declara_var2(self, p):
        'declara_var : tipo DOISPONTOS IDENTIFICADOR'
        p[0] = Tree('declara_var_so_declara', [p[1]], p[3])

    def p_declara_outra_var_1(self, p):
        'declara_outra_var : IDENTIFICADOR VIRGULA declara_outra_var'
        p[0] = Tree('declara_outra_var_1', [p[3]], p[1])

    def p_declara_outra_var_2(self, p):
        'declara_outra_var : IDENTIFICADOR'
        p[0] = Tree('declara_outra_var_2', [], p[1])

    

    def p_retorna(self, p):
        'retorna : RETORNA ABREPAR expressao FECHAPAR'  
        p[0] = Tree('retorna', [p[3]])
    
    def p_chamada_de_funcao(self, p):
        'chamada_de_funcao :  IDENTIFICADOR ABREPAR param_chama_funcao FECHAPAR'
        p[0] = Tree('chamada_de_funcao',[p[3]], p[1])

    def p_param_chama_funcao_1(self, p):
        'param_chama_funcao :   expressao VIRGULA param_chama_funcao '
        p[0] = Tree('param_chama_funcao_loop',[p[1],p[3]])

    def p_param_chama_funcao_2(self, p):
        'param_chama_funcao :  expressao'
        p[0] = Tree('param_chama_funcao_loop_stop',[p[1]])

    def p_expressao_1(self, p):
        'expressao : expressao_simples'
        p[0] = Tree('expressao_simples_simples',[p[1]])

    def p_expressao_2(self, p):
        'expressao : expressao_simples comparacao_operador expressao_simples'
        p[0] = Tree('expressao_simples_composta',[p[1], p[2], p[3]])

    def p_comparacao_operador(self, p):
        '''
            comparacao_operador : MAIOR
                                | MAIORIGUAL
                                | MENOR
                                | MENORIGUAL
                                | IGUALDADE
        '''
        p[0] = Tree('comparacao_operador',[],p[1])


    def p_expressao_simples_1(self,p):
        'expressao_simples : expressao_simples soma termo'
        p[0] = Tree('expressao_simples_termo_com_soma',[p[1],p[2],p[3]])  

    def p_expressao_simples_2(self,p):
        'expressao_simples : termo'
        p[0] = Tree('expressao_simples_termo',[p[1]])

    def  p_soma(self,p):
        '''soma : ADICAO
                | SUBTRACAO
        '''
        p[0] = Tree('soma_termo',[],p[1])

    def p_mult(self,p):
        '''mult : MULTIPLICACAO
                | DIVISAO
        '''
        p[0] = Tree('mult_termo',[],p[1])

    def p_termo_1(self,p):
        'termo : fator'
        p[0] = Tree('fator',[p[1]])



    def p_termo_2(self,p):
        'termo : termo mult fator'
        p[0] = Tree('fator_mult', [p[1],p[2], p[3]])


    # def p_fator_1(self,p):
    #     'fator : chamada_de_funcao'
    #     p[0] = Tree('fator_chamada_de_funcao',[p[1]])
    
    def p_fator_1(self,p):
        'fator : ABREPAR expressao FECHAPAR'
        p[0] = Tree('fator_expressao',[p[2]])

    def p_fator_2(self,p):
        'fator : chamada_de_funcao'
        p[0] = Tree('fator_chamada_de_funcao',[p[1]])

    def p_fator_3(self,p):
        'fator : expressao_numero'
        p[0] = Tree('fato_expressao_numero',[p[1]])

    def p_fator_4(self,p):
        'fator : expressao_identificador'
        p[0] = Tree('fato_expressao_identificador',[p[1]])    

    def p_expressao_identificador(self, p):
        'expressao_identificador : IDENTIFICADOR'
        p[0]  = Tree('expressao_simples_identificador', [], p[1] )

    def p_expressao_numero_1(self, p):
        'expressao_numero : numero'
        p[0]  = Tree('expressao_numero', [p[1]]  )

    def p_expressao_numero_2(self, p):
        '''
            expressao_numero : ADICAO expressao_numero
                             | SUBTRACAO expressao_numero
        '''
        p[0]  = Tree('expressao_numero_composta', [p[2]], p[1] )

    def p_tipo_1(self, p):
        ''' tipo : INTEIRO
                  | FLUTUANTE'''
        p[0]  =Tree('tipo', [], p[1])

    # def p_tipo_2(self, p):
    #     'tipo : numero'
    #     p[0]  = Tree('tipo_numero', [p[1]])

    def p_numero(self,p):
        '''
        numero : INTEIRO
                | FLUTUANTE
        '''
        p[0]  =Tree('numero', [], p[1])

    def p_error(self, p):
        if p:
            print("Erro sintático: '%s', linha %d" % (p.value, p.lineno))
            exit(1)
        else:
            yacc.restart()
            print('Erro sintático: definições incompletas!')
            exit(1)

    def parser_codigo(self,codigo):
        lex = AnaliseLexica()
        self.tokens = lex.tokens
        self.precedence = (
            ('left', 'ATRIBUICAO', 'MENORIGUAL', 'MAIORIGUAL', 'MAIOR', 'MENOR', 'IGUALDADE'),
            ('left', 'ADICAO', 'SUBTRACAO'),
            ('left', 'MULTIPLICACAO', 'DIVISAO'),
            ('left', 'ABREPAR','FECHAPAR'),
        )
        parser = yacc.yacc(debug=True,module=self, optimize=False)
        return parser.parse(codigo)


if __name__ == '__main__':
    from sys import argv, exit
    f = open(argv[1])
    AnaliseSintatica(f.read())