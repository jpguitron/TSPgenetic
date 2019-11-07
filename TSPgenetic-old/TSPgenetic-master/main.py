from node import Node, Chromosome, Generations
from mp import Mp
from animate import generateAnimation

fileName = 'CiudadesMX.csv'
populationSize = 500
numParents = 100
numSwaps = 16
mutationProb = 5#0-100
numGenerations = 300
mutationSwaps = 4



#simulation
simulation = Generations(fileName, populationSize,numParents, numSwaps,mutationProb, mutationSwaps)
simulation.readFile()
simulation.generatePopulation()

evolutionArray = []


for i in range(numGenerations):
    simulation.selectParents()
    simulation.crossParents()
    simulation.mutation()

    results = simulation.getBest()
    evolutionArray.append(results[0].nodes)
    print(results[1])

generateAnimation(evolutionArray, numGenerations-1)
#mxMap = Mp()
#mxMap.generateLines(results[0].nodes)
#mxMap.display()


for i in results[0].nodes:
    print(i.city)
