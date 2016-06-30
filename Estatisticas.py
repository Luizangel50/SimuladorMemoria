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

	def imprimir_estatisticas(self, tempo_execucao, clock):
		print "--- Tempo de execucao: ", tempo_execucao, " segundos ---"

		print "L1 Hits: ", self.hits_L1
		print "L1 Misses: ", self.misses_L1
		
		print "\nL2 Hits: ", self.hits_L2
		print "L2 Misses: ", self.misses_L2

		print "\nAcessos a Memoria: ", self.acessos_memoria

		print "\nTempo em clocks: ", clock