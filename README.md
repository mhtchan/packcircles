# packcircles
A pure Python implementation of the circle packing algorithm detailed in Wang et al. (2006). Visualization of large hierarchical data by circle packing. *Proc of the SIGCHI*, 517-520.

<img src="https://raw.githubusercontent.com/mhtchan/packcircles/master/images/packing.gif" width="400" height="400">

# Installation
Using `pip`:
```
pip install packcircles
```
or directly using `setup.py`:
```
git clone https://github.com/mhtchan/packcircles.git
cd packcircles
python setup.py install
```

# Usage
The function `pack` takes an iterable of the radii of the circles to pack and returns a generator that yields the layout of each circle as tuples in the form `(x_coordinate, y_coordinate, radius)`.

# Example
```python
import packcircles as pc
circles = pc.pack([15,5,7,12])
print(list(circles))
## [(-15.579319782711305, 4.287939798231928, 15), (4.4206802172886945, 4.287939798231928, 5), (2.9206802172886945, -7.6179411015587295, 7), (20.647637933172685, -0.7801804930509242, 12)]
```

The layout in the gif at the top of the page can be generated by the following code:
```python
import packcircles as pc
import matplotlib.pyplot as plt
from matplotlib import colormaps
radii =  [28,12,51,26,10,16,24,25,59,11,29,40,16,11,10,26,39,16,48,36,28]
fig, ax = plt.subplots()
cmap = colormaps('coolwarm_r')
circles = pc.pack(radii)
for (x,y,radius) in circles:
    patch = plt.Circle(
        (x,y),
        radius,
        color=cmap(radius/max(radii)),
        alpha=0.65
    )
    ax.add_patch(patch)
fig.set_figheight(15)
fig.set_figwidth(15)
ax.set(xlim=(-150, 140), ylim=(-180, 170))
plt.axis('off')
plt.show()
```
