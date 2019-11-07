from node import Node, Chromosome, Generations
from mp import Mp
from animate import generateAnimation 




def simulate(fileName, populationSize, numParents, numSwaps, mutationProb,mutationSwaps,start,stop):
    #simulation
    simulation = Generations(fileName, populationSize,numParents, numSwaps,mutationProb, mutationSwaps)
    simulation.readFile(start,stop)
    simulation.generatePopulation()

    evolutionArray = []


    for i in range(numGenerations):
        simulation.selectParents()
        simulation.crossParents()
        simulation.mutation()

        results = simulation.getBest()
        evolutionArray.append(results[0].nodes)
        print(results[1])

    return results[0].nodes

def simaleteWithNodes(fileName, populationSize,numParents, numSwaps,mutationProb, mutationSwaps,res,limitCostGeneration,prn=False):
    #simulation
    simulation = Generations(fileName, populationSize,numParents, numSwaps,mutationProb, mutationSwaps)
    simulation.generatePopulationFromArray(res,limitCostGeneration)

    evolutionArray = []


    for i in range(numGenerations):
        simulation.selectParents()
        simulation.crossParents()
        simulation.mutation()

        results = simulation.getBest()
        evolutionArray.append(results[0].nodes)
        print(results[1])

    if prn:
        generateAnimation(evolutionArray, numGenerations-1)
        for i in results[0].nodes:
            print(i.city)
    return results[0].nodes
    





fileName = 'CiudadesMX.csv'
populationSize = 100
numParents = 20
numSwaps = 16
mutationProb = 5#0-100
numGenerations = 50
mutationSwaps = 2
results = []

cycles = 8
cyclesStep = 4

for i in range(cycles):
    results.append(simulate(fileName, populationSize, numParents, numSwaps, mutationProb,mutationSwaps,i*cyclesStep,i*cyclesStep+cyclesStep))


populationSize = 100
numParents = 20
numSwaps = 16
mutationProb = 5#0-100
numGenerations = 100
mutationSwaps = 4
limitCostGeneration = 999
results2 = []

cycles = 4
cyclesStep = 2

for i in range(cycles):
    results2.append(simaleteWithNodes(fileName, populationSize,numParents, numSwaps,mutationProb, mutationSwaps,results[i*cyclesStep:i*cyclesStep+2],limitCostGeneration))


populationSize = 200
numParents = 40
numSwaps = 8
mutationProb = 5#0-100
numGenerations = 200
mutationSwaps = 4
limitCostGeneration = 999
results3 = []

cycles = 2
cyclesStep = 2

for i in range(cycles):
    results3.append(simaleteWithNodes(fileName, populationSize,numParents, numSwaps,mutationProb, mutationSwaps,results2[i*cyclesStep:i*cyclesStep+2],limitCostGeneration))


populationSize = 1000
numParents = 200
numSwaps = 4
mutationProb = 10#0-100
numGenerations = 300
mutationSwaps = 4
limitCostGeneration = 999


simaleteWithNodes(fileName, populationSize,numParents, numSwaps,mutationProb, mutationSwaps,results3,limitCostGeneration,True)