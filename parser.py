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
            ('left', 'ATRIBUICAO', 'MENORIGUAL', 'MAIORIGUAL', 'MAIOR', 'MENOR', 'IGUALDADE'),
            ('left', 'ADICAO', 'SUBTRACAO'),
            ('left', 'MULTIPLICACAO', 'DIVISAO'),
            ('left', 'ABREPAR', 'FECHAPAR')
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
        'principal : PRINCIPAL ABREPAR declaracao_param FECHAPAR  sequencia_de_declaracao FIM'
        p[0] = Tree('principal_com_param', [p[3], p[5]], p[1])

    def p_principal_2(self, p):
        'principal : PRINCIPAL ABREPAR  FECHAPAR sequencia_de_declaracao FIM'
        p[0] = Tree('principal_sem_param', [p[4]], p[1] )

    def p_func_loop_1(self, p):
        'func_loop : declaracao_de_funcao func_loop'
        p[0] = Tree('func_loop', [p[1], p[2]])

    def p_func_loop_2(self, p):
        'func_loop : declaracao_de_funcao'
        p[0] = Tree('declaracao_de_funcao_sem_loop',[p[1]])

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
        'sequencia_de_declaracao : declaracao'
        p[0] = Tree('sequencia_de_declaracao_sem_loop', [p[1]])

    def p_sequencia_de_declaracao_2 (self, p):
        'sequencia_de_declaracao : declaracao sequencia_de_declaracao'
        p[0] = Tree('sequencia_de_declaracao_loop',[p[1], p[2]])

    def p_declaracao_2(self, p):
        '''
            declaracao : expressao_condicional
                    | expressao_iteracao
                    | expressao_atribuicao
                    | expressao_leitura
                    | expressao_escreva
                    | declara_var
                    | retorna
                    | chamada_de_funcao
        '''
        p[0] = Tree('declaracao', [p[1]] )


    def p_declara_var1(self, p):
        'declara_var : tipo DOISPONTOS IDENTIFICADOR VIRGULA declara_outra_var'
        p[0] = Tree('declara_var', [p[1], p[5]], p[3])

    def p_declara_var2(self, p):
        'declara_var : tipo  DOISPONTOS IDENTIFICADOR ATRIBUICAO expressao_simples'
        p[0] = Tree('declara_var', [p[1], p[5]], p[3])

    # def p_declara_var3(self, p):
    #     'declara_var : tipo IDENTIFICADOR ATRIBUICAO expressao_simples'
    #     p[0] = Tree('declara_var', [p[1], p[4]], p[2])
    
    def p_declara_outra_var(self, p):
        'declara_outra_var : IDENTIFICADOR'
        p[0] = Tree('declara_outra_var', [], p[1])

    # def p_declara_var4(self, p):
    #     'declara_var :  IDENTIFICADOR ATRIBUICAO INTEIRO'
    #     p[0] = Tree('declaracao_var', [p[1]], p[3])

    def p_retorna(self, p):
        'retorna : RETORNA ABREPAR expressao FECHAPAR'
    
        p[0] = Tree('retorna', [p[3]])

    def p_expressao_condicional_1(self, p):
        'expressao_condicional : SE expressao ENTAO sequencia_de_declaracao FIM'
        p[0] = Tree('expressao_condicional', [p[2],p[4]])
   
    def p_expressao_condicional_2(self, p):
        'expressao_condicional : SE expressao ENTAO sequencia_de_declaracao SENAO sequencia_de_declaracao FIM'
        p[0] = Tree('expressao_condicional', [p[2],p[4],p[6]])


    def p_expressao_iteracao(self, p):
        'expressao_iteracao : REPITA sequencia_de_declaracao ATE expressao'
        p[0] =  Tree('expressao_iteracao', [p[2], p[4]])

    def p_expressao_atribuicao(self, p):
        'expressao_atribuicao : IDENTIFICADOR ATRIBUICAO expressao'
        p[0] =  Tree('expressao_atribuicao', [p[3]], p[1])

    def p_expressao_leitura(self, p):
        'expressao_leitura : LEIA ABREPAR IDENTIFICADOR FECHAPAR'
        p[0] = Tree('expressao_leitura', [], p[1])

    def p_expressao_escreva_1(self, p):
        'expressao_escreva : ESCREVE ABREPAR expressao FECHAPAR'
        p[0] = Tree('expressao_escreva', [p[3]], p[1])

    def p_expressao_1(self, p):
        'expressao : ABREPAR expressao FECHAPAR'
        p[0]  = Tree('chamada_de_parenteses', [p[2]])

    # def p_expressao_2(self, p):
    #     'expressao : expressao_simples operador_aritmetico expressao'
    #     p[0] =  Tree('expressao_com_aritmetica', [p[1],p[2], p[3]])

    def p_expressao_2(self, p):
        'expressao : expressao operador_aritmetico expressao'
        p[0] =  Tree('expressao_com_aritmetica', [p[1],p[2], p[3]])

    def p_expressao_3(self, p):
        'expressao : expressao operador_logico expressao'
        p[0] =  Tree('expressao_expressao_condicional', [p[1],p[2], p[3]])


    def p_expressao_4(self, p):
        'expressao : expressao_simples'
        p[0]  = Tree('expressao_simples_unica', [p[1]] )

    def p_expressao_5(self, p):
        'expressao : chamada_de_funcao'
        p[0]  = Tree('expressao_chamada_de_funcao', [p[1]])




    

    # def p_operador_logico_2(self, p):
    #     'operador_logico : MAIORIGUAL'
    #     p[0]  = Tree('operador_logico',[], p[1])

    # def p_operador_logico_3(self, p):
    #     'operador_logico : MENOR'
    #     p[0]  = Tree('operador_logico',[], p[1])

    # def p_operador_logico_4(self, p):
    #     'operador_logico : MENORIGUAL'
    #     p[0]  = Tree('operador_logico',[], p[1])
    
    # def p_operador_logico_5(self, p):
    #     'operador_logico : IGUALDADE'
    #     p[0]  = Tree('operador_logico',[], p[1])


    # def p_expressao_com_expressao_aritmetica_1(self, p):
    #     'expressao_simples : fator operador_aritmetico expressao_simples'
    #     p[0]  = Tree('expressao_simples', [p[1], p[2], p[3]])

    def  p_expressao_com_expressao_aritmetica(self, p):
        'expressao_simples : fator'
        p[0]  = Tree('expressao_simples_so_fator',[p[1]]) 



    # def p_fator_1(p):
    #     'simples_exp : termo'
    #     p[0] = Tree('simples_exp', [p[1]])

    # def p_simples_exp_2(p):
    #     'simples_exp : simples_exp soma_sub termo'
    #     p[0] = Tree('simples_exp_somasub', [p[1], p[2], p[3]])

    # def p_soma_sub_1(p):
    #     'soma_sub : SOMA'
    #     p[0] = Tree('soma_sub_soma', [], p[1])

    # def p_soma_sub_2(p):
    #     'soma_sub : SUB'
    #     p[0] = Tree('soma_sub_subtracao', [], p[1])

    # def p_termo_1(p):
    #     'termo : fator'
    #     p[0] = Tree('termo_fator', [p[1]])

    # def p_termo_2(p):
    #     'termo : termo mult_div fator'
    #     p[0] = Tree('termo_multdiv', [p[1], p[2], p[3]])

    # def p_mult_div_1(p):
    #     'mult_div : MULT'
    #     p[0] = Tree('mult_div_multiplicacao', [], p[1])

    # def p_mult_div_2(p):
    #     'mult_div : DIVISAO'
    #     p[0] = Tree('mult_div_divisao', [], p[1])

    # def p_fator_1(p):
    #     'fator : ID'
    #     p[0] = Tree('fator_id', [], p[1])

    # def p_fator_2(p):
    #     'fator : numero_decl'
    #     p[0] = Tree('fator_numero', [p[1]])

    # def p_fator_3(p):
    #     'fator : ABRE_PAR exp_decl FECHA_PAR'
    #     p[0] = Tree('fator_exp', [p[2]])

    # def  p_expressao_com_expressao_aritmetica_3(self, p):
    #     'expressao_simpexpressao_simples_les : fator'
    #     p[0]  = Tree('expressao_simples_so_fator_com_parenteses',[p[2]]) 

    # def  p_expressao_com_expressao_aritmetica_4(self, p):
   # expressao_simples_ #     'expressao_simples : ABREPAR fator operador_aritmetico expressao_simples FECHAPAR'
    #     p[0]  = Tree('expressao_simples_com_parenteses',[p[2], p[3], p[4]]) 

    # def  p_expressao_com_expressao_aritmetica_5(self, p):
    #     'expressao_simples : fator operador_aritmetico ABREPAR expressao_simples FECHAPAR'
    #     p[0]  = Tree('expressao_simples_com_parenteses',[p[1], p[2], p[4]]) 

    # def  p_expressao_com_expressao_aritmetica_6(self, p):
    #     'expressao_simples : ABREPAR fator FECHAPAR operador_aritmetico  expressao_simples '
    #     p[0]  = Tree('expressao_simples_com_parenteses',[p[2], p[4], p[5]]) 

    # def p_operador_add(self, p):
    #     '''
    #     operador_add : ADICAO
    #                  | SUBTRACAO
    #     '''
    #     p[0]  = Tree('operador_add',[], p[1])

    # def p_operador_add_2(self, p):
    #     'operador_add : SUBTRACAO'
    #     p[0]  = Tree('operador_add',[], p[1])

    # def p_termo_1(self, p):
    #     'termo : termo operador_mult fator'
    #     p[0]  = Tree('termo', [p[1], p[2], p[3]])

    # def p_termo_2(self, p):
    #     'termo : fator'
    #     p[0]  =Tree('termo', [p[1]])    

    # def p_operador_mult(self, p):
    #     '''
    #     operador_mult : MULTIPLICACAO
    #                   | DIVISAO
    #     '''
    #     p[0] = Tree('operador_mult',[] ,p[1])

    # def p_operador_mult_2(self, p):  
    #     'operador_mult : DIVISAO'
    #     p[0] = Tree('operador_mult',[], p[1])

    # def p_fator_1(self, p):
    #     'fator : NUMERO'
    #     p[0] = Tree('fator', [p[1]])


    def p_operador_logico(self, p):
        '''
        operador_logico : MAIOR
                        | MAIORIGUAL
                        | MENOR
                        | MENORIGUAL
                        | IGUALDADE
        '''
        p[0]  = Tree('operador_logico', [], p[1])

    def p_operador_aritmetico(self, p):
        '''
        operador_aritmetico : SUBTRACAO
                            | ADICAO
                            | MULTIPLICACAO
                            | DIVISAO                        
        '''
        p[0]  = Tree('operador_aritmetico', [], p[1])


    def p_fator_1(self, p):
        '''
        fator : IDENTIFICADOR
        '''
        p[0] = Tree('termo_identificador', [], p[1])

    def p_fator_2(self, p):
        '''
        fator : INTEIRO
              | FLUTUANTE
        '''
        p[0] = Tree('termo_numero', [], p[1])




    # def p_fator_3(self, p):
    #     'fator : FLUTUANTE'
    #     p[0] = Tree('fator', [p[1]])


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
        'tipo : numero'
        p[0]  = Tree('tipo', [], p[1])

    def p_numero(self,p):
        '''
        numero : INTEIRO
                | FLUTUANTE
        '''
        p[0]  =Tree('numero', [], p[1])

    # def p_tipo_3(self, p):
    #     'tipo : FLUTUANTE'
    #     p[0]  = Tree('tipo_flutuante', [], p[1])

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