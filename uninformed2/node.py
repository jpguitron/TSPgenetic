import math
from random import shuffle
import random
import copy
import csv


#Location/gen
class Node:
    def __init__(self, node_id, state,city, lat, lon):
        self.id = node_id
        self.state = state
        self.city = city
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
    def __init__(self, fileName, populationSize, numParents, numSwaps, mutationProb, mutationSwaps):
        self.populationSize = populationSize
        self.fileName = fileName
        self.numParents = numParents
        self.numSwaps = numSwaps
        self.mutationProb = mutationProb
        self.mutationSwaps = mutationSwaps

    #Read data from csv file and store it 
    def readFile(self,start,stop):
        self.nodes = []

        with open(self.fileName, encoding = "ISO-8859-1") as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            line_count = 0
            for row in csv_reader:
                if line_count != 0 and line_count<=stop and start<line_count:
                    node = Node(row[0],row[1],row[2],row[3],row[4])
                    self.nodes.append(node)
                line_count += 1

    #Generate a random population
    def generatePopulation(self):
        self.populationArray = []
        for i in range(self.populationSize):
            chromosome = Chromosome(self.nodes)
            chromosome.randomShuffle()
            self.populationArray.append(chromosome)
    
    def generatePopulationFromArray(self,data,limit):
        self.populationArray = []

        i = 0
        while i<self.populationSize:
            nodes = []
            passed = []
            for numDat in range(len(data)):
                randArray = random.randrange(0,len(data),1)
                while (randArray in passed):
                    randArray = random.randrange(0,len(data),1)
                passed.append(randArray)

                if len(nodes)==0:
                    insertArray=0
                else:
                    insertArray = random.randrange(0,len(nodes),1)

                for index in range(len(data[randArray])):
                    nodes.insert(insertArray, data[randArray][index])
            
            chromosome = Chromosome(nodes)
            if chromosome.getTotalCost() <= limit:
                self.populationArray.append(chromosome)
                i += 1

    
    def takeFirst(self,elem):
        return elem[0]

    #Select Chromosomes for the next generation
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
        
        costPopulation = list(zip(costsList,self.populationArray))
        costPopulation.sort(key=self.takeFirst)
        
        costsList.clear()
        self.populationArray.clear()

        for i in costPopulation:
            costsList.append(i[0])
            self.populationArray.append(i[1])


        for i in range(int(self.populationSize/2)):
            percentage = ((self.populationSize/2)-i)/(self.populationSize/2)
            percentageChange = costsList[i]*percentage
            costsList[i] -= percentageChange 
            costsList[self.populationSize-i-1] += percentageChange 

        #Select unique parents
        self.parents = random.choices(self.populationArray, costsList,k=self.numParents)
    
    def crossParents(self):
        self.populationArray.clear()
        for pobI in range(self.populationSize):#poblacion
            
            selectedParents = random.sample(range(0, self.numParents), 2)#select parents for new chromosome
            chromosome = Chromosome(self.parents[selectedParents[0]].nodes)

            selected = random.randrange(0,len(self.parents[selectedParents[1]].nodes),1)
            for i in range(self.numSwaps):
                
                if selected+i < len(self.parents[selectedParents[1]].nodes):
                    node = self.parents[selectedParents[1]].nodes[selected+i]

                    indexInChromosome = chromosome.getIndex(node)
                    chromosome.nodes.pop(indexInChromosome)
                    
                    chromosome.nodes.insert(selected+i,node)

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
                for swap in range(self.mutationSwaps):
                    while True:
                        pos1 = random.randrange(0,len(i.nodes),1)
                        pos2 = random.randrange(0,len(i.nodes),1)
                        if pos1 != pos2:
                            i.nodes[pos1], i.nodes[pos2] = i.nodes[pos2], i.nodes[pos1] 
                            break