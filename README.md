# About GBT
GBT (Geweldige Bepaling Tracés) is a program for pathfinding through BGT data.
It supports many parameters, like costs per layer and maximum path length.
The path is found on a grid, the granularity of which can be changed at will.
BGT data gets automatically downloaded from `pdok.nl`.

# Using the pathfinder
Use `python3 -m path-finding` to run the project.
On the first run, this will create a `config.json` file, in which you can provide the weights used during pathfinding.
For each layer property a grid tile has, their weight will be added to the total cost of the path.
Unregistered tiles are those without any layer properties.

The pathfinder uses RDC (RijksDriehoeksCoördinaten) as its coordinate system.
To find a path from coordinate `xa,ya` to `xb,yb`, run `python -m path-finding xa,ya xb,yb`.
If a path is found, the output will be written to `output/path.geojson`.

Data files get cached.
This means that running the pathfinder again on the same grid -- with different parameters -- is faster.

## Options
### General
- `--clear-cache`: remove the cached files stored in `.bgt_data`, `.gpkg_data` and `.tiff_data` before running the pathfinder.
- `-o <s>`, `--output-name <s>`: place the output in the file `output/<s>.geojson`. Default: `path`.

### Path
- `-c <x>`, `--path-cost <x>`: cost per meter of path. Default: `0.0`. _Note: the higher the cost, the stronger the A* heuristic will be._
- `-l <x>`, `--max-length <x>`: the maximum length in meters that the path may have. Default: unlimited.
- `--padding x`: how much padding to add to each side of the grid, as a factor of the grid size. This allows the path to backtrack a bit. Default: `0.1`. _Note: without padding, the grid has the path's start and end points as its corners._
- `--resolution <x>`: how granular the grid is, i.e. `<x>` grid units per meter. Default: `1.0`.

### Multiple paths
- `-p <n>`, `--paths <n>`: how many paths to generate. Paths will be placed in `output/path_<i>.geojson`. Default: `1`. _Note: on its own, this option is useless. Use the options below to get meaningfully different paths._
- `-m <x>`, `--existing-path-multiplier <x>`: factor with which the tile costs on existing paths increase. This helps to avoid existing paths. Default: `1.0`.
- `-r <x>`, `--existing-path-radius <x>`: meters of influence that the existing path multiplier has. The factor with which the tile costs increase, is linearly interpolated within this radius. Default: `0.0`.
- `--partitions <n>`: split the first path into evenly-sized parts. The second path will be generated via the endpoints of each part. Default: `1`. _Note: currently, this option can only be used when the amount of paths to generate is 2._
