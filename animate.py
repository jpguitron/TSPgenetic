import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

def generateAnimation(lines, generations):
    x = [0,0]
    y = [0,0]
    fig, ax = plt.subplots()
    localLines = []

    for i in range(len(lines)):
        line, = ax.plot(x, y, color='k',linewidth=2.0)
        line.axes.axis([-120, -80, 10, 35])
        localLines.append(line)

    def update(num, lines):
        for i in range(len(lines[0])-1):
            x = [lines[num][i].lon,lines[num][i+1].lon]
            y = [lines[num][i].lat,lines[num][i+1].lat]
            localLines[i].set_data(x,y)
            
        x = [lines[num][0].lon,lines[num][len(lines[0])-1].lon]
        y = [lines[num][0].lat,lines[num][len(lines[0])-1].lat] 

        localLines[len(lines[0])-1].set_data(x,y)
        return localLines

    ani = animation.FuncAnimation(fig, update, generations, fargs=[lines],interval=50, blit=True, repeat=False)
    #ani.save('test.gif')
    plt.show()
