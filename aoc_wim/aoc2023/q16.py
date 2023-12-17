"""
--- Day 16: The Floor Will Be Lava ---
https://adventofcode.com/2023/day/16
"""
from aocd import data

from aoc_wim.zgrid import ZGrid


def part_a(z0, dz0):
    paths = []
    rays = [[(z0, dz0)]]
    seen = set()
    while rays:
        ray = rays[0]
        if len(ray) > 1 and ray[0] == ray[-1]:
            paths.append([z for z, dz in ray])
            del rays[0]
            continue
        z, dz = ray[-1]
        z += dz
        if (z, dz) in seen:
            paths.append([z for z, dz in ray])
            del rays[0]
            continue
        seen.add((z, dz))
        if z not in grid:
            paths.append([z for z, dz in ray])
            del rays[0]
            continue
        match grid[z], dz.real, dz.imag:
            case  ".", _, _: ray.append((z, dz))
            case  "-", _, 0: ray.append((z, dz))
            case  "|", 0, _: ray.append((z, dz))
            case  "/", _, 0: ray.append((z, grid.turn_left * dz))
            case  "/", 0, _: ray.append((z, grid.turn_right * dz))
            case "\\", _, 0: ray.append((z, grid.turn_right * dz))
            case "\\", 0, _: ray.append((z, grid.turn_left * dz))
            case "|", _, 0:
                paths.append([z for z, dz in ray])
                del rays[0]
                if z + grid.up in grid:
                    rays.append([(z, grid.up)])
                if z + grid.down in grid:
                    rays.append([(z, grid.down)])
            case "-", 0, _:
                paths.append([z for z, dz in ray])
                del rays[0]
                if z + grid.left in grid:
                    rays.append([(z, grid.left)])
                if z + grid.right in grid:
                    rays.append([(z, grid.right)])
    return len({z for z, dz in seen if z in grid})


grid = ZGrid(data)
print("answer_a:", part_a(z0=-1, dz0=1))

w, h = grid.width, grid.height
bs = []
for col in range(w):
    bs.append(part_a(z0=complex(col, -1j), dz0=grid.down))
    bs.append(part_a(z0=complex(col, h), dz0=grid.up))
for row in range(h):
    bs.append(part_a(z0=complex(-1, row), dz0=grid.right))
    bs.append(part_a(z0=complex(w, row), dz0=grid.left))
print("answer_b:", max(bs))
