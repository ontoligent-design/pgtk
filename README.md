# Project Gutenberg Toolkit

## Overview

`pgtk` is a command line utility, written in Python, to make it easier to search and acquire resources from Project Gutenberg.

It has the following commands:

```
NAME
    pgtk

SYNOPSIS
    pgtk COMMAND

COMMANDS
    COMMAND is one of the following:

     getcat
       Download RDF catalog from Project Gutenburg

     mkdb
       Create db with downloaded RDF data

     query
       Run a query to the catalog table in the database. Don't use a LIMIT clause; instead pass argument.

     search
       Search catalog by fields:  title (ti), creators (cr), and subjects (su). Also: languages (la) defaults to 'EN', types (ty) defaults to 'TEXT', and formats (fo) defaults to '%TEXT/PLAIN%'.

     getpubs
       Download epubs from a list of files generated from a search

     rmcat
       Remove RDF cache from file system
 ```

To install it, do something like this:

* Clone this repo somewhere on your system.
* Create a directory to put `pgtk` resources, i.e. the executible file `pgtk` and the local database that `pgtk` needs to create.
* Set `PGTK_HOME` to this directory. So, in `.bash_profile` enter:
  * `export PGTK_HOME="/where/you/put/pgtk"`
* Run `chmod +x pgtk` to make the file executible and then symlink to an alias in `/usr/local/bin`. Or, you create an alias statement for it in your bash profile to the file.
* Source your bash profile file.
* Your are ready to run `pgtk`.

To use it, do these things:

* Get into a working directory where you want to download content.
* You will first need to download Gutenberg's RDF catalog and import it into the local database. Do this:
   * `pgtk getcat`
* Then:
   * `pgtk mkdir`
   
To find and download content, follow this pattern:
* Search for something
  * `pgtk search au 'Austen'`
* View results
```
rca2t$ pgtk search --cr "austen"
158|AUSTEN, JANE|EMMA|https://www.gutenberg.org/ebooks/158.txt.utf-8
946|AUSTEN, JANE|LADY SUSAN|https://www.gutenberg.org/ebooks/946.txt.utf-8
1212|AUSTEN, JANE|LOVE AND FREINDSHIP [SIC]|https://www.gutenberg.org/ebooks/1212.txt.utf-8
141|AUSTEN, JANE|MANSFIELD PARK|https://www.gutenberg.org/ebooks/141.txt.utf-8
121|AUSTEN, JANE|NORTHANGER ABBEY|https://www.gutenberg.org/ebooks/121.txt.utf-8
105|AUSTEN, JANE|PERSUASION|https://www.gutenberg.org/ebooks/105.txt.utf-8
1342|AUSTEN, JANE|PRIDE AND PREJUDICE|https://www.gutenberg.org/ebooks/1342.txt.utf-8
42671|AUSTEN, JANE|PRIDE AND PREJUDICE|https://www.gutenberg.org/ebooks/42671.txt.utf-8
161|AUSTEN, JANE|SENSE AND SENSIBILITY|https://www.gutenberg.org/ebooks/161.txt.utf-8
21839|AUSTEN, JANE|SENSE AND SENSIBILITY|https://www.gutenberg.org/ebooks/21839.txt.utf-8
31100|AUSTEN, JANE|THE COMPLETE PROJECT GUTENBERG WORKS OF JANE AUSTEN A LINKED INDEX OF ALL PG EDITIONS OF JANE AUSTEN|https://www.gutenberg.org/ebooks/31100.txt.utf-8
42078|AUSTEN, JANE|THE LETTERS OF JANE AUSTEN SELECTED FROM THE COMPILATION OF HER GREAT NEPHEW, EDWARD, LORD BRADBOURNE|https://www.gutenberg.org/ebooks/42078.txt.utf-8
37431|AUSTEN, JANE MACKAYE, STEELE, MRS.|PRIDE AND PREJUDICE, A PLAY FOUNDED ON JANE AUSTEN'S NOVEL|https://www.gutenberg.org/ebooks/37431.txt.utf-8
33513|AUSTEN, SIDNEY|THE FRIGHTENED PLANET|https://www.gutenberg.org/ebooks/33513.txt.utf-8
17797|AUSTEN-LEIGH, JAMES EDWARD|MEMOIR OF JANE AUSTEN|https://www.gutenberg.org/ebooks/17797.txt.utf-8
22536|AUSTEN-LEIGH, WILLIAM AUSTEN-LEIGH, RICHARD ARTHUR|JANE AUSTEN, HER LIFE AND LETTERS: A FAMILY RECORD|https://www.gutenberg.org/ebooks/22536.txt.utf-8
54010|HUBBACK, MRS. (CATHERINE-ANNE AUSTEN)|THE YOUNGER SISTER: A NOVEL, VOL. I.|https://www.gutenberg.org/ebooks/54010.txt.utf-8
54011|HUBBACK, MRS. (CATHERINE-ANNE AUSTEN)|THE YOUNGER SISTER: A NOVEL, VOL. II.|https://www.gutenberg.org/ebooks/54011.txt.utf-8
54012|HUBBACK, MRS. (CATHERINE-ANNE AUSTEN)|THE YOUNGER SISTER: A NOVEL, VOL. III.|https://www.gutenberg.org/ebooks/54012.txt.utf-8
54066|HUBBACK, MRS. (CATHERINE-ANNE AUSTEN)|THE YOUNGER SISTER: A NOVEL, VOLUMES 1-3|https://www.gutenberg.org/ebooks/54066.txt.utf-8
39897|LAYARD, AUSTEN HENRY|DISCOVERIES AMONG THE RUINS OF NINEVEH AND BABYLON|https://www.gutenberg.org/ebooks/39897.txt.utf-8
# 21 items returned
```
* Adjust search
  * `pgtk search au 'Austen, J'`
