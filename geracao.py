from parser import Tree
from parser import AnaliseSintatica
from llvmlite import ir
from semantica import *
from subprocess import call
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
		self.escrevaFlutuante = ir.Function(self.modulo, ir.FunctionType(ir.FloatType(), [ir.FloatType()]), 'escrevaFlutuante')
		self.escrevaInteiro = ir.Function(self.modulo, ir.FunctionType(ir.IntType(32), [ir.IntType(32)]), 'escrevaInteiro')
		self.leiaFlutuante = ir.Function(self.modulo, ir.FunctionType(ir.FloatType(), []), 'leiaFlutuante')
		self.leiaInteiro = ir.Function(self.modulo, ir.FunctionType(ir.IntType(32), []), 'leiaInteiro')
		self.inicioGeracao(self.tree)
		print(self.modulo)

		arq = open("programa.ll", "w")
		arq.write(str(self.modulo))
		arq.close() 
		call("llc programa.ll --mtriple \"x86_64-unknown-linux-gnu\"", shell=True)
		call("gcc -c programa.s", shell=True)
		call("gcc -o saida programa.o print_scanf.o", shell=True)
		call("./saida", shell=True)

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
			# print("chamou")
			return self.declara_var(node.child[0])
	
	def declara_var(self,node):
		tipo =""
		# print(node.)
		if(self.escopo=="global"):
			if self.tabela["global."+node.value]["tipo"] == "inteiro":
				tipo = "inteiro"
				self.tabela["global."+node.value]["valor"] = ir.GlobalVariable(self.modulo, ir.IntType(32),name="global."+ node.value)
				# self.tabela["global."+node.value]["valor"] 
			elif self.tabela["global."+node.value]["tipo"] == "flutuante":
				tipo = "flutuante"
				self.tabela["global."+node.value]["valor"] = ir.GlobalVariable(self.modulo, ir.FloatType(),name="global."+ node.value)
				# self.tabela["global."+node.value]["valor"] 
		else:
			if self.tabela[self.escopo+"."+node.value]["tipo"] == "inteiro":
				tipo = "inteiro"
				self.tabela[self.escopo+"."+node.value]["valor"] =  self.builder.alloca(ir.IntType(32), name =self.escopo + "." + node.value)
				# self.tabela[self.escopo+"."+node.value]["valor"] 
			elif self.tabela[self.escopo+"."+node.value]["tipo"] == "flutuante":
				tipo = "flutuante"
				# print("passou2")
				self.tabela[self.escopo+"."+node.value]["valor"] = self.builder.alloca(ir.FloatType(), name = self.escopo + "." + node.value)
				# self.tabela[self.escopo+"."+node.value]["valor"] 
		
		if(node.type == "declara_var_loop"):
			self.declara_outra_var(node.child[1],tipo) 
    	
	def declara_outra_var(self,node,tipo):
		if(self.escopo=="global"):
			if self.tabela["global."+node.value]["tipo"] == "inteiro":
				tipo = "inteiro"
				self.tabela["global."+node.value]["valor"] = ir.GlobalVariable(self.modulo, ir.IntType(32),name= "global."+ node.value)
			elif self.tabela["global."+node.value]["tipo"] == "flutuante":
				tipo = "flutuante"	
				self.tabela["global."+node.value]["valor"]  = ir.GlobalVariable(self.modulo, ir.FloatType(),name="global."+ node.value)	
		else:

			if self.tabela[self.escopo+"."+node.value]["tipo"] == "inteiro":
				tipo = "inteiro"
				self.tabela[self.escopo+"."+node.value]["valor"]  =  self.builder.alloca(ir.IntType(32), name =self.escopo + "." + node.value)
			elif self.tabela[self.escopo+"."+node.value]["tipo"] == "flutuante":
				tipo = "flutuante"
				self.tabela[self.escopo+"."+node.value]["valor"] = self.builder.alloca(ir.FloatType(), name =	self.escopo + "." + node.value)
		if(node.type == "declara_outra_var_1"):
			return self.declara_outra_var(node.child[0],tipo)   
  	

	def  declaracao_de_funcao(self,node):
		if(node.type == "declaracao_de_funcao_td"):
			if(node.value=="principal"):
				nome ='main'
			else: nome = node.value
			self.escopo = node.value
			tipo = node.child[0].value

			parametragem = self.declaracao_param(node.child[1])

			if tipo=="inteiro":
				self.func = ir.Function(self.modulo, ir.FunctionType(ir.IntType(32), ( [parametragem[i][0] for i in range(0, len(parametragem))])), name=nome)
			elif tipo=="flutuante":
				self.func = ir.Function(self.modulo, ir.FunctionType(ir.FloatType(), ( [parametragem[i][0] for i in range(0, len(parametragem))])), name=nome)
			bloco = self.func.append_basic_block('entry')
			self.builder = ir.IRBuilder(bloco)

			for i, param in enumerate(parametragem):
				self.func.args[i].name = param[1]
				self.tabela[self.escopo + '.' + param[1]]["valor"] = self.builder.alloca(param[0], name = param[1])
				self.builder.store(self.func.args[i], self.tabela[self.escopo + '.' + param[1]]["valor"])
				self.builder.load(self.tabela[self.escopo + "." + param[1]]["valor"])
			self.sequencia_de_declaracao(node.child[2])
			self.escopo = "global"
		
		if(node.type == "declaracao_de_funcao_sem_corpo"):  
			if(node.value=="principal"):
				nome ='main'
			else: nome = node.value
			self.escopo = node.value
			tipo = node.child[0].value
			parametragem = self.declaracao_param(node.child[1])
			if tipo=="inteiro":
				self.func = ir.Function(self.modulo, ir.FunctionType(ir.IntType(32), ( [parametragem[i][0] for i in range(0, len(parametragem))])), name=nome)
			elif tipo=="flutuante":
				self.func = ir.Function(self.modulo, ir.FunctionType(ir.FloatType(), ( [parametragem[i][0] for i in range(0, len(parametragem))])), name=nome)
			bloco = self.func.append_basic_block('entry')
			self.builder = ir.IRBuilder(bloco)

			for i, param in enumerate(parametragem):
				self.func.args[i].name = param[1]
				self.tabela[self.escopo + '.' + param[1]]["valor"] = self.builder.alloca(param[0], name = param[1])
				self.builder.store(self.func.args[i], self.tabela[self.escopo + '.' + param[1]]["valor"])

			self.builder.ret_void()
			self.escopo = "global"

		if(node.type == "declaracao_de_funcao_sem_corpo_sem_parametros"):
			if(node.value=="principal"):
				nome ='main'
			else: nome = node.value
			self.escopo = node.value
			tipo = node.child[0].value
			self.func = ir.Function(self.modulo, ir.FunctionType(ir.VoidType(), ()), name=nome)
			bloco = self.func.append_basic_block('entry')
			self.builder = ir.IRBuilder(bloco)
			self.builder.ret_void()
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
			self.escopo = "global"

	def declaracao_param(self,node, valor=''):	
		tipos = []
		if len(node.child) > 0:
			tipo = self.tipagem(node.child[0])
			tipos.append((tipo, node.value))
			if len(node.child) > 1:	
				tipos = tipos + self.declaracao_param(node.child[1], node.value)

		return tipos

	def tipagem(self, node):
		if(node.value == 'inteiro'):
			return ir.IntType(32)
		elif node.value == 'flutuante':
			return ir.FloatType()
		else:
			return ir.VoidType()
	
	def sequencia_de_declaracao(self,node):
		if(node.type == "sequencia_de_declaracao_sem_loop"):
			return self.declaracao(node.child[0])
		else:
			self.sequencia_de_declaracao(node.child[0])
			return self.declaracao(node.child[1])

	def declaracao(self,node):
		if(node.type == "declaracao_expressao_condicional") :
			return self.expressao_condicional(node.child[0])
		if(node.type == "declaracao_expressao_iteracao") :
			return self.expressao_iteracao(node.child[0])

		if(node.type == "declaracao_expressao_atribuicao"):
			return self.expressao_atribuicao(node.child[0])

		if(node.type == "declaracao_expressao_leitura") :
			return self.expressao_leitura(node.child[0])
		
		if(node.type == "declaracao_expressao_escreva") :
			return self.expressao_escreva(node.child[0])

		if(node.type == "declaracao_declara_var") :
			return self.declara_var(node.child[0])

		if(node.type == "declaracao_retorna") :
			return self.expressao_retorna(node.child[0])

		if(node.type == "declaracao_chamada_de_funcao") :
			return self.chamada_de_funcao(node.child[0])


	def float_to_int(self, num):
		return self.builder.fptosi(num, ir.IntType(32))
	
	def int_to_float(self, num):
		return self.builder.sitofp(num, ir.FloatType())

	def expressao_condicional(self,node):
		# self.phi = True
		condicao = self.expressao(node.child[0])

		blocoDoEntao = self.func.append_basic_block(name='entao')

		if(len(node.child) == 3):
			blocoDoSenao = self.func.append_basic_block(name='senao')

		blocoFim = self.func.append_basic_block(name='fim')

		if(len(node.child) == 3):
			self.builder.cbranch(condicao, blocoDoEntao, blocoDoSenao)	
		else:
			self.builder.cbranch(condicao, blocoDoEntao,blocoFim)
				
		self.builder.position_at_end(blocoDoEntao) #valores do then
		valorDoEntao = self.sequencia_de_declaracao(node.child[1])
		self.phi = True
		self.builder.branch(blocoFim)
		blocoDoEntao = self.builder.basic_block

		if(len(node.child) == 3): #valores do else
			self.builder.position_at_end(blocoDoSenao)
			valorDoSenao = self.sequencia_de_declaracao(node.child[2])
			self.phi = True
			self.builder.branch(blocoFim)
			blocoDoSenao = self.builder.basic_block
		else:
			self.builder.position_at_end(blocoDoSenao)
			valorDoSenao = None
			self.phi = True
			self.builder.branch(blocoFim)
			blocoDoSenao = self.builder.basic_block

		self.builder.position_at_end(blocoFim)

		phi = self.builder.phi(ir.FloatType(), name= 'seTmp')
		phi.add_incoming(valorDoEntao, blocoDoEntao)

		if(len(node.child) == 3):
			phi.add_incoming(valorDoSenao, blocoDoSenao)
		self.phi = False
		return phi

	def expressao_iteracao(self, node):
		self.phi = True
		blocoRepita = self.func.append_basic_block('repita')
		blocoFimRepita = self.func.append_basic_block('fimRepita')
		self.builder.branch(blocoRepita)
		self.builder.position_at_end(blocoRepita)
		valorRepita = self.sequencia_de_declaracao(node.child[0])
		blocoRepita = self.builder.basic_block
		self.phi = True
		# print(valorRepita)
		condicao = self.expressao(node.child[1])
		self.builder.cbranch(condicao, blocoRepita, blocoFimRepita)
		self.builder.position_at_end(blocoFimRepita)
		self.phi = True
		x = str(valorRepita).split(" ")
		x = x[3].replace(",","")
		if(x=='i32'):
			phi = self.builder.phi(ir.IntType(32), 'repitaTmp')
		else:
			phi= self.builder.phi(ir.FloatType(), 'repitaTmp')
		# if(nova[6])
		# phi = self.builder.phi(ir.FloatType(), 'repitaTmp')
		phi.add_incoming(valorRepita, blocoRepita)
		self.phi = False
		return phi

	def expressao_atribuicao(self, node):
		resultado = self.expressao(node.child[0])
		if self.escopo + "." + node.value in self.tabela.keys(): 
			if self.tabela[self.escopo + "." + node.value]["tipo"] == "inteiro":	
				resultado = self.builder.fptosi(resultado, ir.IntType(32))				
				self.builder.store(resultado, self.tabela[self.escopo + "." + node.value]["valor"])
				return self.int_to_float(self.builder.load(self.tabela[self.escopo + "." + node.value]["valor"]))

			elif self.tabela[self.escopo + "." + node.value]["tipo"] == "flutuante":	
				self.builder.store(resultado,  self.tabela[self.escopo + "." + node.value]["valor"])
				return self.builder.load(self.tabela[self.escopo + "." + node.value]["valor"])
		else :

			if self.tabela["global." + node.value]["tipo"] == "inteiro":
				resultado = self.builder.fptosi(resultado, ir.IntType(32))	
				self.builder.store(resultado,  self.tabela["global." + node.value]["valor"])
				return self.int_to_float(self.builder.load(self.tabela["global." + node.value]["valor"]))
				
			elif self.tabela["global." + node.value]["tipo"] == "flutuante":
				self.builder.store(resultado,  self.tabela["global." + node.value]["valor"])
				return self.builder.load(self.tabela["global." + node.value]["valor"])

	def expressao(self,node):
		if( node.type == "expressao_simples_composta" ):
			esquerda = self.expressao_simples(node.child[0])
			operacao = self.comparacao_operador(node.child[1])
			direita = self.expressao_simples(node.child[2])

			if operacao == '=':
				return self.builder.fcmp_unordered('==', esquerda, direita, name = 'fcmpIgual')
			elif operacao == '>':
				return self.builder.fcmp_unordered('>', esquerda, direita, name ='fcmpMaior')
			elif operacao == '>=':
				return self.builder.fcmp_unordered('>=', esquerda, direita, name = 'fcmpMaiorIgual')
			elif operacao == '<':
				return self.builder.fcmp_unordered('<', esquerda, direita,  name = 'fcmpMenor')
			elif operacao == '<=':
				return self.builder.fcmp_unordered('<=', esquerda, direita, name = 'fcmpMenorIgual')
		else :
			return self.expressao_simples(node.child[0])

	def comparacao_operador(self,node):
		return node.value

	def parametros_funcao(self,node):	
		valores = []
		if len(node.child) > 1:
			valores.append(self.expressao(node.child[1]))
			valores = valores + self.parametros_funcao(node.child[0])
		elif len(node.child) == 1:
			valores.append(self.expressao(node.child[0]))
		return valores

		
	def chamada_de_funcao(self,node):
		nomeDaFuncao = node.value
		valores = self.parametros_funcao(node.child[0])
		funcao = self.modulo.get_global(nomeDaFuncao)
		tipos = self.tabela[nomeDaFuncao]["parametros"]

		i = 0
		while i < len(tipos):
			if tipos[i] == 'inteiro':
				valores[i] = self.builder.fptosi(valores[i], ir.IntType(32))
			i = i + 1

		chamada_de_funcao = self.builder.call(funcao, valores)
		# if self.tabela[nomeDaFuncao]["tipo"] == 'inteiro':
			# chamada_de_funcao = self.builder.fptosi(ir.Constant(ir.IntType(32), chamada_de_funcao), ir.FloatType())
		
		return chamada_de_funcao


	def expressao_simples(self,node):
		if(node.type == "expressao_simples_termo_com_soma"):
			esquerda = self.expressao_simples(node.child[0])
			operacao = self.soma(node.child[1])
			direita = self.termo(node.child[2])

			if operacao == "+": 
				return self.builder.fadd(esquerda, direita, 'addtmp')

			elif operacao == "-":
				return self.builder.fsub(esquerda, direita, 'subtmp')

		else :
			return self.termo(node.child[0])

	def termo(self,node):
		if(node.type == "fator_mult"):
			esquerda = self.termo(node.child[0])
			operacao = self.mult(node.child[1])
			direita = self.fator(node.child[2])

			if operacao == "*": 
				return self.builder.fmul(esquerda, direita, 'multmp')

			elif operacao == "/":
				return self.builder.fdiv(esquerda, direita, 'divtmp')

		else:
			return self.fator(node.child[0])


	def fator(self, node):
		if node.type == "fator_expressao":
			return self.expressao(node.child[0])
		elif node.type == "fator_chamada_de_funcao":
			return self.chamada_de_funcao(node.child[0])
		elif node.type == "fato_expressao_numero":
			return ir.Constant(ir.FloatType(), self.expressao_numero(node.child[0]))
		elif node.type == "fato_expressao_identificador":
			return self.expressao_identificador(node.child[0])

	def expressao_numero(self, node):
		if(node.type== "expressao_numero_composta"):
			return float(node.child[0].child[0].value) * -1
		return float(node.child[0].value)

	def expressao_identificador(self,node):
		if self.escopo + "." + node.value in self.s.keys():
			if self.tabela[self.escopo + "." + node.value]["tipo"] == "inteiro":
				return self.int_to_float(self.builder.load(self.tabela[self.escopo + "." + node.value]["valor"])) #carrega o valor
			
			elif self.tabela[self.escopo + "." + node.value]["tipo"] == "flutuante":
				return self.builder.load(self.tabela[self.escopo+"."+ node.value]["valor"])

		elif "global." + node.value in self.s.keys():
			if self.s["global." + node.value]["tipo"] == "inteiro":
				return self.int_to_float(self.builder.load(self.tabela["global." + node.value]["valor"])) #carrega o valor
			
			elif self.s["global." + node.value]["tipo"] == "flutuante":
				return self.builder.load(self.tabela["global." + node.value]["valor"])


	def expressao_escreva(self, node):
		result = self.expressao(node.child[0])
		print(result)

		print(str(result).split("="))

		if 'float' in str(result):
			resultado = self.int_to_float(result)
			return self.builder.call(self.escrevaFlutuante, [result])
		else:
			resultado = self.float_to_int(result)
			return self.builder.call(self.escrevaInteiro, [resultado])

	def expressao_leitura(self, node):
		variavel = self.builder.call(self.leiaFlutuante, [], "leiaFlutuante")
		if self.escopo + "." + node.value in self.tabela.keys():
			if self.s[self.escopo + "." + node.value]["tipo"] == "inteiro":
				self.builder.store(self.float_to_int(variavel), self.tabela[self.escopo + "." + node.value]["valor"])
				return self.builder.load(self.tabela[self.escopo+"." + node.value]["valor"])
			elif self.s[self.escopo + "." + node.value]["tipo"] == "flutuante":
				self.builder.store(variavel, self.tabela[self.escopo + '.' + node.value]["valor"])
				return  self.builder.load(self.tabela[self.escopo+"." + node.value]["valor"])
		else:
			if self.s["global." + node.value]["tipo"] == "inteiro":
				self.builder.store(self.float_to_int(variavel), self.tabela["global." + node.value]["valor"])
				return self.builder.load(self.tabela["global." + node.value]["valor"])
			elif self.s["global." + node.value]["tipo"] == "flutuante":
				self.builder.store(variavel, self.tabela["global." + node.value]["valor"])
				return self.builder.load(self.tabela["global." + node.value]["valor"])


	def expressao_retorna(self, node):
		expressao = self.expressao(node.child[0])
		print(expressao)
		print("novo")
		if self.phi==True:

			# if('i32' in str(expressao) and self.tabela[self.escopo]["tipo"]=="flutuante"):
			# 	return self.int_to_float(expressao)
			# if('i32' in str(expressao) and self.tabela[self.escopo]["tipo"]=="inteiro"):
			# 	return self.float_to_int(expressao)
			return expressao
		if self.tabela[self.escopo]["tipo"] == 'flutuante':
			expressao = self.int_to_float(expressao)
		if self.tabela[self.escopo]["tipo"] == 'inteiro':
			expressao =  self.float_to_int(expressao)

		# print("entroukkkk")
		return self.builder.ret(expressao)

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