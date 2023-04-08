#!/usr/bin/env python3

""" 7. Plotting a cube - Examples from http://scitools.org.uk/iris/
docs/latest/userguide """

# Matplotlib's pyplot basics
import matplotlib.pyplot as plt
plt.plot([1, 2, 2.5])
plt.show()

# 7.1.1. Interactive plot rendering
plt.interactive(True)
plt.plot([1, 2, 2.5])

print(plt.isinteractive())

plt.close()

plt.draw() # update changes
plt.interactive(False)# non-interactive mode

# 7.1.2. Saving a plot
plt.plot([1, 2, 2.5])
plt.savefig('plot123.png')

















