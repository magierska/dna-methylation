class ChromosomeAreas:
    def __init__(self, islands=None, shores=None, shelves=None, seas=None):
        self.areas = {
            'islands': ChromosomeAreas.init_array(islands),
            'shores': ChromosomeAreas.init_array(shores),
            'shelves': ChromosomeAreas.init_array(shelves),
            'seas': ChromosomeAreas.init_array(seas)
        }

    @classmethod
    def init_array(cls, array):
        return [] if array is None else array

    def add(self, other):
        for key in self.areas:
            self.areas[key] += other.areas[key]
