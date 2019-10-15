import math
from random import shuffle
import random
import copy
import csv


#Location/gen
class Node:
    def __init__(self, node_id, state, lat, lon):
        self.id = node_id
        self.state = state
        self.lat = float(lat)
        self.lon = float(lon)

    def getCost(self,other_city_node):
        xDistance = (self.lat-other_city_node.lat)**2
        yDistance = (self.lon-other_city_node.lon)**2
        distance = math.sqrt(xDistance+yDistance)
        return distance

#Route
class Chromosome:
    def __init__(self, nodes):
        self.nodes = copy.deepcopy(nodes)        

    def randomShuffle(self):
        shuffle(self.nodes)

    def getTotalCost(self):
        totalCost = 0
        for i in range(len(self.nodes)):
            if i+1 < len(self.nodes):
                totalCost += self.nodes[i].getCost(self.nodes[i+1]) 
            else:
                totalCost += self.nodes[0].getCost(self.nodes[len(self.nodes)-1])
        return totalCost
    
    def getIndex(self, nodeSearched):
        counter=0
        for node in self.nodes:
            if node.id == nodeSearched.id:
                return counter
            counter += 1
        return -1

#generations manager
class Generations:
    def __init__(self, fileName, populationSize, numParents, numSwaps,mutationProb):
        self.populationSize = populationSize
        self.fileName = fileName
        self.numParents = numParents
        self.numSwaps = numSwaps
        self.mutationProb = mutationProb

    #Read data from csv file and store it 
    def readFile(self):
        self.nodes = []
        with open(self.fileName, encoding = "ISO-8859-1") as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            line_count = 0
            for row in csv_reader:
                if line_count != 0:
                    node = Node(row[0],row[1],row[3],row[4])
                    self.nodes.append(node)
                line_count += 1

    #Generate a random population
    def generatePopulation(self):
        self.populationArray = []
        for i in range(self.populationSize):
            chromosome = Chromosome(self.nodes)
            chromosome.randomShuffle()
            self.populationArray.append(chromosome)
    
    #Select two Chromosomes for the next generation
    def selectParents(self):
        totalCosts = 0
        costsList = []
        for i in self.populationArray:
            currentCost = i.getTotalCost()
            totalCosts += currentCost
            costsList.append(currentCost)

        for i in range(len(costsList)):
            costsList[i] = costsList[i]/totalCosts
        # Invert costs
        costsList = [1.0 / c for c in costsList]         
        sum_costsList = sum(costsList)

        # Normalize costs
        costsList = [w / sum_costsList for w in costsList] 
        
        #Select unique parents
        self.parents = random.choices(self.populationArray, costsList,k=self.numParents)
    
    def crossParents(self):
        self.populationArray.clear()
        for pobI in range(self.populationSize):#poblacion
            selectedParents = random.sample(range(0, self.numParents), 2)#select parents for new chromosome
            chromosome = Chromosome(self.parents[selectedParents[0]].nodes)

            for i in range(self.numSwaps):
                selected = random.randrange(0,len(self.parents[selectedParents[1]].nodes),1)
                
                node = self.parents[selectedParents[1]].nodes[selected]
                
                indexInChromosome = chromosome.getIndex(node)
                chromosome.nodes.pop(indexInChromosome)
                chromosome.nodes.insert(selected,node)

            self.populationArray.append(chromosome)

    def getBest (self):
        best = self.populationArray[0]
        bestCost = self.populationArray[0].getTotalCost()
        for i in self.populationArray[1:]:
            cCost = i.getTotalCost()
            if cCost < bestCost:
                best = i
                bestCost = cCost
        return best, bestCost

    
    

    def mutation(self):
        for i in self.populationArray:
            randNum = random.randrange(0,100,1)
            if randNum < self.mutationProb:
                while True:
                    pos1 = random.randrange(0,len(i.nodes),1)
                    pos2 = random.randrange(0,len(i.nodes),1)
                    if pos1 != pos2:
                        i.nodes[pos1], i.nodes[pos2] = i.nodes[pos2], i.nodes[pos1] 
                        break