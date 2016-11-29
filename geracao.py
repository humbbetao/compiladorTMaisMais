from parser import Tree
from parser import AnaliseSintatica
from llvmlite import ir
from semantica import *

class GeracaoDeCodigo():
	def  __init__(self, code, optz = True, debug=True):

		s =  Semantica(code.read())
		s.raiz()
		self.tree = s.tree
		self.tabela =s.tabela
		import copy
		self.s = copy.copy(s.tabela)
		self.builder = None
		self.modulo = ir.Module("Programa")
		self.escopo = "global"
		self.func = None
		self.phi = False
		self.printf_f = ir.Function(self.modulo, ir.FunctionType(ir.FloatType(), [ir.FloatType()]), 'printf_f')
		self.scanf_f = ir.Function(self.modulo, ir.FunctionType(ir.FloatType(), [ir.FloatType()]), 'scanf_f')
		# Types = ir.FloatType()
		# self.plh_print_ty = ir.FunctionType(ir.FloatType(), [ir.FloatType()])
		# self.plh_print = ir.Function(self.modulo, self.plh_print_ty, 'print_value')

		# self.read_value_ty = ir.FunctionType(ir.FloatType(), [])
		# self.read_value = ir.Function(self.modulo, self.read_value_ty, 'read_value')
		self.inicioGeracao(self.tree)
		# print("tabela de simbolos")
		# for keys,values in self.tabela.items():
		# 	print(keys,values)  
		# print("\n")
		print(self.modulo)

		arq = open("programa.ll", "w")
		arq.write(str(self.modulo))
		arq.close() 

	def inicioGeracao(self,node):
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
		tipo =""

		if(self.escopo=="global"):
			if self.tabela["global."+node.value]["tipo"] == "inteiro":
				tipo = "inteiro"
				self.tabela["global."+node.value]["tipo"] = ir.GlobalVariable(self.modulo, ir.IntType(32),name = "global."+ node.value)
			elif self.tabela["global."+node.value]["tipo"] == "flutuante":
				tipo = "flutuante"
				self.tabela["global."+node.value]["tipo"] = ir.GlobalVariable(self.modulo, ir.FloatType(), name ="global."+ node.value)
			
		else:
			if self.tabela[self.escopo+"."+node.value]["tipo"] == "inteiro":
				tipo = "inteiro"
				self.tabela[self.escopo+"."+node.value]["tipo"] =  self.builder.alloca(ir.IntType(32), name =self.escopo + "." + node.value)
			elif self.tabela[self.escopo+"."+node.value]["tipo"] == "flutuante":
				tipo = "flutuante"
				# print("passou2")
				self.tabela[self.escopo+"."+node.value]["tipo"] = self.builder.alloca(ir.FloatType(), name = self.escopo + "." + node.value)
		
		if(node.type == "declara_var_loop"):
			self.declara_outra_var(node.child[1],tipo) 
    	
	def declara_outra_var(self,node,tipo):
		if(self.escopo=="global"):
			if self.tabela["global."+node.value]["tipo"] == "inteiro":
				tipo = "inteiro"
				self.tabela["global."+node.value]["tipo"] = ir.GlobalVariable(self.modulo, ir.IntType(32), name ="global."+ node.value)
			elif self.tabela["global."+node.value]["tipo"] == "flutuante":
				tipo = "flutuante"
				self.tabela["global."+node.value]["tipo"]  = ir.GlobalVariable(self.modulo, ir.FloatType(),name ="global."+ node.value)
			
		else:
			if self.tabela[self.escopo+"."+node.value]["tipo"] == "inteiro":
				tipo = "inteiro"
				self.tabela[self.escopo+"."+node.value]["tipo"]  =  self.builder.alloca(ir.IntType(32), name =self.escopo + "." + node.value)
			elif self.tabela[self.escopo+"."+node.value]["tipo"] == "flutuante":
				tipo = "flutuante"
				self.tabela[self.escopo+"."+node.value]["tipo"] = self.builder.alloca(ir.FloatType(), name =	self.escopo + "." + node.value)
		
		if(node.type == "declara_outra_var_1"):
			self.declara_outra_var(node.child[0],tipo)    	

	def  declaracao_de_funcao(self,node):
		if(node.type == "declaracao_de_funcao_td"):
			if(node.value=="principal"):
				nome ='main'
			else: nome = node.value
			self.escopo = node.value
			tipo = node.child[0].value
			if tipo=="inteiro":
				self.func = ir.Function(self.modulo, ir.FunctionType(ir.IntType(32), ()), name=nome)
			elif tipo=="flutuante":
				self.func = ir.Function(self.modulo, ir.FunctionType(ir.FloatType(), ()), name=nome)
			bloco = self.func.append_basic_block('entry')
			self.builder = ir.IRBuilder(bloco)
			self.sequencia_de_declaracao(node.child[2])
			# self.builder.ret_void()
			self.escopo = "global"

		if(node.type == "declaracao_de_funcao_sem_corpo"):  
			if(node.value=="principal"):
				nome ='main'
			else: nome = node.value
			self.escopo = node.value
			tipo = node.child[0].value
			if tipo=="inteiro":
				self.func = ir.Function(self.modulo, ir.FunctionType(ir.IntType(32), ()), name=nome)
			elif tipo=="flutuante":
				self.func = ir.Function(self.modulo, ir.FunctionType(ir.FloatType(), ()), name=nome)
			bloco = self.func.append_basic_block('entry')
			self.builder = ir.IRBuilder(bloco)
			# self.builder.ret_void()
			self.escopo = "global"

		if(node.type == "declaracao_de_funcao_sem_corpo_sem_parametros"):
			if(node.value=="principal"):
				nome ='main'
			else: nome = node.value
			self.escopo = node.value
			tipo = node.child[0].value
			if tipo=="inteiro":
				self.func = ir.Function(self.modulo, ir.FunctionType(ir.IntType(32), ()), name=nome)
			elif tipo=="flutuante":
				self.func = ir.Function(self.modulo, ir.FunctionType(ir.FloatType(), ()), name=nome)
			bloco = self.func.append_basic_block('entry')
			self.builder = ir.IRBuilder(bloco)
			# self.builder.ret_void()
			self.escopo = "global"

		if(node.type == "declaracao_de_funcao_sem_param_com_corpo"):
			if(node.value=="principal"):
				nome ='main'
			else: nome = node.value
			self.escopo = node.value
			tipo = node.child[0].value
			if tipo=="inteiro":
				self.func = ir.Function(self.modulo, ir.FunctionType(ir.IntType(32), ()), name=nome)
			elif tipo=="flutuante":
				self.func = ir.Function(self.modulo, ir.FunctionType(ir.FloatType(), ()), name=nome)
			bloco = self.func.append_basic_block('entry')
			self.builder = ir.IRBuilder(bloco)
			self.sequencia_de_declaracao(node.child[1])
			# self.builder.ret_void()
			self.escopo = "global"

	def sequencia_de_declaracao(self,node):
		# print(node.type)
		if(node.type == "sequencia_de_declaracao_sem_loop") :
			self.declaracao(node.child[0])
		else:
			self.declaracao(node.child[0])
			self.sequencia_de_declaracao(node.child[1])

	def declaracao(self,node):
		# as ultimas
		if(node.type == "declaracao_expressao_condicional") :
			self.expressao_condicional(node.child[0])
		# as utimas
		# if(node.type == "declaracao_expressao_iteracao") :
		# 	self.expressao_iteracao(node.child[0])

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


	def float_to_int(self, num):
		return self.builder.fptosi(num, ir.IntType(32))
	
	def int_to_float(self, num):
		return self.builder.sitofp(num, ir.FloatType())

	def expressao_condicional(self,node):
		self.phi = True
		# print(node.child[0])
		condicao = self.expressao(node.child[0])
		# print(condicao, "novo")

		entao = self.func.append_basic_block("then") # bloco do então 

		if len(node.child) == 3:
			senao = self.func.append_basic_block("else") # bloco do senao
		
		fim = self.func.append_basic_block("ifcont") #fecha td
		valorEntao = None
		valorSenao = None
		if len(node.child) == 2: # se a condicao do então for verdadeira
			self.builder.cbranch(condicao, entao, fim)
			self.builder.position_at_end(entao)
			valorEntao = self.sequencia_de_declaracao(node.child[1])
			self.phi = True
			self.builder.branch(fim)
			entao = self.builder.basic_block
		else:
			self.builder.cbranch(condicao, entao, senao)		
			self.builder.position_at_end(senao)
			valorSenao = self.sequencia_de_declaracao(node.child[2])
			self.phi = True
			self.builder.branch(fim)
			senao = self.builder.basic_block

		self.builder.position_at_end(fim)

		self.phi = self.builder.phi(ir.FloatType(), "iftmp")
		self.phi.add_incoming(valorEntao, entao)
		if len(node.child) == 3:
		 	self.phi.add_incoming(valorSenao, senao)
		self.phi = False
		return self.phi

	def expressao_atribuicao(self, node):
		resultado = self.expressao(node.child[0])
		if self.escopo + "." + node.value in self.s.keys(): 
			if self.s[self.escopo + "." + node.value]["tipo"] == "inteiro":	
				self.builder.store(ir.Constant(ir.IntType(32), self.float_to_int(resultado)),name= self.tabela[self.escopo + "." + node.value]["valor"])

			elif self.s[self.escopo + "." + node.value]["tipo"] == "flutuante":											
				self.builder.store(self.tabela[self.escopo + "." + node.value]["valor"],resultado)

		else :
			if self.s["global." + node.value]["tipo"] == "inteiro":
				self.builder.store(ir.Constant(ir.IntType(32), self.float_to_int(resultado)), name =self.tabela["global." + node.value]["valor"])
				
			elif self.s["global." + node.value]["tipo"] == "flutuante":
				self.builder.store(resultado, self.tabela["global." + node.value]["valor"])

	def expressao(self,node):
		if( node.type == "expressao_simples_composta" ):
			esquerda = self.expressao_simples(node.child[0])
			# print(node.child[0])
			operacao = self.comparacao_operador(node.child[1])
			direita = self.expressao_simples(node.child[2])
			# print(esquerda, operacao, direita, "nvoo")

			if operacao == '=':
				# print(self.builder.fcmp_unordered('==', esquerda, direita, 'cmptmp'))
				return self.builder.fcmp_unordered('==', esquerda, direita, 'cmptmp')
			elif operacao == '>':
				return self.builder.fcmp_unordered('>', esquerda, direita, 'cmptmp')
			elif operacao == '>=':
				return self.builder.fcmp_unordered('>=', esquerda, direita, 'cmptmp')
			elif operacao == '<':
				return self.builder.fcmp_unordered('<', esquerda, direita, 'cmptmp')
			elif operacao == '<=':
				return self.builder.fcmp_unordered('<=', esquerda, direita, 'cmptmp')

		else :
			return self.expressao_simples(node.child[0])

	def comparacao_operador(self,node):
		# print(node.value)
		return node.value
	
	def expressao_simples(self,node):
		if(node.type == "expressao_simples_termo_com_soma"):
			# print("entrou soma")
			esquerda = self.expressao_simples(node.child[0])
			operacao = self.soma(node.child[1])
			direita = self.termo(node.child[2])

			if operacao == "+": 
				return self.builder.fadd(esquerda, direita, 'addtmp')

			elif operacao == "-":
				return self.builder.fsub(esquerda, direita, 'subtmp')

		else :
			# print(node.child[0])
			return self.termo(node.child[0])

	def termo(self,node):
		if(node.type == "fator_mult"):
			esquerda = self.termo(node.child[0])
			operacao = self.mult(node.child[1])
			direita = self.fator(node.child[2])

			if operacao == "*": 
				return self.builder.fmul(esquerda, direita, 'multmp')

			elif operacao == "/":
				# print(esquerda, "oi", direita)
				return self.builder.fdiv(esquerda, direita, 'divtmp')

		else:
			return self.fator(node.child[0])


	def fator(self, node):
		# print(node.child[0])
		if node.type == "fator_expressao":
			return self.expressao(node.child[0])
		elif node.type == "fator_chamada_de_funcao":
			return self.chamada_de_funcao(node.child[0])
		elif node.type == "fato_expressao_numero":
			return self.expressao_numero(node.child[0])
		elif node.type == "fato_expressao_identificador":
			# print(node.value, "oikiiikk")??
			return self.expressao_identificador(node.child[0])

	def expressao_numero(self, node):
		x = node.child[0].value.isdigit()
		if x is True:
			return ir.Constant(ir.IntType(32), node.child[0].value)
		else:
			return ir.Constant(ir.FloatType(), node.child[0].value)

		# return ir.Constant(ir.FloatType(), node.child[0].value)

	def expressao_identificador(self,node):
		# print(node.value)
		if self.escopo + "." + node.value in self.s.keys():
			# print(node.value, "esta aqui5")
			# print(self.escopo+"."+node.value)
			if self.s[self.escopo + "." + node.value]["tipo"] == "inteiro":
				# print(node.value, "esta aqui1")	
				return self.int_to_float(self.builder.load(self.tabela[self.escopo + "." + node.value]["valor"])) #carrega o valor
			
			elif self.s[self.escopo + "." + node.value]["tipo"] == "flutuante":
				# print(node.value, "esta aqui2")
				return self.builder.load(self.tabela[self.escopo+"."+ node.value]["valor"])

			else:
				# print(node.value, "esta aqui7")

				# print("\n",self.tabela[self.escopo+"."+ node.value]["tipo"], "nodoiekfdklej")
				# print("\n",self.s[self.escopo+"."+ node.value]["tipo"], "nodoiekfdklej")
				return self.builder.load(self.tabela[self.escopo+"."+ node.value]["tipo"])


		elif "global." + node.value in self.s.keys():
			# print(node.value, "esta aqui6")
			if self.s["global." + node.value]["tipo"] == "inteiro":
				# print(node.value, "esta aqui3")
				return self.int_to_float(self.builder.load(self.tabela["global." + node.value]["valor"])) #carrega o valor
			
			elif self.s["global." + node.value]["tipo"] == "flutuante":
				# print(node.value, "esta aqui4")
				return self.builder.load(self.tabela["global." + node.value]["valor"])


	def expressao_escreva(self, node):
		result = self.expressao(node.child[0])
		self.builder.call(self.printf_f, [result])

	def expressao_leitura(self, node):

		variavel = self.builder.call(self.scanf_f, [], "scanf_f")
		if self.escopo + "." + node.value in self.tabela.keys():
			if self.s[self.escopo + "." + node.value]["tipo"] == "inteiro":
				self.builder.store(float_to_int(variavel), self.tabela[self.escopo + "." + node.value]["valor"])

			elif self.s[self.escopo + "." + node.value]["tipo"] == "flutuante":
				self.builder.store(variavel, self.tabela[self.escopo + '.' + node.value]["valor"])
		else:
			if self.s["global." + node.value]["tipo"] == "inteiro":
				self.builder.store(float_to_int(variavel), self.tabela["global." + node.value]["valor"])
			elif self.s["global." + node.value]["tipo"] == "flutuante":
				self.builder.store(variavel, self.tabela["global." + node.value]["valor"])




	def chamada_de_funcao(self, node):
		print(node.value)
        # nomeDaFuncao  = node.value
        # valores = self.parametrizacao(node.child[1])
        # função = self.modulo.get_global(nomeDaFuncao)
        # tipos = self.tabela[node.child[1]]

        # i = 0
        # while i < len(tipos):
        #     if tipos[i] == 'inteiro':
        #         valores[i] = self.builder.fptosi(valores[i], ir.IntType(32))
        #     i = i + 1

        # # self.builder.call(self.escrevaFlutuante, [expr], name = 'call')
        # chamaFunção = self.builder.call(função, valores)
        # if self.símbolos[nó.folha[0]][1] == 'inteiro':
        #     chamaFunção = self.builder.sitofp(ir.Constant(ir.IntType(32), chamaFunção), ir.FloatType())
        # return chamaFunção


	def expressao_retorna(self, node):
		expressao = self.expressao(node.child[0])
		if self.phi:
			return expressao
		if self.tabela[self.escopo]["tipo"] == 'inteiro':
			expressao = self.builder.fptosi(expressao, ir.IntType(32))
		return self.builder.ret(expressao)







	def numero_decl(self, node):
		return ir.Constant(ir.FloatType(), node.value)

	def soma(self,node):
		return node.value

	def mult(self,node):
		return node.value
	
	def tipo(self, node) :
		return node.value

if __name__ == "__main__":
    import sys
    code = open(sys.argv[1])
    driver = GeracaoDeCodigo(code)