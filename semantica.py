from parser import Tree
from parser import AnaliseSintatica

class Semantica():

    def __init__(self,codigo):
        self.tabela ={}
        self.escopo = "global"
        self.ast = AnaliseSintatica()
        self.code = self.ast.parser_codigo(codigo)
        self.tree = self.code

    def raiz(self):
        if(self.tree.type == "statement_loop"):
            self.statement(self.tree.child[0])
            self.programa(self.tree.child[1])

        if(self.tree.type == "statement_sem_loop"):
            self.statement(self.tree.child[0])

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


        # print(node.type)

        if(node.type == "declaracao_de_funcao_td"):
                
            self.tabela[node.value] = {}
            self.tabela[node.value]["variavel"] = False
            self.tabela[node.value]["tipo"] = self.tipo(node.child[0])
            self.tabela[node.value]["num_parametros"] = 0

            self.escopo = node.value
            self.tabela[node.value]["num_parametros"] = self.declaracao_param(node.child[1]) #recebe a quantidade de parametros declarados
            # self.tabela[node.value]["parametros"] =[]
            self.tabela[node.value]["parametros"] = self.param(node.child[1],[])
            # print(self.param(node.child[1],[]),"oi")
            self.sequencia_de_declaracao(node.child[2])
            self.escopo = "global"



        if(node.type == "declaracao_de_funcao_sem_corpo"):  
            self.tabela[node.value] = {}
            self.tabela[node.value]["variavel"] = False
            self.tabela[node.value]["tipo"] = self.tipo(node.child[0])
            self.tabela[node.value]["num_parametros"] = 0

            self.escopo = node.value  #escopo nome da função
            self.tabela[node.value]["num_parametros"] = self.declaracao_param(node.child[1]) #recebe a quantidade de parametros declarados
            # self.tabela[node.value]["parametros"] =[]
            self.tabela[node.value]["parametros"] = self.param(node.child[1],[])
            # print(self.param(node.child[1],[]),"oi")
            self.escopo = "global"


        if(node.type == "declaracao_de_funcao_sem_corpo_sem_parametros"):
            
            self.tabela[node.value] = {}
            self.tabela[node.value]["variavel"] = False
            self.tabela[node.value]["tipo"] = self.tipo(node.child[0])
            self.tabela[node.value]["num_parametros"] = 0
            self.tabela[node.value]["parametros"] =[]

            self.escopo = node.value  #escopo nome da função
            self.escopo = "global"

        if(node.type == "declaracao_de_funcao_sem_param_com_corpo"):
    
            self.tabela[node.value] = {}
            self.tabela[node.value]["variavel"] = False
            self.tabela[node.value]["tipo"] = self.tipo(node.child[0])
            self.tabela[node.value]["num_parametros"] = 0
            self.tabela[node.value]["parametros"] =[]
            self.escopo = node.value
            self.sequencia_de_declaracao(node.child[1])

            self.escopo = "global"

    def declara_var(self,node):

        if(self.escopo + "." + node.value in self.tabela.keys()): #se ja tem variavel com esse nome na tabela
            print("Erro Semântico, nome já utilizado : " + node.value )
            exit(1)
        if(node.value in self.tabela.keys()): #se ja tem variavel com esse nome na tabela
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
            
            self.declara_outra_var(node.child[1], self.tipo(node.child[0]))          

    def declara_outra_var(self,node,tipo):
        if(self.escopo + "." + node.value in self.tabela.keys()): #se ja tem variavel com esse nome na tabela
            print("Erro Semântico, nome já utilizado : " + node.value )
            exit(1)
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

    def declaracao_param(self,node):
        if( self.escopo + "." + node.value in self.tabela.keys()): #se ja tem variavel com esse nome na tabela
            print("Erro Semântico, nome já utilizado :" + node.value )
            exit(1)

        if(node.type == "declaracao_param_loop"):
            # print(node.value, "kkkkkkkkkkkk")
            self.tabela[self.escopo + "." + node.value] = {}
            self.tabela[self.escopo + "." + node.value]["variavel"] = True
            self.tabela[self.escopo + "." + node.value]["inicializada"] = True
            self.tabela[self.escopo + "." + node.value]["tipo"] = self.tipo(node.child[0])
            self.tabela[self.escopo + "." + node.value]["valor"] = None

            return self.declaracao_param(node.child[1]) + 1

        else: 
            # print(node.value, "kkkkkkkkkkkk")
            self.tabela[self.escopo + "." + node.value] = {}
            self.tabela[self.escopo + "." + node.value]["variavel"] = True
            self.tabela[self.escopo + "." + node.value]["inicializada"] = True
            self.tabela[self.escopo + "." + node.value]["tipo"] = self.tipo(node.child[0])
            self.tabela[self.escopo + "." + node.value]["valor"] = None

            return 1

    def param(self,node,lista):
        if(node.type == "declaracao_param_loop"):
            lista.append(self.tipo(node.child[0]))
            print(lista)
            return self.param(node.child[1],lista)
        else:   
            lista.append(self.tipo(node.child[0]))
            return lista

    def sequencia_de_declaracao(self,node):
        if(node.type == "sequencia_de_declaracao_sem_loop") :
            self.declaracao(node.child[0])
        else :
            self.sequencia_de_declaracao(node.child[0])
            self.declaracao(node.child[1])

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


    def expressao_condicional(self,node):
        if(node.type=="expressao_condicional_com_senao"):
            self.expressao(node.child[0],None)
            self.sequencia_de_declaracao(node.child[1])
            self.sequencia_de_declaracao(node.child[2])
        else:
            self.expressao(node.child[0],None)
            self.sequencia_de_declaracao(node.child[1])

    def expressao_iteracao(self, node):
        self.sequencia_de_declaracao(node.child[0])
        self.expressao(node.child[1],None)

    def expressao_atribuicao(self, node):
        if (self.escopo + "." + node.value not in self.tabela.keys() and "global." + node.value not in self.tabela.keys() ):
            print("Erro Semântico. Variável " + node.value + " não encontrada")
            exit(1)

        else:
            if self.escopo + "." + node.value in self.tabela.keys():
                tipo = self.expressao(node.child[0],node.value)
                self.tabela[self.escopo+"." + node.value]["inicializada"] = True
                if self.tabela[self.escopo + '.' + node.value]["tipo"] != tipo and tipo!=None:
                    print("WARNING atribuição: variavel " + node.value + " é do tipo " + self.tabela[self.escopo + '.' + node.value]["tipo"] +  " está atribuindo uma expressão do tipo "+ tipo )              
            elif "global." + node.value in self.tabela.keys():
                tipo = self.expressao(node.child[0],node.value)
                self.tabela["global." + node.value]["inicializada"] = True
                self.expressao(node.child[0], node.value)                 
                if self.tabela['global.' + node.value]["tipo"] != tipo:
                    print("WARNING atribuição: variavel " + node.value + " é do tipo " + self.tabela['global.' + node.value]["tipo"] +  " está atribuindo uma expressão do tipo "+ tipo )
                
                

    def expressao_leitura(self,node):
        if self.escopo + "." + node.value not in self.tabela.keys() and "global." + node.value not in self.tabela.keys():
            print("Erro Semântico. Variável " + node.value + " não encontrada")
            exit(1)

        elif self.escopo + '.' + node.value in self.tabela.keys():
            self.tabela[self.escopo + '.' + node.value]["inicializada"] = True
        elif "global."+ node.value in self.tabela.keys():
            self.tabela["global." + node.value]["inicializada"] = True

    def expressao_escreva(self,node):
        self.expressao(node.child[0], None)

    def expressao_retorna(self,node):       
        novo = self.expressao(node.child[0], None)
        if(self.escopo+"."+novo in self.tabela.keys() ):
            tipo  = self.tabela[self.escopo+"."+novo]["tipo"] 
            if(tipo != self.tabela[self.escopo]["tipo"]):
                print("Erro Semantico. Retorno de funcao "+self.escopo+" o certo eh "+self.tabela[self.escopo]["tipo"])
                exit(1)

    def chamada_de_funcao(self,node):

        if(node.value not in self.tabela.keys()) :
            print("Erro Semântico, nome de funcao não declarado : " + node.value )
            exit(1)
        
        if self.param_chama_funcao(node.child[0],0, node.value) != self.tabela[node.value]["num_parametros"]:
            print("Erro Semântico, número de parametros não correspondem com os da função : " + node.value )
            exit(1)

        self.param_chama_funcao(node.child[0],0, node.value)

