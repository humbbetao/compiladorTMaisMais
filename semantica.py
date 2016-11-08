from parser import Tree
from parser import AnaliseSintatica

class Semantica():

    def __init__(self,codigo):
        self.table ={}
        self.scope = "global"
        self.tree = AnaliseSintatica().parser_codigo(codigo)
        print(self.tree)


    # def p_programa_1(self,p):
    #     'programa : statement programa'
    #     p[0] = Tree('statement_loop', [p[1], p[2]])

    # def p_programa_2(self,p):
    #     'programa : statement '
    #     p[0] = Tree('statement_sem_loop', [p[1]])

    def raiz(self):
        if(self.tree.type == "statement_loop"):
            # print("oi")
            self.statement(self.tree.child[0])
            self.programa(self.tree.child[1])
            print("oi")

        if(self.tree.type == "statement_sem_loop"):
            statement(self.tree.child[0])

    def programa(self,node):
        if(node.type == "statement_loop"):
            print("oi")
            self.statement(node.child[0])
            self.programa(node.child[1])
            print("oi")

        if(node.type == "statement_sem_loop"):
            statement(node.child[0])
            

    def statement(self,node):
        if(node.type == "statement_declaracao_de_funcao"):
            print("statementeDeclara")
            self.declaracao_de_funcao(node.child[0])
        if(node.type == "statement_declara_var"):
            print("declara_var")
            self.declara_var(node.child[0])


    def  declaracao_de_funcao(self,node):
        if(node.value in self.table.keys()): #se ja tem funcao com esse nome na tabela
            print("Erro Semântico, o nome "+  node.value + " já esta sendo utilizado")
            exit(1)


        

        # if (self.tipo(node.child[0])==1):

        if(node.type == "declaracao_de_funcao"):
            print("delcarafunc")
            tipo = None
            if self.tipo(node.child[0]) == 1:
                tipo ="INTEIRO"
            if self.tipo(node.chil[0]) == 2:
                tipo = "FLUTUANTE"
            
            self.table[node.value] = {}
            self.table[node.value]["var"] = False
            self.table[node.value]["tipo"] = tipo
            self.table[node.value]["num_parametros"] = 0

            self.sequencia_de_declaracao(node.child[2])
            self.scope = node.value  #escopo nome da função
            self.table[node.value]["num_parametros"] = self.declaracao_param(node.child[1]) #recebe a quantidade de parametros declarados

            self.scope = "global"



        if(node.type == "declaracao_de_funcao_sem_corpo"):

            tipo = None
            if self.tipo(node.child[0]) == 1:
                tipo ="INTEIRO"
            if self.tipo(node.chil[0]) == 2:
                tipo = "FLUTUANTE"
            
            self.table[node.value] = {}
            self.table[node.value]["var"] = False
            self.table[node.value]["tipo"] = tipo
            self.table[node.value]["num_parametros"] = 0

            # self.sequencia_de_declaracao(node.child[2])
            self.scope = node.value  #escopo nome da função
            self.table[node.value]["num_parametros"] = self.declaracao_param(node.child[1]) #recebe a quantidade de parametros declarados

            self.scope = "global"

        if(self.tree.type == "declaracao_de_funcao_sem_corpo_sem_parametros"):
            print("delcarafunc")
            tipo = None
            if self.tipo(node.child[0]) == 1:
                tipo ="INTEIRO"
            if self.tipo(node.chil[0]) == 2:
                tipo = "FLUTUANTE"
            
            self.table[node.value] = {}
            self.table[node.value]["var"] = False
            self.table[node.value]["tipo"] = tipo
            self.table[node.value]["num_parametros"] = 0

            self.sequencia_de_declaracao(node.child[2])
            self.scope = node.value  #escopo nome da função
            # self.table[node.value]["num_parametros"] = self.declaracao_param(node.child[1]) #recebe a quantidade de parametros declarados

            self.scope = "global"
        if(node.type == "declaracao_de_funcao_sem_param_com_corpo"):
            print("delcarafunc")
            tipo = None
            if self.tipo(node.child[0]) == 1:
                tipo ="INTEIRO"
            if self.tipo(node.chil[0]) == 2:
                tipo = "FLUTUANTE"
            
            self.table[node.value] = {}
            self.table[node.value]["var"] = False
            self.table[node.value]["tipo"] = tipo
            self.table[node.value]["num_parametros"] = 0

            # self.sequencia_de_declaracao(node.child[2])
            self.scope = node.value  #escopo nome da função
            # self.table[node.value]["num_parametros"] = self.declaracao_param(node.child[1]) #recebe a quantidade de parametros declarados

            self.scope = "global"

    #     def p_declara_var1(self, p):
    #     'declara_var : tipo DOISPONTOS IDENTIFICADOR'
    #     p[0] = Tree('declara_var_so_declara', [p[1]], p[3])

    # def p_declara_var2(self, p):
    #     'declara_var : tipo DOISPONTOS IDENTIFICADOR VIRGULA declara_outra_var'
    #     p[0] = Tree('declara_var_loop', [p[1], p[5]], p[3])

    # def p_declara_var3(self, p):
    #     'declara_var : tipo  DOISPONTOS IDENTIFICADOR'
    #     p[0] = Tree('declara_var_com_atribuicao', [p[1]], p[3])

    def declara_var(self,node):

        if(self.scope + "." + node.value in self.table.keys()): #se ja tem variavel com esse nome na tabela
            print("Erro Semântico, nome já utilizado : " + node.value )
            exit(1)

        if(node.type == "declara_var_so_declara"):
            if self.tipo(node.child[0]) == 1:
            tipo = "INTEIRO"

        elif self.tipo(node.child[0]) == 2:
            tipo = "FLUTUANTE"

        elif self.tipo(node.child[0]) == 3:
            print("Erro Semântico, o parametro não pode ser do tipo VAZIO: " + node.value )
            exit(1)

        self.table[self.scope + "." + node.value] = {}
        self.table[self.scope + "." + node.value]["var"] = True
        self.table[self.scope + "." + node.value]["inicializada"] = False
        self.table[self.scope + "." + node.value]["tipo"] = tipo
        self.table[self.scope + "." + node.value]["valor"] = None

        if(node.type == "declara_var_loop"):
        # if(node.type == "declara_var_so_declara"):
            if self.tipo(node.child[0]) == 1:
                tipo = "INTEIRO"

            elif self.tipo(node.child[0]) == 2:
                tipo = "FLUTUANTE"

            elif self.tipo(node.child[0]) == 3:
                print("Erro Semântico, o parametro não pode ser do tipo VAZIO: " + node.value )
                exit(1)

        self.table[self.scope + "." + node.value] = {}
        self.table[self.scope + "." + node.value]["var"] = True
        self.table[self.scope + "." + node.value]["inicializada"] = False
        self.table[self.scope + "." + node.value]["tipo"] = tipo
        self.table[self.scope + "." + node.value]["valor"] = None
        
        self.declara_var(node.child[1])
        
        self.scope = node.value  




    # def p_declaracao_param_1(self, p):
    #     'declaracao_param : declaracao_param VIRGULA tipo DOISPONTOS IDENTIFICADOR'
    #     p[0] = Tree('declaracao_param_loop', [p[1],p[3]], p[5])

    # def p_declaracao_param_2(self, p): 
    #     'declaracao_param : tipo DOISPONTOS IDENTIFICADOR'
    #     p[0] = Tree('declaracao_param', [p[1]], p[3])

    def declaracao_param(self,node):
        if(node.type == "declaracao_param_loop"):
            if( self.scope + "." + node.value in self.table.keys()): #se ja tem variavel com esse nome na tabela
                print("Erro Semântico, nome já utilizado :" + node.value )
                exit(1)

            tipo = ""

            if self.tipo(node.child[1]) == 1:
                tipo = "INTEIRO"

            elif self.tipo(node.child[1]) == 2:
                tipo = "FLUTUANTE"

            elif self.tipo(node.child[1]) == 3:
                print("Erro Semântico, o parametro não pode ser do tipo VAZIO: " + node.value )
                exit(1)

            self.table[self.scope + "." + node.value] = {}
            self.table[self.scope + "." + node.value]["var"] = True
            self.table[self.scope + "." + node.value]["inicializada"] = True
            self.table[self.scope + "." + node.value]["tipo"] = tipo
            self.table[self.scope + "." + node.value]["valor"] = None

            return self.declaracao_param(node.child[0]) + 1

        else: #se for só um parametro

            if( (self.scope + "." + node.value) in self.table.keys()): #se ja tem variavel com esse nome na tabela
                print("Erro Semântico, nome já utilizado : " + node.value )
                exit(1)

            elif self.tipo(node.child[0]) == 1:
                tipo = "INTEIRO"

            elif self.tipo(node.child[0]) == 2:
                tipo = "FLUTUANTE"

            elif self.tipo(node.child[0]) == 3:
                print("Erro Semântico, o parametro não pode ser do tipo VAZIO: " + node.value )
                exit(1)

            self.table[self.scope + "." + node.value] = {}
            self.table[self.scope + "." + node.value]["var"] = True
            self.table[self.scope + "." + node.value]["inicializada"] = True
            self.table[self.scope + "." + node.value]["tipo"] = tipo
            self.table[self.scope + "." + node.value]["valor"] = None

            return 1



    # def p_sequencia_de_declaracao_1(self, p):
    #     'sequencia_de_declaracao : declaracao'
    #     p[0] = Tree('sequencia_de_declaracao_sem_loop', [p[1]])

    # def p_sequencia_de_declaracao_2 (self, p):
    #     'sequencia_de_declaracao : declaracao sequencia_de_declaracao'
    #     p[0] = Tree('sequencia_de_declaracao_loop',[p[1], p[2]])

    def sequencia_de_declaracao(self,node):
        if(node.type == "sequencia_de_declaracao_sem_loop") :
            self.declaracao(node.child[0])
        else :
            self. declaracao(node.child[0])
            self.sequencia_de_declaracao(node.child[1])

  # declaracao : expressao_condicional 
  #                      | expressao_iteracao
  #                      | expressao_atribuicao
  #                      | expressao_leitura
  #                      | expressao_escreva
  #                      | declara_var
  #                      | retorna
  #                      | chamada_de_funcao

    def declaracao(self,node):
        if(node.type == "declaracao_expressao_condicional") :
            self.expressao_condicional(node.child[0])

        if(node.type == "declaracao_expressao_iteracao") :
            self.expressao_iteracao(node.child[0])

        if(node.type == "declaracao_expressao_atribuicao") :
            self.expressao_atribuicao(node.child[0])

        if(node.type == "declaracao_expressao_leitura") :
            self.expressao_leitura(node.child[0])

        if(node.type == "declaracao_expressao_escreva") :
            self.expressao_escreva(node.child[0])

        if(node.type == "declaracao_declara_var") :
            self.declara_var(node.child[0])

        if(node.type == "declaracao_retorna") :
            self.retorna(node.child[0])

        if(node.type == "declaracao_chamada_de_funcao") :
            self.chamada_de_funcao(node.child[0])


    # def p_expressao_condicional_1(self, p):
    #     'expressao_condicional : SE expressao ENTAO sequencia_de_declaracao SENAO sequencia_de_declaracao FIM'
    #     p[0] = Tree('expressao_condicional', [p[2],p[4],p[6]])
    
    # def p_expressao_condicional_2(self, p):
    #     'expressao_condicional : SE expressao ENTAO sequencia_de_declaracao FIM'
    #     p[0] = Tree('expressao_condicional', [p[2],p[4]])

    def expressao_condicional(self,node):
        if(node.type=="expressao_condicional_com_senao"):
            self.expressao(node.child[0], "nada")
            self.sequencia_de_declaracao(node.child[1])
            self.sequencia_de_declaracao(node.child[2])
        else:
            self.expressao(node.child[0], "nada")
            self.sequencia_de_declaracao(node.child[1])

