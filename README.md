# name-format

`name-format` is a compact Python library and CLI for normalising personal names.
It handles real-world edge cases including Irish O’/Ó prefixes, Mc/Mac patterns, initials,
hyphenated names, and particles such as de, van, or von.

The aim is consistency: one clean `full_name()` function in Python and a simple CLI interface.

---

## Features

- Irish prefixes:
    ó brien → O'Brien

- Mc/Mac handling:
    mcavoy → McAvoy

- Initials:
    a. → A.

- Hyphens & apostrophes preserved:
    mary-kate o'reilly → Mary-Kate O'Reilly

- Particles maintained when appropriate:
    seamus de valera → Seamus de Valera

- Accepts:
    - a single string containing both names, or
    - first/last names as separate arguments

---

## Installation (development)

    python3 -m pip install -e . --no-build-isolation

---

## Command-line usage

    python3 -m name_format.cli "ó brien"

Output:

    O'Brien

Separate arguments:

    python3 -m name_format.cli -f "mary-kate" -l "o'reilly"

---

## Python usage

    from name_format.core import full_name

    print(full_name("ó brien"))               # O'Brien
    print(full_name("mary-kate", "o'reilly")) # Mary-Kate O'Reilly

---

## Tests

Run the full suite:

    make dev-install
    make test

Tests cover:

- Irish O’/Ó handling
- Mc/Mac patterns
- Initial formatting
- Hyphenated names
- Apostrophes
- Particles
- CLI behaviour

---

## Project structure

    name-format/
    ├── name_format/
    │   ├── __init__.py
    │   ├── cli.py
    │   └── core.py
    ├── tests/
    ├── Makefile
    ├── pyproject.toml
    ├── requirements-dev.txt
    └── README.md

---

## Notes

Created as a practical exercise in:

- packaging (pyproject.toml)
- editable installs
- CLI entry points
- unit testing
- versioning
- Makefile automation

Simple, robust, and extendable.

---

## License

MIT License  
See `LICENSE` for details.
