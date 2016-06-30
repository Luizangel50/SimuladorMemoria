class Estatisticas:
	"""Classe utilizada para guardar dados estatisticos
	de acessos, hits e misses nas caches e na memoria"""

	def __init__(self):

		# Estatisticas para a Cache L1
		self.hits_L1 = 0
		self.misses_L1 = 0

		# Estatisticas para a Cache L2
		self.hits_L2 = 0
		self.misses_L2 = 0

		# Estatisticas para a Memoria
		self.acessos_memoria = 0

		# Contador do tempo em clocks
		self.clock = 0

		# Estatisticas para leitura
		self.leituras = 0

		# Estatisticas para escrita
		self.escritas = 0

	def imprimir_estatisticas(self, tempo_execucao, arquivo_saida):
		saida = open(arquivo_saida, "w")

		print >> saida, "--- Tempo de execucao: ", tempo_execucao, " segundos ---"

		print >> saida, "\nLeituras: ", self.leituras, "(", float(self.leituras)/float(10000), "%)"
		print >> saida, "Escritas: ", self.escritas, "(", float(self.escritas)/float(10000), "%)"

		print >> saida, "\nL1 Hits: ", self.hits_L1, "(", float(self.hits_L1)/float(10000), "%)"
		print >> saida, "L1 Misses: ", self.misses_L1, "(", float(self.misses_L1)/float(10000), "%)"
		
		print >> saida, "\nL2 Hits: ", self.hits_L2, "(", float(self.hits_L2*100)/float(self.hits_L2+self.misses_L2), "%)"
		print >> saida, "L2 Misses: ", self.misses_L2, "(", float(self.misses_L2*100)/float(self.hits_L2+self.misses_L2), "%)"

		print >> saida, "\nAcessos a Memoria Principal: ", self.acessos_memoria, "(", float(self.acessos_memoria)/float(10000), "%)"

		print >> saida, "\nTempo total em clocks: ", self.clock

		saida.close()