# def p_expressao_iteracao(self, p):
#         'expressao_iteracao : REPITA sequencia_de_declaracao ATE expressao'
#         p[0] =  Tree('expressao_iteracao', [p[2], p[4]])

    def repita_decl(self, node):
        self.sequencia_de_declaracao(node.child[0])
        self.expressao(node.child[1], "nada")

  # 'expressao_atribuicao : IDENTIFICADOR ATRIBUICAO expressao'
        # p[0] =  Tree('expressao_atribuicao', [p[3]], p[1])
    def expressao_atribuicao(self, p):
        if self.scope + "." + node.value not in self.table.keys() and "global." + node.value not in self.table.keys():
            print("Erro Semântico. Variável " + node.value + " não encontrada")
            exit(1)

        else :
            if self.scope + "." + node.value in self.table.keys():
                self.table[self.scope + "." + node.value]["inicializada"] = True 
                self.expressao(node.child[0], node.value) #passa o nome da variável

            elif "global." + node.value in self.table.keys():
                self.table["global." + node.value]["inicializada"] = True
                self.expressao(node.child[0], node.value) #passa o nome da variável
      
    # def p_expressao_leitura(self, p):
    #     'expressao_leitura : LEIA ABREPAR IDENTIFICADOR FECHAPAR'
    #     p[0] = Tree('expressao_leitura', [], p[1])

    def expressao_leitura(self,node):
          if self.scope + "." + node.value not in self.table.keys() and "global." + node.value not in self.table.keys():
            print("Erro Semântico. Variável " + node.value + " não encontrada")
            exit(1)


    # def p_expressao_escreva_1(self, p):
    #     'expressao_escreva : ESCREVE ABREPAR expressao FECHAPAR'
    #     p[0] = Tree('expressao_escreva', [p[3]], p[1])

    def expressao_escreva(self,node):
        # if(node.type == "escreva_decl_exp"):
            self.expressao(node.child[0], "nada")
        # else :
        #     self.chamada_func_escreva(node.child[1])

