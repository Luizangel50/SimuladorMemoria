import Estatisticas
import CacheL1
import CacheL2
import time

def main():
	"""Funcao principal"""

	####################### Inicializando variaveis ##################

	# Tempo do comeco da execucao do programa
	start_time = time.time()

	# Objeto que armazena as estatisticas
	estatisticas = Estatisticas.Estatisticas()

	# Objeto que representa a Cache L1
	cacheL1 = CacheL1.CacheL1(32, 64, 8)

	# Objeto que representa a Cache L2
	cacheL2 = CacheL2.CacheL2(4096, 64, 16)

	# Chamando funcao que executa a simulacao de memoria
	acesso(start_time, cacheL1, cacheL2, estatisticas)

	# Imprimindo estatisticas na saida
	estatisticas.imprimir_estatisticas(time.time() - start_time)

	############################ Pequena explicacao da politica de read e write ###############################
	################## Read #################
	# Se tiver em L1, ignora os outros (tempo de L1)
	# Se tiver em L2 mas nao em L1, aloca em L1 (tempo de L2)
	# Se nao tiver em L1 nem em L2, aloca em L1 e em L2 (tempo memoria)


	################## Write #################
	# Tem em L1 em L2, grava em L1 e L2 (tempo de L2)
	# Tem em L1 e nao L2, grava em L1 e memoria (tempo de memoria)
	# Nao tem em L1 e tem em L2, grava em L2 e L1 (tempo de L2)
	# Nao tem em nenhum lugar, grava em L1 e memoria (tempo de memoria)


def acesso(start_time, cacheL1, cacheL2, estatisticas):
	"""Funcao que faz a simulacao de memoria"""

	# Ler cada linha do arquivo de entrada ate EOF
	for line in open("arquivo de entrada/gcc.trace", "r"):
		linha = line.split()
		endereco = linha[0]
		tipo_acesso = linha[1]

		# Convertendo o a string do endereco hexadecimal em um inteiro
		endereco = int(endereco, 16)
		
		# Acesso de leitura
		if tipo_acesso == "R":
			readhit_L1 = cacheL1.leitura(endereco, estatisticas)

			# Read miss em L1
			if not readhit_L1:
				readhit_L2 = cacheL2.leitura(endereco, estatisticas)

				# Read miss em L1 e em L2
				if not readhit_L2:
					estatisticas.clock += 60
					estatisticas.acessos_memoria += 1

		# Acesso de escrita
		elif tipo_acesso == "W":
			writehit_L1 = cacheL1.escrita(endereco, estatisticas)
			writehit_L2 = cacheL2.escrita(endereco, estatisticas)
			
			# Write hit em L1
			if writehit_L1:

				# Write hit em L2
				if writehit_L2:
					# Contar apenas o tempo de acesso e de comparacao de tag de L2
					estatisticas.clock -= (cacheL1.tempo_acesso + cacheL1.tempo_tag)

				# Write miss em L2
				elif not writehit_L2:
					# Contar apenas o tempo de acesso a memoria
					estatisticas.clock += 60 - (cacheL1.tempo_acesso + cacheL1.tempo_tag)
					estatisticas.acessos_memoria += 1

			# Write miss em L1
			if not writehit_L1:

				# Write miss em L2
				if not writehit_L2:
					# Bloco trazido da memoria
					# Contar apenas o tempo de acesso a memoria
					estatisticas.clock += 60 - (cacheL1.tempo_acesso + cacheL1.tempo_tag)
					estatisticas.acessos_memoria += 1

if __name__ == "__main__":
	main()