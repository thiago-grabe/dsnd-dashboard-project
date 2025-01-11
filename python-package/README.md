# Employee Events

This repository contains the Employee Events package, a Python package for data scientists. The package contains code for working with employee event data, including functions for loading and cleaning the data, computing statistics, and creating visualizations.

## Installation

To install the Employee Events package, run the following command in your terminal:

    uv install employee-events

This will install the package and its dependencies.

## Project Tree

The project tree for the Employee Events package is as follows:

    employee-events/
    employee/
        __init__.py
        employee.py
        query_base.py
        sql_execution.py
        team.py
    notes/
        __init__.py
        notes.py
    data/
        employee_events.db
    tests/
        test_employee_events.py
    README.md
    setup.py
    uv.lock

## Usage

To use the Employee Events package, import it and call the functions you need. For example:

    from employee_events.employee import Employee

    employee = Employee()
    names = employee.names()
    print(names)

This will load the employee event data and print the first few rows of the data.
