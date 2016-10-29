from parser import Tree
from parser import AnaliseSintatica

class Semantica():

    def __init__(self,codigo):
        self.table ={}
        self.scope = "global"
        arvore = AnaliseSintatica(codigo)
        print(arvore.ast)
        self.tree = arvore.ast


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
            print("SS")




if __name__ == "__main__":
    import sys
    code = open(sys.argv[1])
    s = Semantica(code.read())
    s.raiz()
    print("tabela de simbolos", s.table)