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
            print("oi")
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
    
    # def declara_var(self,node):

    # def declaracao_de_funcao(self,node):

    # def declaracao_de_funcao(self,node):

    # def declaracao_de_funcao(self,node):

    # def declaracao_de_funcao(self,node):



    # def programa(self):
    def tipo(self, node) :
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