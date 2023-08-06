from hyde.hyde_callable import HydeCallable
from hyde.hyde_instance import HydeInstance, HydeInstanceError
from hyde.primitives.array import Array


class Map(HydeInstance):
    name = "Map"

    class MapFunction(HydeCallable):
        def __init__(self, map, token):
            self.map   = map
            self.token = token


    class Get(MapFunction):
        arity = 1

        def call(self, _interpreter, arguments):
            key = arguments[0]

            return self.map.value_map.get(key)

        
    class Set(MapFunction):
        arity = 2

        def call(self, _interpreter, arguments):
            key = arguments[0]
            value = arguments[1]
            self.map.value_map[key] = value

            return value

        
    class Keys(MapFunction):
        arity = 0
        
        def call(self, _interpreter, _arguments):
            array = Array(len(self.map.value_map))
            array.elements = list(self.map.value_map.keys())

            return array

    class Merge(MapFunction):
        arity = 1

        def call(self, _interpreter, arguments):
            other = arguments[0]
            new_map = Map()
            new_map.value_map = self.map.value_map
            new_map.value_map.update(other.value_map)

            return new_map


    def __init__(self):
        self.value_map = {}

    def get(self, name):
        if name.lexeme == 'get':
            return Map.Get(self, name)
        elif name.lexeme == 'set':
            return Map.Set(self, name)
        elif name.lexeme == 'keys':
            return Map.Keys(self, name)
        elif name.lexeme == 'merge':
            return Map.Merge(self, name)

        raise HydeInstanceError(name, f'Undefined property {name.lexeme} for {self.name} instance.')

    def set(self, name, value):
        self.value_map[name.lexeme] = value

        return value

    def __str__(self):
        return str(self.value_map)