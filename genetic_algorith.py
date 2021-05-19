from cn_01.linked_list import LinkedList, Links
from cn_01.station import Station


class GeneticAlgorith(object):
    """""
    =============================================
    @max_gen --> indica o numero de interações
    @pop_size --> tamanho máximo para a população
    @pm --> probabilidade para mutação
    @pc --> probabilidade de cruzamento
    
    ps: as probabilidades começam em 0 como menor número e vai até 1, como valor máximo
    =============================================
    """""

    def __init__(self, max_gen=200, pop_size=40, pc=0.9, pm=0.2):

        # @counter --> contador de gerações
        self.counter = 0

        # paramentros do construtor
        self.max_max = max_gen
        self.pop_size = pop_size
        self.pc = pc
        self.pm = pm

        # self.__station = Station()
        # print(self.__station.station_components().iloc[51]['type'])  # search for a specific row

        self.lchromo = 50 # number of turbines defines the length of chromossome --> 50
        self.population = self.init_pop()

    "Método que cruza dois cromossomos"

    def crossover(self, parent):
        cut = random.randint(1, len(parent[0]) - 1)

        pa = parent[0][:cut] + parent[1][cut:]
        pb = parent[0][cut:] + parent[1][:cut]

        return [pa, pb]

    # apenas busca por indeces para iniciar a mutação
    def random_indexes(self, turb_1=0, turb_2=0):
        i1 = turb_1
        i1 = random.randint(0, self.lchromo - 1)  # busca por um indice

        i2 = turb_2
        i2 = random.randint(0, self.lchromo - 1)  # busca por outro indice

        if i1 == i2:
            return self.random_indexes(i1, i2)

        return i1, i2  # retorna dois indices

    # Mutação
    def mutation(self, chromo):
        i1, i2 = self.random_indexes()

        temp = chromo[i1]
        chromo[i1] = chromo[i2]
        chromo[i2] = temp

        return chromo

    "Gera cromossomos aleatorios para poder criar uma população"

    def random_chromo(self):
        linkedList = LinkedList()
        for _ in range(0, self.lchromo):  # i ira ter valor entre 0 e 51 (o 52 nao conta) loop de 52x
            linkedList.append(random.randint(0, self.lchromo))  # adiciona valor entre 0 e 51
        return linkedList

    "Gera populacao"
    def init_pop(self):
        return [self.random_chromo() for _ in range(self.pop_size)]

    "Imprime população"

    # def print_pop(self):
    #     for pop in self.population:
    #         print(pop, self.decode(chromo=pop, n=0), self.decode(chromo=pop, n=1))

    "Metodo de apitidao"

    def fitness(self, ch):
        weighted_mean = 0
        total_link = 0

        for i in range(1, self.lchromo):
            num_links = 0
            pointer = i
            history = []
            while pointer != 0:
                current = pointer - 1  # turbina escolhida por 'i' fica na posicao anterior para buscar na lista
                pointer = ch[current]
                current = current + 1  # Retorno com o valor que o 'i' escolheu para colocar na classe Link e adicionar no historico
                link = f'({current},{pointer})'  # adiciono a turbina escolhida e coloco com quem ela se liga
                if link not in history:  # Se nao estiver na lista de historico ele adiciona (confere se ele fecha o circulo)
                    history.append(link)
                    num_links = num_links + 1
                else:
                    num_links = 0  # passa a ter 0 ligações
                    break

            total_link = total_link + num_links

            # Classe para adicionar um numero de ligacoes e retornar o custo destas ligacoes para uma turbina
            turbineLink = Links(num_links)
            weighted_mean = weighted_mean + turbineLink.multiplication()

        return 0 if total_link == 0 else 1 / (weighted_mean / total_link)  # quanto menor melhor

    "Dentro da populacao, ele ira pegar aleatoriamente 1"

    def select_random(self, fits_population):
        return fits_population[random.randint(0, len(fits_population) - 1)]

    def decode_linklist(self, ch):  # vai deixar de ser uma linked list e virar uma array comum.
        return [ch[i] for i in range(self.lchromo)]

    'Retorna tupla da população junto com o fitness'

    # def fits_population(self):
    #     return [(self.fitness(x), x) for x in self.population]

    def fits_population(self):
        return [(self.fitness(x), self.decode_linklist(x)) for x in self.population]

    '''''
    Aqui dentro ira fazer buscar aleatoriamente 1,
    Depois ira buscar outro que por fim vai ver quem dos dois e melhor.
    Metodo de torneio
    OBS: Metodo da roleta tem que ser de maximizacao, se nao isso nao ira funcionar
    '''''

    def tournament_method(self, fits_population):
        f1, x1 = self.select_random(fits_population=fits_population)
        f2, x2 = self.select_random(fits_population=fits_population)
        if f1 == 0 and f2 == 0:
            return x1
        elif f1 == 0:
            return x2
        elif f2 == 0:
            return x1
        elif f1 < f2:
            return x1
        else:
            return x2
        # return x1 if f1 < f2 else x2  # Verifica qual destes é menor e retorna.

    'Vai selecionar o pai e depois a mae e depois retorna um par de elementos'

    def parents(self, fits_population):
        """ Nesse caso o ciclo e infinito, quando encontrado o valor o ele suspende por causa do yield
         entretando, quando rodado novamente ele continua o ciclo de onde parou e suspende novamente
        """
        while True:
            pai = self.tournament_method(fits_population=fits_population)
            mae = self.tournament_method(fits_population=fits_population)

            yield pai, mae  # aqui e tipo o return so que suspende a funcao

    'Checa se é hora de parar'

    def check_stops(self, fits_population):
        # @fit --> valor da aptidao
        self.counter = self.counter + 1  # incrementa o numero de geracoes
        # if self.counter % 10 == 0:  # mostra em 10 em 10 geracoes
        """
        # (f,x) o elemento 0 indica 'f' e o elemento 1 indica o 'x'
        # isso pq e um problema de minimizacao, caso fosse um problema de max ao invez de
        # procurarmos um o primeiro elemento por 0, procuramos o ultimo elemento por -1 (obs: o penultimo e -2)
        """
        best_chrome = list(sorted(fits_population))[0][1]
        # print(self.fitness(ch=best_chrome), self.decode(best_chrome, 0))

        # salva apenas os fits e deixa de lado os ch
        fits = [f for f, ch in fits_population]

        best = min(fits)
        worst = max(fits)

        avg = sum(fits) / len(fits)

        print(f'[G- {self.counter}] best -> {best}, wrost -> {worst} avg -> {avg}')

        # string1 = '[' + ''.join([str(k) for k in best_chrome]) + ']'
        # string2 = '(' + ''.join([str(self.decode(best_chrome, k)) for k in range(self.npar)]) + ')'
        # print(
        #     f"[G {round(self.counter, 3)}] score = (best ->  {round(best, 4)}, avg-> {round(avg, 4)}, "
        #     f"worst -> {round(worst, 4)}) -- {string1} -- {string2}"
        # )

        return self.counter >= self.max_max

    '''Responsável em rodar o programa'''

    def run(self):
        # pop = self.init_pop()
        while True:
            # coloca o fit na populcao
            # fits_pop = self.fits_population()
            fits_pops = [(self.fitness(x), self.decode_linklist(x)) for x in self.population]

            if self.check_stops(fits_pops):  break  # verifica se ja chegou ao fim

            self.population = self.next(fits_pops)  # caso nao tenha terminado, determina quem e a proxima populacao

            # Transforma de novo em linkedlist

            self.population = self.encode()
        return self.population

    def encode(self):
        ll_list = []
        for i in self.population:
            linkedList = LinkedList()
            for j in range(len(i)):
                linkedList.append(i[j])
            ll_list.append(linkedList)
        return ll_list

    '''Ira inicializar a proxima populacao'''

    def next(self, fits):
        # gera os novos parents
        parents_generator = self.parents(fits)
        size = len(fits)

        # elemento da população que vao sendo selecionados
        nexts = []

        while (len(nexts) < size):
            # captura os novos pais
            parents = next(parents_generator)  # funcation next --> diferente da funcao next que esta a ser criada
            cross = random.random() < self.pc  # ira retornar true ou false, true para realizar mutacao e false para nao realizar

            # else -> os descedentes tomam o valor dos pais sem cruzamento / retorna [cromossoma1, cromossoma2]
            children = self.crossover(parents) if cross else parents

            for ch in children:
                mutate = random.random() < self.pm  # ira retornar true ou false para realização de uma mutação
                nexts.append(self.mutation(ch) if mutate else ch)  # adiciona um novo elemento na nova população
        return nexts[0:size]


import random

ga = GeneticAlgorith(pop_size=200)
ga.run()