# 1,5 + 2 + 1,5 + 2 + 1 + 2
    def param_chama_funcao(self,node,level, nome):
        if node.type == "param_chama_funcao_loop":
            if(self.tabela[nome]["num_parametros"] >= 1):
                if(self.tabela[nome]["parametros"][level]!=self.expressao(node.child[0],None) and  self.expressao(node.child[0],None)!=None):
                    print("Erro Semantico: tipo de parametros incompativel") 
                    exit(1)

            level = level+1

            self.expressao(node.child[0],None)
            return self.param_chama_funcao(node.child[1],level) + 1
        else:
            self.expressao(node.child[0],None)
            if(self.tabela[nome]["num_parametros"] >=1 ):
                if(self.tabela[nome]["parametros"][level]!=self.expressao(node.child[0],None)):
                    print("Erro Semantico: tipo de parametro incompativel") 
                    exit(1)      
                level = level+1
            # verificar aqui os parametros
            return 1


    def expressao(self,node,nomeVariavel):

        if( node.type == "expressao_simples_composta" ):
            esquerda = self.expressao_simples(node.child[0],nomeVariavel)
            self.comparacao_operador(node.child[1])
            direita = self.expressao_simples(node.child[2],nomeVariavel)
            
            if esquerda == "flutuante" or direita == "flutuante":
                return "flutuante"
            else: 
                return "inteiro"       
        else:          
            return self.expressao_simples(node.child[0],nomeVariavel)

    def comparacao_operador(self, node):
            return node.value

    def expressao_simples(self, node,nomeVariavel) :
        if(node.type == "expressao_simples_termo_com_soma"):
            esquerda =self.expressao_simples(node.child[0],nomeVariavel)
            self.soma(node.child[1])
            direita =self.termo(node.child[2],nomeVariavel)
            
            if esquerda == "flutuante" or direita == "flutuante":
                return "flutuante"
            else: 
                return "inteiro"
        else :
            return self.termo(node.child[0], nomeVariavel)

    def soma(self,node):
        return node.value

    def mult(self,node):
        return node.value

    def termo(self,node,nomeVariavel):
        if(node.type == "fator_mult"):
            esquerda = self.termo(node.child[0],nomeVariavel)
            direita = self.fator(node.child[2],nomeVariavel)
           
            if self.mult(node.child[1]) == "/":
                if self.escopo + "." + nomeVariavel in self.tabela.keys():
                    if self.tabela[self.escopo+"."+nomeVariavel]["tipo"]!= "flutuante":
                        print("Warning: tipo incorreto ")
                    return "flutuante"
                      
            if esquerda == "flutuante" or direita == "flutuante":
                return "flutuante"
            else: 
                return "inteiro"
        else:
            return self.fator(node.child[0],nomeVariavel)
 
    def fator(self,node, nomeVariavel):
        if(node.type == "fator_expressao"):
            return self.expressao(node.child[0],nomeVariavel)
        elif(node.type == "fator_chamada_de_funcao"):
            return self.chamada_de_funcao(node.child[0])
        elif(node.type == "fato_expressao_numero"):
            return self.expressao_numero(node.child[0], nomeVariavel,False)

            if(nomeVariavel!=None):
                if self.escopo + "." + node.expressao_numero(node.child[0],nomeVariavel) not in self.tabela.keys() and "global." + node.expressao_numero(node.child[0],nomeVariavel)  not in self.tabela.keys():
                   print("Erro semântico : Variável não declarada : " + node.value)
                   exit(1)

        elif(node.type == "fato_expressao_identificador"):
            return self.expressao_identificador(node.child[0])


    def expressao_identificador(self,node):
        tipo=""
        if self.escopo+"."+node.value in  self.tabela.keys() :
            tipo = self.tabela[self.escopo+"."+node.value]["tipo"]
            if self.tabela[self.escopo+"."+node.value]["inicializada"] == False:
                print("Erro: Variavel " +self.escopo+"."+node.value + " nao foi inicializada" )
                exit(1)
            self.tabela[self.escopo+"."+node.value]["inicializada"]=True
        elif "global."+node.value in  self.tabela.keys() :
            tipo = self.tabela["global."+node.value]["tipo"]
            if self.tabela["global."+node.value]["inicializada"] == False:
                print("Erro: Variavel " +"global."+node.value + " nao foi inicializada" )
                exit(1)
            self.tabela["global."+node.value]["inicializada"]=True
       
        return tipo
       

    def expressao_numero(self,node,nomeVariavel,boole):
        if(node.type=="expressao_numero_composta"):
            if(node.value=="+"):
                return self.expressao_numero(node.child[0],nomeVariavel,False)
            else: 
                return self.expressao_numero(node.child[0],nomeVariavel,True) 
                
        if(node.type=="expressao_numero"):
            # print(node.child[0].value, "nnndiedkejk")
            return self.numero(node.child[0],boole)
    
    def tipo(self, node) :
        return node.value

    def numero(self, node,boole):
        # print(node.value, "kkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkk")
        x = node.value.isdigit()
        if x is True:
            return "inteiro"
        else:
            return "flutuante"   

if __name__ == "__main__":
    import sys
    code = open(sys.argv[1])
    s = Semantica(code.read())
    s.raiz()
    print("tabela de simbolos")
    for keys,values in s.tabela.items():
        if(values["variavel"]==True and values["inicializada"]==False):
            print("Warning: Variavel " +  keys + " nao esta sendo utilizada\n" )
        print(keys,values)  