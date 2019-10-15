from node import Node, Chromosome, Generations


fileName = 'CiudadesMX.csv'
populationSize = 1000
numParents = 10
numSwaps = 5
mutationProb = 5#0-100
numGenerations = 100



#simulation
simulation = Generations(fileName, populationSize,numParents, numSwaps,mutationProb)
simulation.readFile()
simulation.generatePopulation()

for i in range(numGenerations):
    simulation.selectParents()
    simulation.crossParents()
    simulation.mutation()
results = simulation.getBest()
print(results[1])
