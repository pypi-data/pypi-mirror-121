apportionpy
======

A Python package for apportioning seats to states based on population figures. 

Installation
------------

The ``apportionpy`` package works in Python 3. It is available on pypi and can be installed using pip.

    pip install apportionpy

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

Examples
--------

Apportioning seats using the Huntington-Hill method.

    import apportionpy.apportionment as ap

    seats = 10
    populations = [100, 120, 113, 199, 144]
    method = "adam" # adam, jefferson, webster, or hamilton

    method = ap.Apportion(seats=seats, populations=populations, method=method)
