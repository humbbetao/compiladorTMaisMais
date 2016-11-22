from parser import Tree
from parser import AnaliseSintatica

class Semantica():

    def __init__(self,codigo):
        self.tabela ={}
        self.escopo = "global"
        self.tree = AnaliseSintatica().parser_codigo(codigo)

    def raiz(self):
        if(self.tree.type == "statement_loop"):
            self.statement(self.tree.child[0])
            self.programa(self.tree.child[1])

        if(self.tree.type == "statement_sem_loop"):
            statement(self.tree.child[0])

    def programa(self,node):
        if(node.type == "statement_loop"):
            self.statement(node.child[0])
            self.programa(node.child[1])
        if(node.type == "statement_sem_loop"):
            self.statement(node.child[0])          

    def statement(self,node):
        if(node.type == "statement_declaracao_de_funcao"):
            self.declaracao_de_funcao(node.child[0])

        if(node.type == "statement_declara_var"):
            self.declara_var(node.child[0])


    def  declaracao_de_funcao(self,node):
        if(node.value in self.tabela.keys()): #se ja tem funcao com esse nome na tabela
            print("Erro Semântico, o nome "+  node.value + " já esta sendo utilizado")
            exit(1)        

        print(node.type)
        if(node.type == "declaracao_de_funcao_td"):
            
            self.tabela[node.value] = {}
            self.tabela[node.value]["variavel"] = False
            self.tabela[node.value]["tipo"] = self.tipo(node.child[0])
            self.tabela[node.value]["num_parametros"] = 0

            self.escopo = node.value
            self.tabela[node.value]["num_parametros"] = self.declaracao_param(node.child[1]) #recebe a quantidade de parametros declarados
            self.sequencia_de_declaracao(node.child[2])
            self.escopo = "global"



        if(node.type == "declaracao_de_funcao_sem_corpo"):  
            self.tabela[node.value] = {}
            self.tabela[node.value]["variavel"] = False
            self.tabela[node.value]["tipo"] = self.tipo(node.child[0])
            self.tabela[node.value]["num_parametros"] = 0
            self.escopo = node.value  #escopo nome da função
            self.tabela[node.value]["num_parametros"] = self.declaracao_param(node.child[1]) #recebe a quantidade de parametros declarados
            self.escopo = "global"

        if(self.tree.type == "declaracao_de_funcao_sem_corpo_sem_parametros"):
            
            self.tabela[node.value] = {}
            self.tabela[node.value]["variavel"] = False
            self.tabela[node.value]["tipo"] = self.tipo(node.child[0])
            self.tabela[node.value]["num_parametros"] = 0

            self.escopo = node.value  #escopo nome da função
            self.escopo = "global"

        if(node.type == "declaracao_de_funcao_sem_param_com_corpo"):
    
            self.tabela[node.value] = {}
            self.tabela[node.value]["variavel"] = False
            self.tabela[node.value]["tipo"] = self.tipo(node.child[0])
            self.tabela[node.value]["num_parametros"] = 0

            self.escopo = node.value
            self.sequencia_de_declaracao(node.child[1])

            self.escopo = "global"

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

        if(self.escopo + "." + node.value in self.tabela.keys()): #se ja tem variavel com esse nome na tabela
            print("Erro Semântico, nome já utilizado : " + node.value )
            exit(1)

        if(node.type == "declara_var_so_declara"):
            self.tabela[self.escopo + "." + node.value] = {}
            self.tabela[self.escopo + "." + node.value]["variavel"] = True
            self.tabela[self.escopo + "." + node.value]["inicializada"] = False
            self.tabela[self.escopo + "." + node.value]["tipo"] = self.tipo(node.child[0])
            self.tabela[self.escopo + "." + node.value]["valor"] = None

        if(node.type == "declara_var_loop"):
            self.tabela[self.escopo + "." + node.value] = {}
            self.tabela[self.escopo + "." + node.value]["variavel"] = True
            self.tabela[self.escopo + "." + node.value]["inicializada"] = False
            self.tabela[self.escopo + "." + node.value]["tipo"] = self.tipo(node.child[0])
            self.tabela[self.escopo + "." + node.value]["valor"] = None
            
            # print(node.child[0])
            self.declara_outra_var(node.child[1], self.tipo(node.child[0]))          
            # self.escopo = node.value  


    def declara_outra_var(self,node,tipo):
        if(self.escopo + "." + node.value in self.tabela.keys()): #se ja tem variavel com esse nome na tabela
            print("Erro Semântico, nome já utilizado : " + node.value )
            exit(1)

        # print(node.value)
        if(node.type == "declara_outra_var_1"):
            self.tabela[self.escopo + "." + node.value] = {}
            self.tabela[self.escopo + "." + node.value]["variavel"] = True
            self.tabela[self.escopo + "." + node.value]["inicializada"] = False
            self.tabela[self.escopo + "." + node.value]["tipo"] = tipo
            self.tabela[self.escopo + "." + node.value]["valor"] = None
            self.declara_outra_var(node.child[0],tipo)  

        if(node.type == "declara_outra_var_2"):
            self.tabela[self.escopo + "." + node.value] = {}
            self.tabela[self.escopo + "." + node.value]["variavel"] = True
            self.tabela[self.escopo + "." + node.value]["inicializada"] = False
            self.tabela[self.escopo + "." + node.value]["tipo"] = tipo
            self.tabela[self.escopo + "." + node.value]["valor"] = None

  




    # def p_declaracao_param_1(self, p):
    #     'declaracao_param : declaracao_param VIRGULA tipo DOISPONTOS IDENTIFICADOR'
    #     p[0] = Tree('declaracao_param_loop', [p[1],p[3]], p[5])

    # def p_declaracao_param_2(self, p): 
    #     'declaracao_param : tipo DOISPONTOS IDENTIFICADOR'
    #     p[0] = Tree('declaracao_param', [p[1]], p[3])

    def declaracao_param(self,node):
        if( self.escopo + "." + node.value in self.tabela.keys()): #se ja tem variavel com esse nome na tabela
            print("Erro Semântico, nome já utilizado :" + node.value )
            exit(1)

        if(node.type == "declaracao_param_loop"):
            # print(node.value)
            self.tabela[self.escopo + "." + node.value] = {}
            self.tabela[self.escopo + "." + node.value]["variavel"] = True
            self.tabela[self.escopo + "." + node.value]["inicializada"] = True
            self.tabela[self.escopo + "." + node.value]["tipo"] = self.tipo(node.child[0])
            self.tabela[self.escopo + "." + node.value]["valor"] = None

            return self.declaracao_param(node.child[1]) + 1

        else: #se for só um parametro
            # print(node.value)
            self.tabela[self.escopo + "." + node.value] = {}
            self.tabela[self.escopo + "." + node.value]["variavel"] = True
            self.tabela[self.escopo + "." + node.value]["inicializada"] = True
            self.tabela[self.escopo + "." + node.value]["tipo"] = self.tipo(node.child[0])
            self.tabela[self.escopo + "." + node.value]["valor"] = None

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
            self.expressao_retorna(node.child[0])

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
            self.expressao(node.child[0],"nada")
            self.sequencia_de_declaracao(node.child[1])
            self.sequencia_de_declaracao(node.child[2])
        else:
            self.expressao(node.child[0])
            self.sequencia_de_declaracao(node.child[1])

