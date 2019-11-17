import pandas as pd

COLUMN_OF_INTEREST = 'TOTSQFT_EN'
COLUMN_TITLE = 'Square Feet of Home (thousands)'
COLUMN_MIN = 0
COLUMN_MAX = 10

df = pd.read_csv('recs2015_public_v4.csv')

from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import numpy as np

fig = plt.figure()
fig.set_figheight(7)
fig.set_figwidth(10)
ax = fig.add_subplot(111, projection='3d')
ax.set_title('Household Income vs. {}'.format(COLUMN_TITLE))
ax.view_init(30, 40)


def moneypy_to_dollars(moneypy_val):
    # See row 399 in the docs
    return {
        1: 10,
        2: 30,
        3: 50,
        4: 70,
        5: 90,
        6: 110,
        7: 130,
        8: 150,
    }[moneypy_val]

HOUSEHOLD_INCOME = [moneypy_to_dollars(c) for c in df['MONEYPY'] ]
NUMBER_OF_HOUSEHOLDS = df['NWEIGHT'] / 1000 / 1000

hist, xedges, yedges = np.histogram2d(HOUSEHOLD_INCOME,
    df[COLUMN_OF_INTEREST] / 1000,
    weights=NUMBER_OF_HOUSEHOLDS, 
    bins=(8, 20),
    range=[[10, 150],[COLUMN_MIN, COLUMN_MAX]])

# Construct arrays for the anchor positions of the 16 bars.
# Note: np.meshgrid gives arrays in (ny, nx) so we use 'F' to flatten xpos,
# ypos in column-major order. For numpy >= 1.7, we could instead call meshgrid
# with indexing='ij'.
xpos, ypos = np.meshgrid(xedges[:-1] + 0.25, yedges[:-1] + 0.25)
xpos = xpos.flatten('F')
ypos = ypos.flatten('F')
zpos = np.zeros_like(xpos)

# Construct arrays with the dimensions for the 16 bars.
dx = 0.5 * np.ones_like(zpos)
dy = dx.copy()
dz = hist.flatten()
ax.set_xlabel('Annual Household Income (thousands of dollars)')
ax.set_ylabel(COLUMN_TITLE)
ax.set_zlabel('Number of Households (millions)')

ax.bar3d(xpos, ypos, zpos, dx, dy, dz, color='orange', zsort='average')

import imutil
import time
filename = 'output_{}.png'.format(int(time.time()))
imutil.show(plt, filename=filename)
