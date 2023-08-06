# hyde-lang ![pypi Badge](https://img.shields.io/pypi/v/hyde-lang)

Hyde is a language I created after following the guide from Robert Nystrom's book *[Crafting Interpreters](https://craftinginterpreters.com/)*.

Just like [the novel of the same name](https://en.wikipedia.org/wiki/Strange_Case_of_Dr_Jekyll_and_Mr_Hyde), where the evil Mr. Hyde is the antithesis of the benevolent Dr. Jekyll, this scripting language, Hyde, is the polar opposite, often masochistic, and downright hard-to-use alternative to Jekyll.

Hyde is a toy language written to prove that just because something can be done... Sometimes it's best not to.

Jekyll is truly a joy to use -- simply write articles in Markdown and your content is served easily and quickly. Because it's built on top of Ruby, you know it's made for developer happiness.

Hyde, on the other hand, is an evil, deviously hard-to-use alternative to Jekyll. It will punish you for using it. It is a scripting language written in the span of a few weeks, and none of its features are built for rendering large bodies of HTML. It has a spartan standard library, limited primitive types, and barely passable error handling.

## Demo

See a demo of Hyde in action [here](https://hyde-lang-demo.herokuapp.com/).

## Installation

Hyde is built on top of Python and requires Python 3.8 or higher to install.

Install via `pip`:

```sh
pip install hyde-lang
python -m setup.py
```

## Usage

After installation, using Hyde is simple:

```sh
hyde
```

Alternatively, you can write a `.hy` script to be executed:

```sh
hyde path/to/script.hy
```

### Syntax

Hyde has most of the same Lox syntax that is present in *[Crafting Interpreters](https://craftinginterpreters.com/)*. The grammar for Lox is available [here](https://craftinginterpreters.com/appendix-i.html). Therefore, only the differences between Lox and Hyde are highlighted here.

* New booleans:
  * `True`/`False`/`None` in Hyde (like Python) vs. `true`/`false`/`nil` in Lox (like Ruby).
* Comments are preceeded by `#` symbols, not `//` double slashes.
* New primitives -- `Array`, `Map`, and `BasicHttpRequestHandler`.
  * They can be instantiated directly like any other class -- i.e. `var array = Array(1);`
* A few native functions, with capacity to define and load others.
* `load` statements.
  * Pathing is reliant on Python's path resolution (all paths are relative to the location where the script or REPL was executed).
  * `loading` a file works on global scope *only*, no `load`ing within a class or function will result in strange behavior.

### Examples

An example of a Hyde function:
```
fun arrayAppend(array1, value) {
  var l = array1.length() + 1;

  var newArray = Array(l);

  for (var i = 0; i < l - 1; i = i + 1) {
    newArray.set(i, array1.get(i));
  }

  newArray.set(l - 1, value);
  
  return newArray;
}
```

Using Hyde as a webserver (from the demo):
```
load "lib/app.hy";
load "lib/router.hy";
load "lib/utils/html_generator.hy";

# Route loading
var router = Router();

# Template assignment
load "templates/_application_template.hy";
var applicationTemplate = _template();

# View loading into router
load "templates/index.html.hy";
var indexRenderer = _renderer();
router.defineRoute(indexRenderer, "/", "main");

load "templates/about.html.hy";
var aboutRenderer = _renderer();
router.defineRoute(aboutRenderer, "/about", "about");

# Assign router to app
var app = App();
app.assignRouter(router);

# Debug
app.router.printRoutes();

# Start the server!
app.serve();
```

A recursive function:

```
# sums all numbers between start and stop, adds to counter
fun sumBetween(start, stop, counter) {
  if (stop < start) {
    return counter;
  }

  return sumBetween(start, stop - 1, counter + stop);
}

var value = sumBetween(1, 10, 0);
print value; # 55.0
```

Closures:

```
fun makeCounter() {
  var i = 0;

  fun count() {
    i = i + 1;
    return i;
  }

  return count;
}

var counter = makeCounter();

var num1 = counter();
var num2 = counter();

print num1; # 1
print num2; # 2
```

## Tests

Hyde ships with its own test framework called `TestRunner`. You can execute the language tests via the `tests/main.hy` script:

```sh
hyde tests/main.hy
```

Running your own tests is simple with the included test `_template.hy` file, after which you can load your custom tests into a `TestRunner` instance via the `registerTestClass()` method.

**Note:** You need to define and register each individual test case within the test file as well. See the templates for instructions on how to use.

## Extras

* [A VS Code extension to enable syntax highlighting](https://github.com/ty-porter/hyde-lang-syntax) for your coding pleasure
  * Because why not?
  * This is not currently published, however you can build from source and install the raw VSIX.

## Contact

Tyler Porter

tyler.b.porter@gmail.com