# def p_retorna(self, p):
#         'retorna : RETORNA ABREPAR expressao FECHAPAR'  
#         p[0] = Tree('retorna', [p[3]])

    def expressao_retorna(self,node):
         # if (node.type == ""):

        tipo = self.expressao(node.child[0])
        # else:
        #     return node.value #retorna o id

 # def p_chamada_de_funcao(self, p):
 #        'chamada_de_funcao :  IDENTIFICADOR ABREPAR param_chama_funcao FECHAPAR'
 #        p[0] = Tree('chamada_de_funcao',[p[3]], p[1])

    def chamada_de_funcao(self,node):
        if(node.value not in self.table.keys()) :
            print("Erro Semântico, nome de funcao não declarado : " + node.value )
            exit(1)

        if self.param_chama_funcao(node.child[0]) != self.table[node.value]["num_parametros"]:
            print("Erro Semântico, número de parametros não correspondem com os da função : " + node.value )
            exit(1)

    def param_chama_funcao(self,node):
         if node.type == "parametro_chama_func_paramentros":
            if self.scope + "." + node.value not in self.table.keys() and "global" + "." + node.value not in self.table.keys():
                print("Erro semântico : Variável não declarada  " + node.value)
                exit(1)

            elif self.scope + "." + node.value in self.table.keys():
                if self.table[self.scope + "." + node.value]["inicializada"] == False:
                    print("Erro semântico : Variável não inicializada " + node.value)
                    exit(1)

                else:
                    return self.param_chama_funcao(node.child[0]) + 1

            elif "global" + "." + node.value in self.table.keys():
                if self.table["global" + "." + node.value]["inicializada"] == False:
                    print("Erro semântico : Variável não inicializada " + node.value)
                    exit(1)

                else:
                    return self.param_chama_funcao(node.child[0]) + 1

        # elif node.type == "parametro_chama_func_numeros":
        #     self.numero_decl(node.child[0])
        #     self.param_chama_funcao(node.child[0]) + 1

        # elif node.type == "parametro_chama_func_num":
        #     self.numero_decl(node.child[0])
        #     return 1

        # elif node.type == "param_chama_funcao":
        #     if self.scope + "." + node.value not in self.table.keys() and "global." + node.value not in self.table.keys():
        #         print("Erro semântico : Variável não declarada " + node.value)
        #         exit(1)

        #     elif self.scope + "." + node.value in self.table.keys():
        #         if self.table[self.scope + "." + node.value]["inicializada"] == False:
        #             print("Erro semântico : Variável não inicializada " + node.value)
        #             exit(1)
        #         else:
        #             return 1

        #     elif "global" + "." + node.value in self.table.keys():
        #         if self.table["global" + "." + node.value]["inicializada"] == False:
        #             print("Erro semântico : Variável não inicializada " + node.value)
        #             exit(1)
        #         else:
        #             return 1

    # def p_expressao_1(self, p):
    #     'expressao : expressao_simples'
    #     p[0] = Tree('expressao_simples',[p[1]])

    # def p_expressao_2(self, p):
    #     'expressao : expressao_simples comparacao_operador expressao_simples'
    #     p[0] = Tree('chamada_de_funcao',[p[1], p[2], p[3]])

    def expressao(self,node,nomeVariavel):
          if( node.type == "expressao_simples_composta" ):
            self.expressao_simples(node.child[0], nomeVariavel)
            self.comparacao_operador(node.child[1])
            self.expressao_simples(node.child[2], nomeVariavel)

        else :
            self.expressao_simples(node.child[0], nomeVariavel)

 # def p_comparacao_operador(self, p):
 #        '''
 #            comparacao_operador : MAIOR
 #                                | MAIORIGUAL
 #                                | MENOR
 #                                | MENORIGUAL
 #                                | IGUALDADE
 #        '''
 #        p[0] = Tree('comparacao_operador',[],p[1])

    def comparacao_operador(self, node):
            return node.value

    # def p_expressao_simples_1(self,p):
    #     'expressao_simples : expressao_simples soma termo'
    #     p[0] = Tree('expressao_simples_termo_com_soma',[p[1],p[2],p[3]])  

    # def p_expressao_simples_2(self,p):
    #     'expressao_simples : termo'
    #     p[0] = Tree('expressao_simples_termo',[p[1]])
    def simples_exp(self, node, nomeVariavel) :
        if(node.type == "expressao_simples_termo_com_soma"):
            self.expressao_simples(node.child[0], nomeVariavel)
            self.soma(node.child[1])
            self.termo(node.child[2], nomeVariavel)

        else :
            self.termo(node.child[0], nomeVariavel)

 #     def  p_soma(self,p):
 #        '''soma : ADICAO
 #                | SUBTRACAO
 #        '''
 #        p[0] = Tree('soma_termo',[],p[1])

    def soma(self,node):
        return node.value


