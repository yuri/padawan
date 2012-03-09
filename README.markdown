
Padawan is a "training wheels" library for learning how to build database-driven
web applications. It is meant to be an educational tool and is designed
primarily with pegadogical goals in mind. It was written to be used in a database
course that aims to understand how a database fits within the context of a web
application without spending too much time on the elements of web development
that have little to do with databases. Padawan assumes that the web application
will be written in a subset of Python, by students with limited familiarity with
the language.

Padawan assumes use of CGI and MySQL, via Python's cgi and MySQLdb modules.

There are two main files: padawan.py and padawan. Each is described below.

## padawan.py

**padawan.py** provides a wrapper for those two modules, adding the following
features:

* Code can be written using just a subset of Python. In particular,
  the application can avoid use of methods (using only functions instead),
  "%" operator. Use of list subscripts can also be avoided, if desired.
* Common errors are checked more rigorously with additional (and friendlier)
  error messages.
* Values can be retrieved by field names rather than field positions.
* Additional functions are provided.

## padawan

**padawan** is a wrapper around the python executable that provides an additional
level of support, aiming to avoid "Internal Server Error" Messages.

## An example

Here is an example of a Padawan script. More complete examples are available in
the examples directory.

    #!/usr/bin/padawan
    print "Content-Type: text/html; encoding=utf8"
    print

    if not form_has_field("species") :
        print "A value for <b>species</b> specify you must!"
        exit()
        
    species = get_form_field_value("species")
    species = escape_string(species)

    query_template = """
    select * from species where species='%s';
    """

    query = fill_template(query_template, species)

    execute_query(query)

    if get_row_count() == 0 :
        print "This species in our database exists not!"
        print "Good-bye and may the force be with you!"
        exit()

    rows = fetch_all_rows()
    first_row = rows[0]

    homeworld = get_row_value(first_row, "homeworld")

    if homeworld!=None :  # Notice that in Python it's "None", not "NULL".
        print "<p>This species originally from planet <b>" +  homeworld + "</b> is.</p>"
    else :
        print "<p>The homeworld of this species we know not.</p>"

