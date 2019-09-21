# Project Gutenberg Toolkit

## Overview

## Synopsis

* Set `PGTK_HOME`. In `.bash_profile` enter:
  * `export PGTK_HOME="/where/you/put/pgtk"`
* Link `pgtk` in `/usr/local/bin`.
* Run `pgtk` in your working directory.
* To get started using pgtk, you need to download Gutenberg's RDF catalog and import it into the local database. Do:
   * `pgtk download-cache` or `pgtk dc`
* Then:
   * `pgtk populate-database` or `pgtk pd`