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

	def imprimir_estatisticas(self, tempo_execucao):
		saida = open("resultados.txt", "w")

		print >> saida,  "--- Tempo de execucao: ", tempo_execucao, " segundos ---"

		print >> saida, "L1 Hits: ", self.hits_L1
		print >> saida, "L1 Misses: ", self.misses_L1
		
		print >> saida, "\nL2 Hits: ", self.hits_L2
		print >> saida, "L2 Misses: ", self.misses_L2

		print >> saida, "\nAcessos a Memoria: ", self.acessos_memoria

		print >> saida, "\nTempo em clocks: ", self.clock

		saida.close()