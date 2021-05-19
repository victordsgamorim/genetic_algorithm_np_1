from cn_01.linked_list import LinkedList, Links
from cn_01.station import Station
import networkx as nx
import matplotlib.pyplot as plt
import numpy as np


class GeneticAlgorith(object):
    """""
    =============================================
    @max_gen --> number of generation
    @pop_size --> population max size
    @pm --> mutation prob
    @pc --> crossover prob
    @pl --> closest turb linking prob
    @counter --> generation counter
    =============================================
    """""

    def __init__(self, max_gen=1000, pop_size=40, pc=0.9, pm=0.2, pl=0.6):
        self.counter = 0

        self.__max_max = max_gen
        self.__pop_size = pop_size
        self.__pc = pc
        self.__pm = pm
        self.__pl = pl

        self.__station = Station()
        self.__linking = Links()

        self.__lchrome = self.__station.turbines.size()  # 50
        self.__population = self.__init_pop()

        self.G = nx.Graph()

    "Method of mixing/crossing two chromes "

    def __crossover(self, parent):
        cut = random.randint(1, len(parent[0]) - 1)

        pa = parent[0][:cut] + parent[1][cut:]
        pb = parent[0][cut:] + parent[1][:cut]

        return [pa, pb]

    "Search for 2 random indexes in order to start mutation "

    def __random_indexes(self, turb_1=0, turb_2=0):
        i1 = turb_1
        i1 = random.randint(0, self.__lchrome - 1)  # busca por um indice

        i2 = turb_2
        i2 = random.randint(0, self.__lchrome - 1)  # busca por outro indice

        # recursive method in order to find a random number,
        # method which validate if random number are the same, if so, run the method one more time
        if i1 == i2:
            return self.__random_indexes(i1, i2)

        return i1, i2  # retorna dois indices

    "Mutation"

    def __mutation(self, chromo):
        i1, i2 = self.__random_indexes()
        chromo[i1] = random.randint(0, self.__lchrome + 1)
        chromo[i2] = random.randint(0, self.__lchrome + 1)
        return chromo

    "Pupulate random numbers into a linkedlist in order to generate a chrome "

    # def __random_chrome(self):
    #     linkedList = LinkedList()
    #     for _ in range(0, self.__lchrome):  # 'i' will have values from 0 to 49 (chrome length 50)
    #         linkedList.append(
    #             random.randint(0, self.__lchrome + 1))  # add numbers between 0 and 51 (0, 1 substation/ 2-51 turbines)
    #     return linkedList

    def __random_chrome(self):
        linkedList = LinkedList()
        for i in range(0, self.__lchrome):  # 'i' will have values from 0 to 49 (chrome length 50)
            rand = None
            if random.random() < self.__pl:
                rand = self.__linking.closer(self.__station, i + 2)
            else:
                rand = random.randint(0, self.__lchrome + 1)
            linkedList.append(rand)  # add numbers between 0 and 51 (0, 1 substation/ 2-51 turbines)
        return linkedList

    "Generate Population"

    def __init_pop(self):
        return [self.__random_chrome() for _ in range(self.__pop_size)]

    "Fitness -> The smaller the better! It's calculated by finding the inverse of the weighted mean"

    def fitness(self, ch):
        weighted_mean = 0
        total_link = 0
        cost = 0

        for i in range(2, len(self.__station)):
            num_links = 0
            pointer = i
            history = []
            while pointer > 1:
                current = pointer - 2  # Chosen turbine found by 'i' which is located 2 positions before in roder to found its value (which it links)
                pointer = ch[current]
                current = current + 2  # Returns the value which 'i'(turbine x) has found out, insert in a Link class, after that, append to history list
                link = f'({current},{pointer})'  # Add chosen turbine with linked turbine into string
                if link not in history:  # If it isn't in the history list, so, be stored, if it is, it means there a cycle
                    history.append(link)
                    num_links = num_links + 1
                else:
                    num_links = 0  # update to 0 link -> just if there is a cycle
                    break

            total_link = total_link + num_links

            # Add number of links and return the cost of its links into the class
            turbineLink = Links(num_links)
            cost = cost + turbineLink.cost
            weighted_mean = weighted_mean + turbineLink.multiplication()

        # Weighted Mean -> The smaller the better
        return (0,cost) if total_link == 0 else (1 / (weighted_mean / total_link), cost)

    "Inside population list of linkedlist, picks up a random chrome(linkedlist)"

    def select_random(self, fits_population):
        return fits_population[random.randint(0, len(fits_population) - 1)]

    def decode_linklist(self, ch):  # vai deixar de ser uma linked list e virar uma array comum.
        return [ch[i] for i in range(self.__lchrome)]

    'Returns a row with fitness and population [(fitnees / population)]'

    # def fits_population(self):
    #     return [(self.fitness(x), self.decode_linklist(x)) for x in self.__population]

    '''''
    Tournament Method
    1 - Retuns a  2 random linkedlist
    2 - Verify which has better fitness
    '''''

    def tournament_method(self, fits_population):
        f1, x1 = self.select_random(fits_population=fits_population)
        f2, x2 = self.select_random(fits_population=fits_population)

        # Verify which one is smaller.
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

    'Select a father and a mother and then returns a pair of elements'

    def parents(self, fits_population):
        while True:
            f = self.tournament_method(fits_population=fits_population)
            m = self.tournament_method(fits_population=fits_population)

            yield f, m  # returns father and mother

    "Is it time to finish ? "

    def check_stops(self, fits_population):

        # increment the number of generations
        self.counter = self.counter + 1
        # best_chrome = list(sorted(fits_population))[0][1]

        # saves the chromes and leave fits
        chromes = [ch for f, ch in fits_population]

        # saves the fits and leave chromes
        fits = [f for f, ch in fits_population]


        best = min(fits)
        res = 10
        if best == 0:
            for i in fits:
                if i < res and i != 0:
                    res = i

        if(res != 10):
            best = res

        worst = max(fits)

        index_best = fits.index(best)
        best_chrome = chromes[index_best]

        fitness, cost =self.fitness(best_chrome)



        avg = sum(fits) / len(fits)

        print(
            f'[G- {self.counter}] best_chrome = {best_chrome} ---- \ncost= {cost} ----- score = best -> {round(best, 5)}, wrost -> {round(worst, 5)} avg -> {round(avg, 5)}')

        return self.counter >= self.__max_max

    'Runs the program'

    def run(self):
        while True:

            fits_pops = [(self.fitness(x), self.decode_linklist(x)) for x in self.__population]
            costs = []
            new_fits_pops = []

            for i in range(len(fits_pops)):
                costs.append(fits_pops[i][0][1])
                new_fits_pops.append((fits_pops[i][0][0], fits_pops[i][1]))

            # list = fits_pops[0][1]
            # new_fits_popos = fitness, list

            # verify if it's the end
            if self.check_stops(new_fits_pops):
                break

            # in case is not the end, determine who is the next population
            self.__population = self.next(new_fits_pops)  #
            # Transform into linkedlist
            self.__population = self.encode()
        return self.__population

    def encode(self):
        ll_list = []
        for i in self.__population:
            linkedList = LinkedList()
            for j in range(len(i)):
                linkedList.append(i[j])
            ll_list.append(linkedList)
        return ll_list

    'initialize the next population '

    def next(self, fits):
        # generate new parents
        parents_generator = self.parents(fits)
        size = len(fits)

        # the chosen ones which are being selected
        nexts = []

        while (len(nexts) < size):
            # capture new parents
            parents = next(parents_generator)
            cross = random.random() < self.__pc  # choose if want to crossover or not by returning true or false

            children = self.__crossover(parents) if cross else parents
            for ch in children:
                mutate = random.random() < self.__pm  # choose if want to mutate or not by returning true or false
                nexts.append(self.__mutation(ch) if mutate else ch)  # add new elements to population
        return nexts[0:size]

    def network(self):

        # um elemento da população ideal
        one_chrome_ideal_pop = self.decode_linklist(self.__population[0])

        x = self.__station.station_components()['lon'].to_numpy()
        y = self.__station.station_components()['lat'].to_numpy()
        for i in range(len(x)):
            self.G.add_node(i, pos=(x[i], y[i]))

        # random_chrome = self.decode_linklist(self.__random_chrome())
        position = 2
        for i in range(len(one_chrome_ideal_pop)):
            self.G.add_edge(position, one_chrome_ideal_pop[i])
            position = position + 1

        pos = nx.get_node_attributes(self.G, 'pos')
        nx.draw(self.G, pos, with_labels=True, node_size=180, font_size=12)
        plt.show()


import random

ga = GeneticAlgorith(pop_size=500)
ga.run()
ga.network()