# def p_expressao_iteracao(self, p):
#         'expressao_iteracao : REPITA sequencia_de_declaracao ATE expressao'
#         p[0] =  Tree('expressao_iteracao', [p[2], p[4]])

    def expressao_iteracao(self, node):
        self.sequencia_de_declaracao(node.child[0])
        self.expressao(node.child[1],"nada")

  # 'expressao_atribuicao : IDENTIFICADOR ATRIBUICAO expressao'
        # p[0] =  Tree('expressao_atribuicao', [p[3]], p[1])
    def expressao_atribuicao(self, node):
        if (self.escopo + "." + node.value not in self.tabela.keys()
             and "global." + node.value not in self.tabela.keys() ):
            print("Erro Semântico. Variável " + node.value + " não encontrada")
            exit(1)

        else :
            tipo = self.expressao(node.child[0],"nada")
            print(tipo)
            if self.escopo + "." + node.value in self.tabela.keys():
                # print("aqui2")
                self.tabela[self.escopo + "." + node.value]["inicializada"] = True 
                self.expressao(node.child[0], node.value) #passa o nome da variável

                # print(tipo)
                # if self.tabela[self.escopo + '.' + node.value]["tipo"] != :
                #     print("WARNING atribuição: variavel '" + node.value + "' é do tipo '" + self.tabela[self.escopo + '.' + node.value]["tipo"] +  "' está atribuindo uma expressão do tipo '" + tipo + "'")
            elif "global." + node.value in self.tabela.keys():
                self.tabela["global." + node.value]["inicializada"] = True
                self.expressao(node.child[0], node.value) 
                # 'global.' + subarvore.value in self.tabela.keys():
                # if self.tabela["global." + subarvore.value][1] != tipo:
                #     print("WARNING atribuição: identificador '" + node.value + "' é do tipo '" +
                #     self.tabela["global." + node.value][1] +
                #     "' está atribuindo uma expressão do tipo '" + tipo + "'")



                # = self.expressao(node.child[0], node.value) #passa o nome da variável

            # elif "global." + node.value in self.tabela.keys():
            #     self.tabela["global." + node.value]["valor"] = True
            #     self.tabela[self.escopo + "." + node.value]["valor"]=self.expressao(node.child[0], node.value) #passa o nome da variável
      
    # def p_expressao_leitura(self, p):
    #     'expressao_leitura : LEIA ABREPAR IDENTIFICADOR FECHAPAR'
    #     p[0] = Tree('expressao_leitura', [], p[1])

    def expressao_leitura(self,node):
        if self.escopo + "." + node.value not in self.tabela.keys() and "global." + node.value not in self.tabela.keys():
            print("Erro Semântico. Variável " + node.value + " não encontrada")
            exit(1)
        elif self.escopo + '.' + node.value in self.tabela.keys():
            self.tabela[self.escopo + '.' + node.value]["inicializada"] = True
        else:
            self.tabela['global.' + node.value]["inicializada"] = True


    # def p_expressao_escreva_1(self, p):
    #     'expressao_escreva : ESCREVE ABREPAR expressao FECHAPAR'
    #     p[0] = Tree('expressao_escreva', [p[3]], p[1])

    def expressao_escreva(self,node):
        self.expressao(node.child[0], "nada")
        # else :
        #     self.chamada_func_escreva(node.child[1])

