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
    shore = next_area_beginning(Area(BED_FIRST_INDEX, first_island_start - 1))
    if shore.start == BED_FIRST_INDEX:
        return ChromosomeAreas(shores=[shore])
    shelf = next_area_beginning(Area(BED_FIRST_INDEX, shore.start - 1))
    if shelf.start == BED_FIRST_INDEX:
        return ChromosomeAreas(shores=[shore], shelves=[shelf])
    return ChromosomeAreas(shores=[shore], shelves=[shelf], seas=[Area(BED_FIRST_INDEX, shelf.start - 1)])


def next_area_beginning(area):
    if len(area) < BORDER:
        return area
    return Area(area.end - BORDER + 1, area.end)


def find_ending(last_island_end, size):
    shore = next_area_ending(Area(last_island_end + 1, size - 1))
    if shore.end == size:
        return ChromosomeAreas(shores=[shore])
    shelf = next_area_ending(Area(shore.end + 1, size - 1))
    if shelf.end == size:
        return ChromosomeAreas(shores=[shore], shelves=[shelf])
    return ChromosomeAreas(shores=[shore], shelves=[shelf], seas=[Area(shelf.end + 1, size - 1)])


def next_area_ending(area):
    if len(area) < BORDER:
        return area
    return Area(area.start, area.start + BORDER - 1)


def find(between_islands):
    shores = next_areas(between_islands)
    if len(shores) == 1:
        return ChromosomeAreas(shores=shores)
    shelves = next_areas(Area(shores[0].end + 1, shores[1].start - 1))
    if len(shelves) == 1:
        return ChromosomeAreas(shores=shores, shelves=shelves)
    return ChromosomeAreas(shores=shores, shelves=shelves, seas=[Area(shelves[0].end + 1, shelves[1].start - 1)])


def next_areas(area):
    if len(area) <= 2 * BORDER:
        return [area]
    return [Area(area.start, area.start + BORDER - 1), Area(area.end - BORDER + 1, area.end)]


def write_to_file(file, areas, chromosome):
    for area in areas:
        file.write('%s\t%d\t%d\n' % (chromosome, area.start, area.end + 1))


def task1():
    chromosomes = {}
    with open('data/cpgIslandExt.txt') as islands_input_file:
        for line in islands_input_file.readlines():
            split_line = line.split('\t')
            name = split_line[1]
            if validate_regex(name):
                if name not in chromosomes:
                    chromosomes[name] = ChromosomeAreas()
                chromosomes[name].areas['islands'].append(Area(int(split_line[2]), int(split_line[3]) - 1))

    sizes = read_sizes()

    files = {}
    for area in AREAS:
        files[area] = open('results/' + area + '.bed', 'w+')
    for key in chromosomes:
        islands = sorted(chromosomes[key].areas['islands'], key=lambda x: x.start)
        beginning = find_beginning(islands[0].start)
        chromosomes[key].add(beginning)
        for i in range(0, len(islands) - 1):
            areas = find(Area(islands[i].end + 1, islands[i + 1].start - 1))
            chromosomes[key].add(areas)
        ending = find_ending(islands[len(islands) - 1].end, sizes[key])
        chromosomes[key].add(ending)
        for file_key in files:
            write_to_file(files[file_key], chromosomes[key].areas[file_key], key)
    for key in files:
        files[key].close()