* View results
```
 rca2t$ pgtk search --cr "Austen, J"
158|AUSTEN, JANE|EMMA|https://www.gutenberg.org/ebooks/158.txt.utf-8
946|AUSTEN, JANE|LADY SUSAN|https://www.gutenberg.org/ebooks/946.txt.utf-8
1212|AUSTEN, JANE|LOVE AND FREINDSHIP [SIC]|https://www.gutenberg.org/ebooks/1212.txt.utf-8
141|AUSTEN, JANE|MANSFIELD PARK|https://www.gutenberg.org/ebooks/141.txt.utf-8
121|AUSTEN, JANE|NORTHANGER ABBEY|https://www.gutenberg.org/ebooks/121.txt.utf-8
105|AUSTEN, JANE|PERSUASION|https://www.gutenberg.org/ebooks/105.txt.utf-8
1342|AUSTEN, JANE|PRIDE AND PREJUDICE|https://www.gutenberg.org/ebooks/1342.txt.utf-8
42671|AUSTEN, JANE|PRIDE AND PREJUDICE|https://www.gutenberg.org/ebooks/42671.txt.utf-8
161|AUSTEN, JANE|SENSE AND SENSIBILITY|https://www.gutenberg.org/ebooks/161.txt.utf-8
21839|AUSTEN, JANE|SENSE AND SENSIBILITY|https://www.gutenberg.org/ebooks/21839.txt.utf-8
31100|AUSTEN, JANE|THE COMPLETE PROJECT GUTENBERG WORKS OF JANE AUSTEN A LINKED INDEX OF ALL PG EDITIONS OF JANE AUSTEN|https://www.gutenberg.org/ebooks/31100.txt.utf-8
42078|AUSTEN, JANE|THE LETTERS OF JANE AUSTEN SELECTED FROM THE COMPILATION OF HER GREAT NEPHEW, EDWARD, LORD BRADBOURNE|https://www.gutenberg.org/ebooks/42078.txt.utf-8
37431|AUSTEN, JANE MACKAYE, STEELE, MRS.|PRIDE AND PREJUDICE, A PLAY FOUNDED ON JANE AUSTEN'S NOVEL|https://www.gutenberg.org/ebooks/37431.txt.utf-8
# 13 items returned
```
* Save results
  * `pgtk search --cr "Austen, J" > AUSTEN.txt`
  * Edit `AUSTEN.txt` if you'd like
* Download results
  * `pgtk getpubs AUSTEN.txt`
```
pgtk getpubs AUSTEN.txt
Downloading files to AUSTEN
158 AUSTEN_JANE_EMMA
946 AUSTEN_JANE_LADY_SUSAN
1212 AUSTEN_JANE_LOVE_AND_FREINDSHIP_SIC_
141 AUSTEN_JANE_MANSFIELD_PARK
121 AUSTEN_JANE_NORTHANGER_ABBEY
105 AUSTEN_JANE_PERSUASION
1342 AUSTEN_JANE_PRIDE_AND_PREJUDICE
42671 AUSTEN_JANE_PRIDE_AND_PREJUDICE
161 AUSTEN_JANE_SENSE_AND_SENSIBILITY
21839 AUSTEN_JANE_SENSE_AND_SENSIBILITY
31100 AUSTEN_JANE_THE_COMPLETE_PROJECT_GUTENBERG_WORKS_OF_JANE_AUSTEN_A_LINKED_INDEX_OF_ALL_PG_EDITIONS_OF_JANE_AUSTEN
42078 AUSTEN_JANE_THE_LETTERS_OF_JANE_AUSTEN_SELECTED_FROM_THE_COMPILATION_OF_HER_GREAT_NEPHEW_EDWARD_LORD_BRADBOURNE
37431 AUSTEN_JANE_MACKAYE_STEELE_MRS_PRIDE_AND_PREJUDICE_A_PLAY_FOUNDED_ON_JANE_AUSTEN_S_NOVEL
# # 13 items returned
```

