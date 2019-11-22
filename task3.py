from ChromosomeRegex import validate_regex
from Area import Area

AREAS = ['islands', 'shores', 'shelves', 'seas']


def read_areas():
    result = {}
    for area in AREAS:
        with open('results/' + area + '.bed') as file:
            for line in file.readlines():
                split_line = line.split('\t')
                name = split_line[0]
                if name not in result:
                    result[name] = []
                result[name].append((Area(int(split_line[1]), int(split_line[2]), area)))
    for key in result:
        result[key] = sorted(result[key], key=lambda x: x.start)
    return result


def find_dna_methylation(methylation_area, chromosome_areas):
    middle = methylation_area.middle()
    for i, area in enumerate(chromosome_areas):
        if area.contains(middle):
            return area.name, i
    raise ValueError


def task3():
    methylations = {}
    with open('data/dnaMethylation.bed') as islands_input_file:
        for line in islands_input_file.readlines():
            split_line = line.split('\t')
            name = split_line[0]
            if validate_regex(name):
                if name not in methylations:
                    methylations[name] = []
                methylations[name].append(Area(int(split_line[1]), int(split_line[2]) - 1))

    areas = read_areas()
    counter = {}
    for area in AREAS:
        counter[area] = 0
    for key in methylations:
        methylations_chr = sorted(methylations[key], key=lambda x: x.start)
        i = 0
        for meth_key in methylations_chr:
            area_name, j = find_dna_methylation(meth_key, areas[key][i::])
            counter[area_name] += 1
            i += j

        print(counter)
