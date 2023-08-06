# snakist

### Why 🐍 case?

According to [PEP8](https://www.python.org/dev/peps/pep-0008/), in Python, it is recommended not to use 🐪 case for variable or function names. 

However, it is common for programmers who have come from other languages to write variable names or function names in camel case. (Languages such as Java recommend this.) 

I don't care what other people do. But I want to follow the rules of PEP8 and write code consistently. 

There are often libraries that violate this rule. But t's cumbersome to statically modify the library or ask the developer to do so. 

So I made a simple logic to follow my own rules.

### Install

```
pip install snakist
```

### Usage

```
import module_have_camel

module_have_camel = camelMethod() # I don't wanna use camel case

from snakist import snake

module_have_camel = snake(module_have_camel)

# or

snake(module_have_camel)

module_have_camel.camel_method()
```

### Limitation

This method works by adding a descriptor to the class rather than changing the instance. That is, it affects not only the instance, but the class itself. I wrote this because I thought it was simple, but if there is a good way, it would be good if you let me know.