# def p_mult(self,p):
 #        '''mult : MULTIPLICACAO
 #                | DIVISAO
 #        '''
 #        p[0] = Tree('mult_termo',[],p[1])

    def mult(self,node):
        return node.value


 # def p_termo_1(self,p):
 #        'termo : fator'
 #        p[0] = Tree('fator',[p[1]])

    def termo(self,node):
        if(node.type == "fator"):
            self.fator(node.child[0])
        else:
            self.termo(node.child[0])
            self.mult(node.child[1])
            self.fator(node.child[2])

 #    def p_termo_2(self,p):
 #        'termo : termo mult fator'
 #        p[0] = Tree('fator_mult', [p[1],p[2], p[3]])


    
    # def p_fator_1(self,p):
    #     'fator : ABREPAR expressao FECHAPAR'
    #     p[0] = Tree('fator_expressao',[p[2]])

    # def p_fator_3(self,p):
    #     'fator : chamada_de_funcao'
    #     p[0] = Tree('fator_chamada_de_funcao',[p[1]])
    def fator(self,node):
        if(node.type == "fator_expressao"):
            self.expressao(node.child[0])
        if(node.type == "fator_chamada_de_funcao"):
            self.chamada_de_funcao(node.child[0])
        else:
            self.expressao_numero(node.child[0])
            self.expressao_identificador(node.child[1])


    # def p_fator_2(self,p):
    #     '''
    #         fator : expressao_numero
    #               | expressao_identificador
    #     '''
    #     p[0] = Tree('fator_expressao_generica',[p[1]])

    # def p_expressao_identificador(self, p):
    #     'expressao_identificador : IDENTIFICADOR'
    #     p[0]  = Tree('expressao_simples_identificador', [], p[1] )

    def expressao_identificador(self,node):
        return node.value

    def expressao_numero(self,node):
        if(node.type=="expressao_numero_composta"):
             self.expressao_numero(node.child[0])
        else:
            self.numero(node.child[0])

        node.value

    # def p_expressao_numero_1(self, p):
    #     'expressao_numero : numero'
    #     p[0]  = Tree('expressao_numero', [p[1]]  )

    # def p_expressao_numero_2(self, p):
    #     '''
    #         expressao_numero : ADICAO expressao_numero
    #                          | SUBTRACAO expressao_numero
    #     '''
    #     p[0]  = Tree('expressao_numero', [p[2]] )

    # def p_tipo_1(self, p):
    #     ''' tipo : INTEIRO
    #               | FLUTUANTE'''
    #     p[0]  =Tree('tipo', [], p[1])

    # # def p_tipo_2(self, p):
    # #     'tipo : numero'
    # #     p[0]  = Tree('tipo_numero', [p[1]])

    # def p_numero(self,p):
    #     '''
    #     numero : INTEIRO
    #             | FLUTUANTE
    #     '''
    #     p[0]  =Tree('numero', [], p[1])


    def tipo(self, node) :
        if(node.value == "INTEIRO"):
            return 1

        if(node.value == "FLUTUANTE"):
            return 2

    def numero(self, node) :
        if(node.value == "INTEIRO"):
            return 1

        if(node.value == "FLUTUANTE"):
            return 2

if __name__ == "__main__":
    import sys
    code = open(sys.argv[1])
    s = Semantica(code.read())
    s.raiz()
    print("tabela de simbolos", s.table)