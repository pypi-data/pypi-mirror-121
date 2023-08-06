# The PyStar 
![PyStar Logo](./assets/logo.png)

PyStar is a user-friendly application for anyone who would like to learn simulations. It shows relevant quantities for each of modeling system. 
Explore and enjoy.

# Requirements
This application uses [ESPResSo package](https://espressomd.org/) as a backend. Thus, it is essential to get compiled your package. The rest can be installed via 
`pip3 install -r requirements.txt`

# Introduction
PyStar is an application to learn about simulations. The application can provide you variety of use cases: starting from demonstration concents of model/methods to new students and ending by comprehensive university course about modeling.

The application is written in user-friendly way. You can pull slicers, toggle checkboxes drag and drop particles to tune your own simulation setup.


# QuickStart
```python
import espressomd
from simlearn import PyStar
PyStar.run()
```

# Future Content of the Software
* Introduce new ensembles: NpT, RE
* Introduce new systems: chains, gels, combs..
* ...

# The team
PyStar is currently maintained by [Alexander D. Kazakov](https://github.com/AlexanderDKazakov/) with contributions coming from talented individuals in various forms and means. A non-exhaustive but growing list needs to mention: Tabea G. Langen, Pascal Hebbeker, Peter Kosovan, Filip Uhlík, Lucie Nová.
