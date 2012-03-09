#!/usr/bin/padawan
print "Content-Type: text/html; encoding=utf8"
print

# The three lines above are absolutely essential. Make sure that your file has
# them and that they are _exactly_ like shown. When in doubt - copy and paste!
# If you do have those lines, have placed the file in the right directory
# (public_html/dynamic) and have set the right permissions (allowing "owner" to
# execute and prohibiting "group" and "other" from writing) then you should get
# the error page with Yoda in the worst case.

# First, let's connect to the database.
#
# !!! Make sure to replace "okenobi" with your username.!!!
#
# Also, replace "starwars" with another database
# name if you want to use another database.
connect_to_db("starwars", "okenobi")

# First, let's tell the user what then can do with this page. The user really
# should have come here specifying which species they want. So, if they did not,
# let's tell them so and send them away.

if not form_has_field("species") :
    print "A value for <b>species</b> specify you must!"
    exit()

# If we get to this point, it means the user _have_ specified the species.
# So, let's get the name of the species from the form.
species = get_form_field_value("species")

# Let's escape the value, in case we are dealing with a sneaky user!
species = escape_string(species)

# Let's generate an HTML header with the name of the species.

print "<h1> Species: "+species+"</h1>"

# Now let's prepare the first query. This one is just for us to get information
# about the species to put it at the top of the page. The actual query will
# depend on the value of the species, so we'll need a template. %s marks the
# place where the name of the species is going to be inserted.
query_template = """
select * from species where species='%s';
"""

# Now let's prepare the actual query we are going to use by filling in the
# template.
query = fill_template(query_template, species)

# Let's print the query just so we know what we are doing.
print "<pre>"+query+"</pre>"

# Let's send this query to the database. (Notice: the query, not the template.)
execute_query(query)

# Check if we got no results. If so, let's tell the user so and send them
# packing.

if get_row_count() == 0 : # note that we need "==" here, not "="
    print "This species in our database exists not!"
    print "Good-bye and may the force be with you!"
    exit()

# If we got this far, it means we got 1 or more results. Let's be lazy and just
# pick the top one.

rows = fetch_all_rows()
first_row = rows[0]

# Let's check this species homeworld."
homeworld = get_row_value(first_row, "homeworld")

# If the world is defined, tell the user what it is.

if homeworld!=None :  # Notice that in Python it's "None", not "NULL".
    print "<p>This species originally from planet <b>" +  homeworld + "</b> is.</p>"
else :
    print "<p>The homeworld of this species we know not.</p>"


# Now let's prepare our second query - this one will get the list of characters
# of this species. Again, we will need a template.
query_template = """
select * from persona
where species='%s';
"""

# Now let's prepare the actual query we are going to use by filling in the
# template.
query = fill_template(query_template, species)

# Let's again print the query just so we know what we are doing.
print "<pre>"+query+"</pre>"

# Let's send this query to the database. (Notice: the query, not the template.)
execute_query(query)

# Now let's go through all the results and make an HTML link for each one.
# To do this we will need a template for the link. Note that this template will
# generate a link with a URL that points to "show_character_info.py" setting the
# value of "name" to whatever is filled into the template.

link_template = """
- <a href="show_character_info.py?name=%s">%s</a> born on %s.<br/>
"""

# Let's see if get got no results.

if get_row_count() == 0 : # note that we need "==" here, not "="
    print "No creatures to this species belong!"
    print "Maybe the Death Star zapped them all!"
    exit()

# If we are here then it means we do have some characters to report.

print "<p>The following creatures to species <b>"+species+"</b> belong:</p>"

for row in fetch_all_rows() :
    name = get_row_value(row, "name")
    homeworld = get_row_value(row, "homeworld")
    # if homeworld is not spefied, let's set it to "unknown planet"
    if homeworld == None:
        homeworld = "unknown planet"
    # We are providing the value of name twice, because the first value
    # goes into the URL and the second goes into the text of the link.
    print fill_template(link_template, name, name, homeworld)

# Let's add a link back to the list of species, just in case.

print """
<p>Go back to <a href='list_species.py'>the list of species</a>.</p>
"""

print "<p><i>That's all, young Jedis!</i></p>"
