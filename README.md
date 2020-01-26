# GENE Ontology

## Introduction

Understanding our genes e.g., what they do, which processes they are part of, and where the proteins they code for are found, is of utmost importance for many kinds of research, including bioinformatics. To facilitate this, the scientific community has developed *Gene
Ontology*, or just *GO*, which is an extensive database of
  * various properties a gene can have, and
  * information on how these properties relate to each other.
  
This python code reads in the Gene Ontology database in a suitable data structure and processes the data in certain ways. This code could be one of the first steps in creating a web based browser for Gene Ontology and related data resources.

The properties that a gene can have are called *GO categories*. In the data we will be working with, there are 47,385 different GO
categories. Each GO category has an `id`, e.g. `GO:0008150`, a more descriptive `name`, e.g. `biological_process`, and a few other
attributes.

How the GO categories relate to each other is captured in *relations* that are composed of *relationships*. There are a number of different relations, and the most important of these is the `is_a` relation. For example, the GO category with `id` equal to `GO:0000003` and `name` equal to `reproduction` forms a relationship in the `is_a` relation to `GO:0008150` (`biological_process`), i.e. `reproduction` `is_a ` `biological_process`. There are a number of other types of relations. Another example is `part_of`, where one of the relationships is `GO:0098687` (`chromosomal region`) is `part_of` `GO:0005694` (`chromosome`).

Mathematically speaking, a relationship is a pair of categories, and a relation is a set of relationships.

I implemented *invert* relation, e.g. creating the relation `has_part` from `part_of` by saying that category *a* `has_part` category *b* if category *b* is `part_of` category *a* (note that *a* and *b* swapped place).

I also demonstrated how to combine two relations, e.g. you can construct a new relation `my_rel` from `is_a`and `part_of` by saying that two categories are related with `my_rel` if they are related with at least one of the `is_a` or `part_of` relations.

Some relations are *transitive*, meaning that if *a* is related to *b*, and *b* is related to *c*, then *a* is also related to *c*. The `is_a` relation is transitive, e.g. we have the relationship `GO:0019953` (`sexual reproduction`) `is_a` `GO:0000003` (`reproduction`), and as we also have the relationship `GO:0000003` (`reproduction`) `is_a` `GO:0008150` (`biological_process`), we know that we have the relationship `GO:0019953` (`sexual reproduction`) `is_a` `GO:0008150` (`biological_process`). However these indirect relationships are not explicitly stated in the Gene Ontology database.

If you are interested, you can look at http://geneontology.org for more information.

## Materials

In addition to this document, two other files have been provided:
  * Go.obo file was downloaded from http://purl.obolibrary.org/obo/go.obo and is licensed under the
    [Creative Commons Attribution 4.0 International Public License][1]. Please see http://geneontology.org for more information.
  * The `GO.py` file contains code for parsing the `go.obo` file and storing the information using three classes defined in the `GO.py`
    file.
  * The file `test_GO.py` defines a number of functions that help testing the code in `GO.py`.

[1]: https://creativecommons.org/licenses/by/4.0/legalcode

## Notes

All this code should run with Python 3 on an ordinary PC or server. CPU and memory requirements should be modest.

Please provide us your code to solve the tasks the day before the interview so that we can familiarize ourselves with your solutions.
