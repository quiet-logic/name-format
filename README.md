# name-format

Robust personal-name formatter in Python.

Supports:
- Irish O'/Ó prefixes
- Mc/Mac rules
- Initials (A. B. etc)
- Hyphens and apostrophes
- Particles like `de`, `van`, `von` (when not first)

```python
from name_format import full_name

print(full_name("ó brien"))       # O'Brien
print(full_name("michael patrick o'sullivan"))  # Michael O'Sullivan