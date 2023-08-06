#########################################
Hb Bank Statement Machine Learning Module
#########################################

This module add a machine learning on the **account.bank.statement** to predict
the party and the account to use for a new line.

*******
Install
*******

Dependencies for ArchLinux

.. code-block::

    sudo pacman -S cairo pkgconf gobject-introspection


Dependencies for debian


.. code-block::

    sudo apt-get install libcairo2-dev libgirepository1.0-dev


Install the package

.. code-block::

    # installs python deps
    pip install -e .
    # createdb postgresql database
    createdb bank_stmt_ml
    # initialize database
    trytond-admin -c trytond-dev.conf -d bank_stmt_ml --all
    # install module hb_tryton
    trytond-admin -c trytond-dev.conf -d bank_stmt_ml -u hb_bank_statement_machine_learning --activate-dependencies

*********
Low level
*********

The machine learning is added on the **acount.statement.line**, the machine learning is based on the field number on the line,
this field must be filled

.. code-block::

    pool = Pool()
    Line = pool.get('account.statement.line')
    line = Line()
    line.number = 'My number'
    line.set_account_and_party_from_ml()
    assert line.party
    assert line.account

*****
Usage
*****

An on_change method on the field number exist to predict the fields party and account from the interface

*********
CHANGELOG
*********

0.1.0 (2021-09-28)
------------------

* Implemented the machine learning
* Implemented the on change method on the fields number
