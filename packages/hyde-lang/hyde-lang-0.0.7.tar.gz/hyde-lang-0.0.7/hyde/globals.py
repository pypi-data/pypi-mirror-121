from hyde.primitives.array import Array as HydeArray
from hyde.primitives.http import BasicHttpRequestHandler as HydeBasicHttpRequestHandler
from hyde.primitives.map import Map as HydeMap
from hyde.hyde_callable import HydeCallable


class Globals:
    class GlobalHydeCallable(HydeCallable):
        def __str__(self):
            return f'<fn {self.__name__}>'


    class Array(GlobalHydeCallable):
        arity = 1

        def call(self, _interpreter, arguments):
            size = int(arguments[0])

            return HydeArray(size)


    class BasicHttpRequestHandler(GlobalHydeCallable):
        arity = 1

        def call(self, _interpreter, arguments):
            request_attrs = arguments[0]

            return HydeBasicHttpRequestHandler(request_attrs)

    class clock(GlobalHydeCallable):
        from time import time

        arity = 0

        def call(self, _interpreter, _arguments):
            return float(round(self.time() * 1000))

    
    class Map(GlobalHydeCallable):
        arity = 0

        def call(self, _interpreter, _arguments):
            return HydeMap()

    
    class toString(GlobalHydeCallable):
        arity = 1

        def call(self, _interpreter, arguments):
            object = arguments[0]

            return str(object)


    GLOBAL_FUNCTIONS = [
        Array,
        BasicHttpRequestHandler,
        clock,
        Map,
        toString
    ]

    @classmethod
    def define(cls, environment):
        for fn in cls.GLOBAL_FUNCTIONS:
            environment.define(fn.__name__, fn())