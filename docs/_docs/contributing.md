---
title: Contribute
permalink: /docs/contribute/
---

## Necessary software and compatibility

The following software is necessary to be able to develop and test Codeconut:
- Python 3.5 or newer
- Python packages defined inside the "requirements.txt" in the repo-root
- Ruby 2.6 or newer
- Ceedling gem
- GNU compiler toolchain (MinGW for Windows users)
- Papyrus

The following software is optional (helpful for the development of the website):
- Jekyll gem
- GitHub Pages gem


## Coding style guides

Codeconut uses the **C/C++ style guide from Google** for C and C++ code.
Python code is written according to the **PEP8** guidelines.

Upon committing, the code is linted using **cppunit** in case of C/C++ code and **flake8** for Python code.


## Workflow

Codeconut is developed using the **test driven development** (TDD) methodology. This means that every new feature or fix should be covered by a test case.

A popular and recommended approach for test driven development is the **red - green - refactor** cycle.

No matter if your contribution implies a new feature or just a bug fix: Always check the UML diagrams to see, if changes are necessary. A specification that is consistent with the real code is not just helpful for new potential contributors - it's helpful to retain a good code quality and important in cases, where Codeconut will be used for safety-relevant applications.

Contributions that focus on improving the documentation and the UML diagrams are always welcome.


## Committing your work to the main branch

To contribute to Codeconut, create a fork and make the changes you are interested in. Upon making a pull request, your submitted code will be checked by the project maintainers.

While every contribution is greatly appreciated, open issues and feature requests have the highest priority for the community.