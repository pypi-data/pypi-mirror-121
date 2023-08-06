# snakist

### Why 🐍 case?

According to [PEP8](https://www.python.org/dev/peps/pep-0008/), in Python, it is recommended not to use 🐪 case for variable or function names. 

However, it is common for programmers who have come from other languages to write variable names or function names in camel case. (Languages such as Java recommend this.) 

I don't care what other people do. But I want to follow the naming convention of PEP8 and write code consistently. 

There are often libraries that violate this rule. If someone else made a module like that, you should use it as it was made, but I don't want it. Because I'm a **Snakeist**.

So I made a simple logic to follow my own rules.

### Install

```
pip install snakist
```

### Usage

```
import module_has_camel

module_has_camel = camelMethod() # I don't wanna use camel case

from snakist import snake

module_has_camel = snake(module_has_camel) # ─┐
snake(module_has_camel) # ────────────────────┴ Either style doesn't matter.

module_has_camel.camel_method()
```

It can be used for all instances, not just modules.

```
import module_has_camel

instance = module_has_camel.ClassHasCamel()

instance.camelMethod()

instance = snake(instnace)

instance.camel_method()
```

### Limitation

This method works by adding a descriptor to the class rather than changing the instance. That is, it affects not only the instance, but the class itself. I wrote this because I thought it was simple, but if there is a good way, it would be good if you let me know.

And if snake is applied, there is no linting. More precisely, there is no linting for the snake case attribute. (The method of the original class can be linted.)