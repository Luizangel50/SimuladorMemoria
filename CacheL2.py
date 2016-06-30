from math import log

class CacheL2:
	"""Classe utilizada para especificar a Cache L1"""

	def __init__(self, tamanho_cache, tamanho_bloco, vias):
		"""Construtor"""
		
		self.tamanho_endereco = 32																		# Tamanho do endereco
		self.tamanho_cache = tamanho_cache																# Tamanho total da cache em Kbytes
		self.tamanho_bloco = tamanho_bloco																# Tamanho do bloco em bytes
		self.vias = vias																				# Associatividade
		self.tempo_acesso = 4																			# Tempo (em clocks) de acesso em L1
		self.tempo_tag = 2																				# Tempo (em clocks) de comparacao de tag

		self.quantidade_conjuntos = int((tamanho_cache*1024)/(vias*tamanho_bloco))						# Quantidade de conjuntos de blocos existentes
		self.cache = {}
		self.cache['tag'] = [[-1 for i in range(vias)] for j in range(self.quantidade_conjuntos)]		# Cache propriamente dita: armazena as tags
		self.cache['sujo'] = [[0 for i in range(vias)] for j in range(self.quantidade_conjuntos)]		# Blocos sujos da cache = 1, limpos = 0
		self.fifo = [[-1 for i in range(vias)] for j in range(self.quantidade_conjuntos)]				# Fila da cache

	def traducao_endereco(self, endereco):
		"""Realiza a traducao do endereco virtual"""

		bits_set = int(log(self.quantidade_conjuntos, 2))												# Quantidade de bits do endereco destinada ao set (conjunto ou via)
		bits_offset = int(log(self.tamanho_bloco, 2))													# Quantidade de bits do endereco destinada ao offset
		bits_tag = self.tamanho_endereco - (bits_set + bits_offset)										# Quantidade de bits do endereco destinada a tag

		offset = endereco & int(self.tamanho_bloco - 1)													# Offset do endereco
		set = (endereco >> bits_offset) & int(self.quantidade_conjuntos - 1)							# Set do endereco
		tag = endereco >> (bits_set + bits_offset)														# Tag do endereco

		# print "Offset: " , str(bin(offset)), "; ", bits_offset
		# print "Set: ", bin(set), "; ", bits_set, "; ", self.quantidade_conjuntos
		# print "Tag: ", bin(tag), "; ", bits_tag

		return (tag, set, offset)

	def bloco_existente(self, endereco_traduzido, estatisticas, tipo_acesso):
		"""Verifica se o bloco existe na Cache"""

		# Acesso do tipo leitura
		if tipo_acesso == "leitura":
			set = endereco_traduzido[1]
			tag = endereco_traduzido[0]
			for i in range(0, self.vias):
				# Read hit
				if(self.cache['tag'][set][i] == tag):
					estatisticas.hits_L2 += 1											# Atualizacao das estatisticas
					estatisticas.clock += self.tempo_acesso + self.tempo_tag			# Incremento do clock
					return True

			# Read miss
			estatisticas.misses_L2 += 1
			return False

		elif tipo_acesso == "escrita":
			set = endereco_traduzido[1]
			tag = endereco_traduzido[0]
			for i in range(0, self.vias):
				# Write hit: marcar bloco como sujo
				if(self.cache['tag'][set][i] == tag):
					self.cache['sujo'][set][i] = 1										# Marcando bloco como sujo
					estatisticas.hits_L2 += 1											# Atualizacao das estatisticas
					estatisticas.clock += self.tempo_acesso + self.tempo_tag			# Incremento do clock

					return True

			# Write miss
			estatisticas.misses_L2 += 1
			return False

	def atualizar_fifo(self, set):
		"""Atualiza a fila de blocos em um set"""

		for i in range(0, self.vias-1):
			self.fifo[set][i] = self.fifo[set][i+1]


	def alocar_bloco(self, endereco_traduzido, estatisticas):
		"""Aloca bloco na cache"""

		set = endereco_traduzido[1]
		tag = endereco_traduzido[0]

		for i in range(0, self.vias):
			# Existe espaco no conjunto para alocar o bloco
			if self.cache['tag'][set][i] == -1:			
				self.cache['tag'][set][i] = tag
				self.atualizar_fifo(set)
				self.fifo[set][self.vias-1] = tag
				# print self.cache['tag'][set]
				# print self.cache['sujo'][set]
				# print self.fifo[set]
				return

		bloco_substituido = self.fifo[set][0]

		# Politica de substituicao de blocos: FIFO
		for j in range(0, self.vias):
			# Achando bloco a ser substituido
			if self.cache['tag'][set][j] == bloco_substituido :

				# Verifica se o bloco esta sujo ou limpo
				if self.cache['sujo'][set][j] == 1:
					# Atualizacao na memoria do bloco sujo
					estatisticas.clock += 60
					estatisticas.acessos_memoria += 1

				self.cache['tag'][set][j] = tag					# Substituindo tag
				self.cache['sujo'][set][j] = 0					# Setando o bloco como limpo
				self.atualizar_fifo(set)						# Atualizando a fila
				self.fifo[set][self.vias-1] = tag 				# Colocando o novo bloco na ultima posicao da fila

				# print self.cache['tag'][set]
				return


	def leitura(self, endereco, estatisticas):
		"""Realiza a operacao de leitura na Cache"""

		# Tupla com o endereco separado em tag, set e offset
		endereco_traduzido = self.traducao_endereco(endereco)
		
		hit = self.bloco_existente(endereco_traduzido, estatisticas, "leitura")

		# Aloca o bloco na cache se ele nao estiver presente
		if not hit:
			self.alocar_bloco(endereco_traduzido, estatisticas)

		return hit


	def escrita(self, endereco, estatisticas):
		"""Realiza a operacao de escrita na Cache"""

		# Tupla com o endereco separado em tag, set e offset
		endereco_traduzido = self.traducao_endereco(endereco)

		hit = self.bloco_existente(endereco_traduzido, estatisticas, "escrita")

		return hit