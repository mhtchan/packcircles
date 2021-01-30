# packcircles
A pure Python implementation of the circle packing algorithm detailed in Wang et al. (2006). Visualization of large hierarchical data by circle packing. *Proc of the SIGCHI*, 517-520.

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