# def p_retorna(self, p):
#         'retorna : RETORNA ABREPAR expressao FECHAPAR'  
#         p[0] = Tree('retorna', [p[3]])

    def expressao_retorna(self,node):       
        self.expressao(node.child[0], "nada")

        # else:
        #     return node.value #retorna o id

 # def p_chamada_de_funcao(self, p):
 #        'chamada_de_funcao :  IDENTIFICADOR ABREPAR param_chama_funcao FECHAPAR'
 #        p[0] = Tree('chamada_de_funcao',[p[3]], p[1])

    def chamada_de_funcao(self,node):

        if(node.value not in self.tabela.keys()) :
            print("Erro Semântico, nome de funcao não declarado : " + node.value )
            exit(1)

        if self.param_chama_funcao(node.child[0]) != self.tabela[node.value]["num_parametros"]:
            print("Erro Semântico, número de parametros não correspondem com os da função : " + node.value )
            exit(1)

    def param_chama_funcao(self,node):
        if node.type == "param_chama_funcao_loop":
            a = self.expressao(node.child[0],"nada")
            return self.param_chama_funcao(node.child[1]) + 1
        else:
            return 1
            a = self.expressao(node.child[0],"nada") 
         # node.type == "param_chama_funcao_loop_stop":
        

            # if self.escopo + "." + node.value not in self.tabela.keys() and "global" + "." + node.value not in self.tabela.keys():
            #     print("Erro semântico : Variável não declarada  " + node.value)
            #     exit(1)

            # elif self.escopo + "." + node.value in self.tabela.keys():
            #     if self.tabela[self.escopo + "." + node.value]["inicializada"] == False:
            #         print("Erro semântico : Variável não inicializada " + node.value)
            #         exit(1)

            #     else:
            #         return self.param_chama_funcao(node.child[0]) + 1

            # elif "global" + "." + node.value in self.tabela.keys():
            #     if self.tabela["global" + "." + node.value]["inicializada"] == False:
            #         print("Erro semântico : Variável não inicializada " + node.value)
            #         exit(1)

            #     else:
            #         return self.param_chama_funcao(node.child[0]) + 1

        # elif node.type == "parametro_chama_func_numeros":
        #     self.numero_decl(node.child[0])
        #     self.param_chama_funcao(node.child[0]) + 1

        # elif node.type == "parametro_chama_func_num":
        #     self.numero_decl(node.child[0])
        #     return 1

        # elif node.type == "param_chama_funcao":
        #     if self.escopo + "." + node.value not in self.tabela.keys() and "global." + node.value not in self.tabela.keys():
        #         print("Erro semântico : Variável não declarada " + node.value)
        #         exit(1)

        #     elif self.escopo + "." + node.value in self.tabela.keys():
        #         if self.tabela[self.escopo + "." + node.value]["inicializada"] == False:
        #             print("Erro semântico : Variável não inicializada " + node.value)
        #             exit(1)
        #         else:
        #             return 1

        #     elif "global" + "." + node.value in self.tabela.keys():
        #         if self.tabela["global" + "." + node.value]["inicializada"] == False:
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
            esquerda = self.expressao_simples(node.child[0],nomeVariavel)
            self.comparacao_operador(node.child[1])
            direita = self.expressao_simples(node.child[2],nomeVariavel)
            if esquerda ==direita:
                return "inteiro"

        else:          
            return self.expressao_simples(node.child[0],nomeVariavel)

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
    def expressao_simples(self, node,nomeVariavel) :
        if(node.type == "expressao_simples_termo_com_soma"):
            esquerda =self.expressao_simples(node.child[0],nomeVariavel)
            self.soma(node.child[1])
            direita =self.termo(node.child[2],nomeVariavel)

            if esquerda == direita:
                return esquerda
            # else:
            #     return "flutuante"

        else :
            return self.termo(node.child[0], nomeVariavel)

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

    def termo(self,node,nomeVariavel):
        # print(node.child[0])
        if(node.type == "fator"):
           return self.fator(node.child[0],nomeVariavel)
        else:
            esquerda = self.termo(node.child[0],nomeVariavel)
           
            # if self.mult(node.child[1]) =="/":
            #     if self.escopo + "." + nomeVariavel in self.tabela.keys() :
            #         if self.tabela[self.escopo+"."+nomeVariavel]["tipo"]!= "flutuante":
            #             print("Warning de cast")
            direita = self.fator(node.child[2],nomeVariavel)
            # print(self.mult(node.child[1]))
            if self.mult(node.child[1]) == "/":
                if self.escopo + "." + nomeVariavel in self.tabela.keys():
                     if self.tabela[self.escopo+"."+nomeVariavel]["tipo"]!= "flutuante":
                        print("Warning de cast")

            if esquerda == direita:
                return esquerda

            # else:
            #     "flutuante"

 #    def p_termo_2(self,p):
 #        'termo : termo mult fator'
 #        p[0] = Tree('fator_mult', [p[1],p[2], p[3]])


    
    # def p_fator_1(self,p):
    #     'fator : ABREPAR expressao FECHAPAR'
    #     p[0] = Tree('fator_expressao',[p[2]])

    # def p_fator_3(self,p):
    #     'fator : chamada_de_funcao'
    #     p[0] = Tree('fator_chamada_de_funcao',[p[1]])
    def fator(self,node, nomeVariavel):
        if(node.type == "fator_expressao"):
            return self.expressao(node.child[0],nomeVariavel)
        if(node.type == "fator_chamada_de_funcao"):
            return self.chamada_de_funcao(node.child[0])
        if(node.type == "fato_expressao_numero"):
            print(self.expressao_numero(node.child[0], nomeVariavel,False))
            return self.expressao_numero(node.child[0], nomeVariavel,False)

            # if(nomeVariavel!="nada"):
            #     if self.escopo + "." + node.expressao_numero(node.child[0],nomeVariavel) not in self.tabela.keys() and "global." + node.expressao_numero(node.child[0],nomeVariavel)  not in self.tabela.keys():
            #        print("Erro semântico : Variável não declarada : " + node.value)
            #        exit(1)
                # else:
                #     if self.escopo + "." + node.value in self.tabela.keys() :
                #         if self.escopo + "." + nomeVariavel in self.tabela.keys():
                #             if self.tabela[escopo + "." + node.value]["inicializada"] == True # ja recebendo numa variavel inicializada
                #                 if self.tabela[self.escopo + "." + nomeVariavel]["tipo"] == "INTEIRO" and self.tabela[self.escopo + "." + node.value]["tipo"] == "FLUTUANTE": #inteiro e float
                #                     print("Warning : Voce está associando um tipo FLUTUANTE a um tipo INTEIRO : " + nomeVariavel)

                #                 elif self.tabela[self.escopo + "." + nomeVariavel]["tipo"] == "FLUTUANTE" and self.tabela[self.escopo + "." + node.value]["tipo"] == "INTEIRO": #float e inteiro
                #                     print("Warning : Voce está associando um tipo INTEIRO a um tipo FLUTUANTE : " + nomeVariavel)
                #             else:
                #                 print("Erro semântico : Variável não inicializada : " + node.value)
                #                 exit(1)

                #     elif "global." + node.value in self.tabela.keys() :
                #          if "global." + nomeVariavel in self.tabela.keys():
                #             if self.tabela["global." + node.value]["inicializada"] == True # ja recebendo numa variavel inicializada
                #                 if self.tabela["global." + nomeVariavel]["tipo"] == "INTEIRO" and self.tabela["global." + node.value]["tipo"] == "FLUTUANTE": #inteiro e float
                #                     print("Warning : Voce está associando um tipo FLUTUANTE a um tipo INTEIRO : " + nomeVariavel)

                #                 elif self.tabela["global." + nomeVariavel]["tipo"] == "FLUTUANTE" and self.tabela["global." + node.value]["tipo"] == "INTEIRO": #float e inteiro
                #                     print("Warning : Voce está associando um tipo INTEIRO a um tipo FLUTUANTE : " + nomeVariavel)
                #             else:
                #                 print("Erro semântico : Variável não inicializada : " + node.value)
                #                 exit(1)

                #         if self.escopo + "." + nomeVariavel in self.tabela.keys():

                #             if self.tabela["global." + node.value]["inicializada"] == True: #recebenco ID inicializado 
                #                 if self.tabela[self.escopo + "." + nomeVariavel]["tipo"] == "INTEIRO" and self.tabela["global." + node.value]["tipo"] == "FLUTUANTE": #inteiro e float
                #                     print("Warning : Voce está associando um tipo FLUTUANTE a um tipo INTEIRO : " + nomeVariavel)

                #                 elif self.tabela[self.escopo + "." + nomeVariavel]["tipo"] == "FLUTUANTE" and self.tabela["global." + node.value]["tipo"] == "INTEIRO": #float e inteiro
                #                     print("Warning : Voce está associando um tipo INTEIRO a um tipo FLUTUANTE : " + nomeVariavel)
                            
                #             else:
                #                 print("Erro semântico : Variável não inicializada : " + node.value)
                #                 exit(1)

                #      elif "global." + nomeVariavel in self.tabela.keys():
                            
                #             if self.tabela["global." + node.value]["inicializada"] == True: #recebenco ID inicializado 
                                
                #                 if self.tabela["global." + nomeVariavel]["tipo"] == "INTEIRO" and self.tabela["global." + node.value]["tipo"] == "FLUTUANTE": #inteiro e float
                #                     print("Warning : Voce está associando um tipo FLUTUANTE a um tipo INTEIRO : " + nomeVariavel)

                #                 elif self.tabela["global." + nomeVariavel]["tipo"] == "FLUTUANTE" and self.tabela["global." + node.value]["tipo"] == "INTEIRO": #float e inteiro
                #                     print("Warning : Voce está associando um tipo INTEIRO a um tipo FLUTUANTE : " + nomeVariavel)
                            
                #             else:
                #                 print("Erro semântico : Variável não inicializada : " + node.value)
                #                 exit(1)
                    




        if(node.type == "fato_expressao_identificador"):
            # print(self.expressao_identificador(node.child[0],nomeVariavel))
            return self.expressao_identificador(node.child[0],nomeVariavel)


    # def p_fator_2(self,p):
    #     '''
    #         fator : expressao_numero
    #               | expressao_identificador
    #     '''
    #     p[0] = Tree('fator_expressao_generica',[p[1]])

    # def p_expressao_identificador(self, p):
    #     'expressao_identificador : IDENTIFICADOR'
    #     p[0]  = Tree('expressao_simples_identificador', [], p[1] )

    def expressao_identificador(self,node,nomeVariavel):
        return node.value

    def expressao_numero(self,node,nomeVariavel,boole):
        if(node.type=="expressao_numero_composta"):
            # print(node.value)
            if(node.value=="+"):
                return self.expressao_numero(node.child[0],nomeVariavel,False)
            else: 
                return self.expressao_numero(node.child[0],nomeVariavel,True) 
                
        if(node.type=="expressao_numero"):
            # print(self.numero(node.child[0],boole),"oi")
            return self.numero(node.child[0],boole)

        # node.value

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
        return node.value

    def numero(self, node,boole):
        x = node.value.isdigit()
        if x is True:
            return "inteiro"
        else:
            return "flutuante"   
        # valor =0
        # if boole == True:
        #     valor = valor - float(node.value)
        # print(valor)
        # return valor 
        # if(node.value =:
        #     return 1



        # if(node.value == "FLUTUANTE"):
        #     return 2

if __name__ == "__main__":
    import sys
    code = open(sys.argv[1])
    s = Semantica(code.read())
    s.raiz()
    # print("tabela de simbolos", s.tabela)
    for keys,values in s.tabela.items():
        print(keys,values)
        # print(values)