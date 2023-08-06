apportionpy
======

A Python package for apportioning seats to states based on population figures. 

Installation
------------

The ``apportionpy`` package works in Python 3. It is available on pypi and can be installed using pip.

    pip install apportionpy

pypi link -> https://pypi.org/project/apportionpy/

Package structure
-----------------

* apportionpy

  * apportionment
  
  * methods

    * calculate_adam
    * calculate_hamilton
    * calculate_jefferson
    * calculate_webster
    * calculate_huntington_hill
    * calculate_equal_proportions
  
  * experimental
  
    * estimate_lowest_divisor
    * estimate_highest_divisor

Examples
--------

Apportioning seats using the Huntington-Hill method.

``` python
import apportionpy.apportionment as ap

# Amount of seats to apportion.
seats = 70

# Populations per state, respectively.
populations = [300500, 200000, 50000, 38000, 21500]

# Apportionment method to use in apportioning seats to states.
method = "adam" 

"""
Possible methods:
  - adam,
  - jefferson 
  - webster
  - hamilton
  - huntington hill
  - equal proportions
"""

result = ap.Apportion(seats=seats, populations=populations, method=method)

# print results
print(result.method)
print("initial fair shares", result.initial_fair_shares)
print("(final) fair shares", result.fair_shares)
print("initial quotas", result.initial_quotas)
print("final quotas", result.final_quotas)
print("initial divisor", result.initial_divisor)
print("modified divisor", result.modified_divisor)

"""
output:

adam
initial fair shares [35, 23, 6, 5, 3] 
(final) fair shares [34, 22, 6, 5, 3] 
initial quotas [34.48360655737705, 22.95081967213115, 5.7377049180327875, 4.360655737704918, 2.4672131147540983] 
final quotas [33.00113375210664, 21.964148919871306, 5.4910372299678265, 4.1731882947755485, 2.3611460088861658] 
initial divisor 8714.285714285714 
modified divisor 9105.747767857141
"""

```
