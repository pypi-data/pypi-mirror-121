
# mdio

A Python library to read, write, and manipulate molecular dynamics (MD) trajectory files.

`mdio` is designed to provide basic MD file I/O capabilities. It's not supposed to replace great packages like [mdtraj](www.mdtraj.org) and [mdanalysis](www.mdanalysis.org), but is a lighter weight alternative when all you need is basic MD trajectory file I/O and nothing much more.

For example, the following script would read in a Gromacs `.xtc` format trajectory file, strip it of water molecules, correct molecule coordinates split up by periodic boundary condition artifacts, least-squares fit each snaphot to the first, and then write out the new coordinates in Amber netcdf (`.nc`) format:


```python
import mdio

topfile = '../test/examples/test.gro'
trajfile = '../test/examples/test.xtc'
outfile = 'protein.nc'

traj = mdio.load(trajfile, top=topfile, selection='not water')
traj = traj.make_whole()
traj = traj.fitted_to(traj[0])
traj.save(outfile)
```

## Installation

Easiest via `pip`. You need `numpy` and `cython` pre-installed:
```
% pip install numpy cython
% pip install mdio
```

## User Guide

### Loading data

`mdio` can load data from a variety of file formats: Gromacs (`.xtc` and `.gro`), NAMD/CHARMM (`.dcd`), AMBER (`.nc`, `.mdcrd`, `.rst`), and PDB (`.pdb`). `mdio` auto-detects file formats, so although it may be useful to use the standard file extensions, you don't have to - `mdio` will happily load an AMBER netcdf file that has the extension `.traj` (or even `.xtc`!).


```python
t = mdio.load('../test/examples/test.nc')
print(t)
```

    mdio.Trajectory with 10 frames, 892 atoms and box info.


Alternative ways of reading files are supported:


```python
f = mdio.open('../test/examples/test.nc', top='../test/examples/test.pdb')
t2 = f.read()
f.close()
print(t2)
```

    mdio.Trajectory with 10 frames, 892 atoms and box info.


Or using a context manager, and in a frame-by-frame way:


```python
with mdio.open('../test/examples/test.dcd') as f:
    frames = []
    frame = f.read_frame()
    while frame is not None:
        frames.append(frame)
        frame = f.read_frame()
t3 = mdio.Trajectory(frames)
print(t3)
```

    mdio.Trajectory with 10 frames, 892 atoms and box info.


You can create an `mdio` trajectory object from a suitably-shaped numpy array. `mdio` assumes the numbers in the array are in nanometers.


```python
import numpy as np
xyz = np.random.random((120, 55, 3))
t4 = mdio.Trajectory(xyz)
print(t4)
```

    mdio.Trajectory with 120 frames, and 55 atoms.


### Saving data

Trajectory files can also be written in a variety of ways. The required format is inferred from the filename extension, so unlike for file reading, this must be appropriate.


```python
# a) Using the save() method of a trajectory object:
t.save('test.nc')

# b) Using mopen():
with mdio.open('test2.dcd', "w") as f:
    f.write(t)

# c) Frame-by-frame:
f =  mdio.open('test3.xtc', "w")
for frame in t.frames():
    f.write_frame(frame)
f.close()
```

### Manipulating trajectories

#### a) Frame-wise:

Trajectories can be sliced and concatenated/appended (if they are compatible):


```python
t5 = t[2:9:3] + t2
t5 += t3
print(t5)
```

    mdio.Trajectory with 23 frames, 892 atoms and box info.


#### b) Atom-wise:

Trajectories with selected subsets of atoms can be created. There are two methods for doing this. One is to specify a list of atom indices:


```python
t6 = t.select([0, 1, 3, 5, 23, 34])
print(t6)
```

    mdio.Trajectory with 10 frames, 6 atoms and box info.


The other is to specify a selection string, which uses a syntax very similar to that used by `mdtraj`, see [here](http://mdtraj.org/latest/atom_selection.html):


```python
t7 = t2.select('name CA')
print(t7)
```

    mdio.Trajectory with 10 frames, 58 atoms and box info.


#### c) Coordinate-wise:

It is not the purpose of `mdio` to provide a rich variety of trajectory analysis facilities, but a few common functions are implemented. Firstly coordinates can be least-squares fitted to reference structures and the fitting can be weighted:


```python
# a) Simple fit
t8 = t.fitted_to(t[0])

# b) Mass-weighted fit of t2 to the 6th frame in trajectory t3:
weights = [atom.element.mass for atom in t2.topology.atoms]
t9 = t2.fitted_to(t3[5], weights=weights)

# c) Use just residue 1 for the fit:
weights = np.zeros(t2.n_atoms)
weights[t2.topology.select('residue 1')] = 1.0
t10 = t2.fitted_to(t3[5], weights=weights)
```

Secondly some PBC-related transformations are supported. 

* `packed_around()` transforms coordinates so they lie within the unit cell whose centre would be the centre of geometry of the selected atoms. 
* `make_whole()` corrects for molecules split by PBC imaging; this uses bond information generated from analysis of the topology file, so this needs to have 'good' geometry.


```python
t11 = t2.packed_around('residue 3')
t12 = t11.make_whole()
```

Finally RMSDs can be calculated:


```python
r2 = t2.rmsd_from(t3[6])
print(r2)
```

    [0.09093863981724826, 0.07614511939046421, 0.07949020859896917, 0.07497944478603998, 0.06590847615210413, 0.051843638106744715, 5.960464477539063e-08, 0.07091305468398602, 0.07106069413686344, 0.08153553252567688]


### NGLViewer compatibility

`mdio.Trajectory` objects look enough like the ones generated by MDTraj that they can be viewed in Jupyter notebooks with [nglview](https://github.com/arose/nglview) using the `show_mdtraj()` function.

### Author:

Charlie Laughton charles.laughton@nottingham.ac.uk

### License:

BSD 3-clause
