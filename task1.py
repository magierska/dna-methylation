from ChromosomeRegex import validate_regex
from Area import Area
from ChromosomeAreas import ChromosomeAreas

AREAS = ['islands', 'shores', 'shelves', 'seas']
BORDER = 2000
BED_FIRST_INDEX = 0


def read_sizes():
    sizes = {}
    with open('data/sizes.txt') as sizes_file:
        for line in sizes_file.readlines():
            split_line = line.split('\t')
            sizes[split_line[0]] = int(split_line[1])

    return sizes


def find_beginning(first_island_start):
    shore = next_area_beginning(Area(BED_FIRST_INDEX, first_island_start))
    if shore.start == BED_FIRST_INDEX:
        return ChromosomeAreas(shores=[shore])
    shelf = next_area_beginning(Area(BED_FIRST_INDEX, shore.start))
    if shelf.start == BED_FIRST_INDEX:
        return ChromosomeAreas(shores=[shore], shelves=[shelf])
    return ChromosomeAreas(shores=[shore], shelves=[shelf], seas=[Area(BED_FIRST_INDEX, shelf.start)])


def next_area_beginning(area):
    if len(area) < BORDER:
        return area
    return Area(area.end - BORDER, area.end)


def find_ending(last_island_end, size):
    shore = next_area_ending(Area(last_island_end, size))
    if shore.end == size:
        return ChromosomeAreas(shores=[shore])
    shelf = next_area_ending(Area(shore.end, size))
    if shelf.end == size:
        return ChromosomeAreas(shores=[shore], shelves=[shelf])
    return ChromosomeAreas(shores=[shore], shelves=[shelf], seas=[Area(shelf.end, size)])


def next_area_ending(area):
    if len(area) < BORDER:
        return area
    return Area(area.start, area.start + BORDER)


def find(between_islands):
    shores = next_areas(between_islands)
    if len(shores) == 1:
        return ChromosomeAreas(shores=shores)
    shelves = next_areas(Area(shores[0].end, shores[1].start))
    if len(shelves) == 1:
        return ChromosomeAreas(shores=shores, shelves=shelves)
    return ChromosomeAreas(shores=shores, shelves=shelves, seas=[Area(shelves[0].end, shelves[1].start)])


def next_areas(area):
    if len(area) <= 2 * BORDER:
        return [area]
    return [Area(area.start, area.start + BORDER), Area(area.end - BORDER, area.end)]


def write_to_file(file, areas, chromosome):
    for area in areas:
        file.write('%s\t%d\t%d\n' % (chromosome, area.start, area.end))


def task1():
    chromosomes = {}
    with open('data/cpgIslandExt.txt') as islands_input_file:
        for line in islands_input_file.readlines():
            split_line = line.split('\t')
            name = split_line[1]
            if validate_regex(name):
                if name not in chromosomes:
                    chromosomes[name] = ChromosomeAreas()
                chromosomes[name].areas['islands'].append(Area(int(split_line[2]), int(split_line[3])))

    sizes = read_sizes()

    files = {}
    for area in AREAS:
        files[area] = open('results/' + area + '.bed', 'w+')
    for key in chromosomes:
        islands = sorted(chromosomes[key].areas['islands'], key=lambda x: x.start)
        beginning = find_beginning(islands[0].start)
        chromosomes[key].add(beginning)
        for i in range(0, len(islands) - 1):
            areas = find(Area(islands[i].end, islands[i + 1].start))
            chromosomes[key].add(areas)
        ending = find_ending(islands[len(islands) - 1].end, sizes[key])
        chromosomes[key].add(ending)
        for file_key in files:
            write_to_file(files[file_key], chromosomes[key].areas[file_key], key)
    for key in files:
        files[key].close()

