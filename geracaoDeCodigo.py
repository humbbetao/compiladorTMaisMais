from parser import *
from llvmlite import ir
from semantica import *

class GeracaoCodigo():


	def inicioGeracao(self, node):
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


    def declara_var(self,node):
		if(self.scope == "global"):
			if self.table["global." + node.value]["tipo"] == "inteiro":
				self.table["global." + node.value]["valor"] = ir.GlobalVariable(self.modulo, ir.IntType(32), "global." + node.value)

			elif self.table["global." + node.value]["tipo"] == "flutuante":
				self.table["global." + node.value]["valor"] = ir.GlobalVariable(self.modulo, ir.FloatType(), "global." + node.value)
		else:
			if self.table[self.scope + "." + node.value]["tipo"] == "inteiro":
				self.table[self.scope + "." + node.value]["valor"] = self.builder.alloca(ir.IntType(32), self.scope + "." + node.value)

			else:
				self.table[self.scope + "." + node.value]["valor"] = self.builder.alloca(ir.FloatType(), self.scope + "." + node.value)


        # if(node.type == "declara_var_loop"):
        #     self.tabela[self.escopo + "." + node.value] = {}
        #     self.tabela[self.escopo + "." + node.value]["variavel"] = True
        #     self.tabela[self.escopo + "." + node.value]["inicializada"] = False
        #     self.tabela[self.escopo + "." + node.value]["tipo"] = self.tipo(node.child[0])
        #     self.tabela[self.escopo + "." + node.value]["valor"] = None
            
        #     self.declara_outra_var(node.child[1], self.tipo(node.child[0]))   




if __name__ == '__main__':
	import sys
	code = open(sys.argv[1])
	driver = GeracaoCodigo(code)