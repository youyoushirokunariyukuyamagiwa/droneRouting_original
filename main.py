import numpy as np
from matplotlib import pyplot

def arrow():
    fig = pyplot.figure()
    ax = fig.add_subplot(111)

    point = {
        'depo': [0, 0],
        'node1': [1273, 457],
        'node2': [922, 1011],
        'node3': [675, 1114],
        'node4': [1324, 472],
    }

    ax.plot(*point['depo'], 'o', color="blue")
    ax.plot(*point['node1'], 'o', color="red")
    ax.plot(*point['node2'], 'o', color="red")
    ax.plot(*point['node3'], 'o', color="red")
    ax.plot(*point['node4'], 'o', color="red")

    ax.annotate('', xy=point['node1'], xytext=point['depo'],
                arrowprops=dict(shrink=0, width=1, headwidth=8, 
                                headlength=10, connectionstyle='arc3',
                                facecolor='gray', edgecolor='gray')
               )
    ax.annotate('', xy=point['node4'], xytext=point['node1'],
                arrowprops=dict(shrink=0, width=1, headwidth=8, 
                                headlength=10, connectionstyle='arc3',
                                facecolor='gray', edgecolor='gray')
               )
    ax.annotate('', xy=point['node2'], xytext=point['node4'],
                arrowprops=dict(shrink=0, width=1, headwidth=8, 
                                headlength=10, connectionstyle='arc3',
                                facecolor='gray', edgecolor='gray')
               )
    ax.annotate('', xy=point['node3'], xytext=point['node2'],
                arrowprops=dict(shrink=0, width=1, headwidth=8, 
                                headlength=10, connectionstyle='arc3',
                                facecolor='gray', edgecolor='gray')
               )
    ax.annotate('', xy=point['depo'], xytext=point['node3'],
                arrowprops=dict(shrink=0, width=1, headwidth=8, 
                                headlength=10, connectionstyle='arc3',
                                facecolor='gray', edgecolor='gray')
               )

    ax.set_xlim([0, 1500])
    ax.set_ylim([0, 1500])

    pyplot.show()

if __name__ == "__main__":
    arrow()