#!/usr/bin/env python3
        
class GO:
    def __init__(self, filename):
        self.categories = {
        }
        self.relations = {
            'is_a': GO_relation({'id': ['is_a'],
                                 'name': ['is_a'],
                                 'is_transitive': [True]}),
            'has_part': GO_relation({'id': ['has_part'],
                                 'name': ['has_part'],
                                 'is_transitive': [False]}),
            'my_rel': GO_relation({'id': ['my_rel'],
                                 'name': ['my_rel'],
                                 'is_transitive': [False]})
            
        }
        self._read(filename)
        self._init_relations()
    
    def _read(self, filename):
        with open(filename, 'r') as f:
            section = ''
            attributes = {}
            for line in f:
                line = line.strip()
                if line == '':
                    if section == 'Term':
                        category = GO_category(attributes)
                        self.categories[category.id] = category
                    elif section == 'Typedef':
                        relation = GO_relation(attributes)
                        self.relations[relation.id] = relation
                    attributes.clear()
                    section = ''
                elif line.startswith('[') and line.endswith(']'):
                    section = line[1:-1]
                else:
                    k, v = line.split(': ', 1)
                    try:
                        attributes[k].append(v)
                    except KeyError:
                        attributes[k] = [ v ]

    def _init_relations(self):
        is_a = self.relations['is_a']
        has_part = self.relations['part_of']
        my_rel = self.relations['is_a'] or self.relations['part_of']
        for go, category in self.categories.items():
            if 'is_a' in category.others:
                for value in category.others['is_a']:
                    other_go, _ = value.split(' ! ', 1)
                    other_category = self.categories[other_go]
                    is_a.add_pair(category, other_category)
                del category.others['is_a']
            if 'has_part' in category.others:
                for value in category.others['has_part']:
                    other_go, _ = value.split(' ! ', 1)
                    other_category = self.categories[other_go]
                    is_a.add_pair(category, other_category)
                del category.others['has_part']
            if 'my_rel' in category.others:
                for value in category.others['my_rel']:
                    other_go, _ = value.split(' ! ', 1)
                    other_category = self.categories[other_go]
                    is_a.add_pair(category, other_category)
                del category.others['my_rel']
            if 'relationship' in category.others:
                for value in category.others['relationship']:
                    rel, other_go, _ = value.split(' ', 2)
                    other_category = self.categories[other_go]
                    self.relations[rel].add_pair(category, other_category)
                del category.others['relationship']
    
     
def _pop_single_value(k, values):
    if len(values[k]) != 1:
        raise ValueError('There must be exactly one element in values.')
    value = values[k][0]
    del values[k]
    return value


class GO_category:
    def __init__(self, attributes):
        self.id = _pop_single_value('id', attributes)
        self.name = _pop_single_value('name', attributes)
        self.defination = _pop_single_value('def', attributes)
        self.others = attributes

    def __repr__(self):
        return '{} ({})'.format(self.id, self.name)

    def __lt__(self, other):
        return self.id < other.id

    
class GO_relation:
    def __init__(self, attributes):
        attributes = attributes.copy()
        self.id = _pop_single_value('id', attributes)
        self.name = _pop_single_value('name', attributes)
        self.is_transitive = ('is_transitive' in attributes and
                              str(_pop_single_value('is_transitive', attributes)).lower() != 'false')
        self.others = attributes
        self.pairs = {}
        
    def __repr__(self):
        return '<{}>'.format(self.id)
    def trans_property(category1,category2):
        if 'is_a' in category1.others:
            for value in category1.others['is_a']:
                category_t_add, _ = value.split(' ! ', 1)
                other_category = self.categories[category2]
                is_a.add_pair(category2, category_to_add)
    def add_pair(self, category1, category2):
        if not isinstance(category1, GO_category):
            raise TypeError('category1 must be a GO_category.')
        if not isinstance(category2, GO_category):
            raise TypeError('category2 must be a GO_category.')
        try:
            self.pairs[category1].add(category2)
        except KeyError:
            self.pairs[category1] = { category2 }

    def __contains__(self, pair):
        if (not isinstance(pair, tuple) or len(pair) != 2 or
            not isinstance(pair[0], GO_category) or not isinstance(pair[1], GO_category)):
            raise TypeError('pair must be a tuple of two GO_category objects.')
        try:
            return pair[1] in self.pairs[pair[0]]
        except KeyError:
            return False

    def __getitem__(self, category):
        if not isinstance(category, GO_category):
            raise TypeError('category must be a GO_category.')
        try:
            return self.pairs[category]
        except KeyError:
            return set()
        
    def __iter__(self):
        for category1 in self.pairs:
            for category2 in self.pairs[category1]:
                yield category1, category2

    def copy(self):
        cls = self.__class__
        result = cls.__new__(cls)
        attributes = {'id': [self.id], 'name': [self.name], 'is_transitive': [self.is_transitive]}
        attributes.update(self.others)
        result.__init__(attributes)
        for category1, category2 in self:
            result.add_pair(category1, category2)
        return result

    def __eq__(self, other):
        return (self.id == other.id and
                self.name == other.name and
                self.is_transitive == other.is_transitive and
                self.others == other.others and
                self.pairs == other.pairs)
