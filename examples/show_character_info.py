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
# should have come here specifying which name of the character they want info
# about. So, if they did not, let's tell them so and send them away.

if not form_has_field("name") :
    print "A value for <b>name</b> specify you must!"
    exit()

# If we get to this point, it means the user _have_ specified the name.
# So, let's get the name of the name from the form.
name = get_form_field_value("name")

# Let's escape the value, in case we are dealing with a sneaky user!
name = escape_string(name)

# Let's generate an HTML header with the name of the character.

print "<h1> Creature: "+name+"</h1>"

# Now let's prepare the query.
query_template = """
select * from persona where name='%s';
"""

# Now let's prepare the actual query we are going to use by filling in the
# template.
query = fill_template(query_template, name)

# Let's print the query just so we know what we are doing.
print "<pre>"+query+"</pre>"

# Let's send this query to the database. (Notice: the query, not the template.)
execute_query(query)

# Check if we got no results. If so, let's tell the user so and send them
# packing.

if get_row_count() == 0 : # note that we need "==" here, not "="
    print "This creature in our database exists not!"
    print "Good-bye and may the force be with you!"
    exit()

# If we got this far, it means we got 1 or more results. Let's be lazy and just
# pick the top one.

rows = fetch_all_rows()
first_row = rows[0]

# Let's check this character's species."
species = get_row_value(first_row, "species")

# If the species is defined, tell the user what it is.

if species!=None :  # Notice that in Python it's "None", not "NULL".
    print "<p>This creature a <b>" +  species + "</b> is.</p>"
else :
    print "<p>The species of this creature we know not.</p>"


# Let's check this character's homeworld."
homeworld = get_row_value(first_row, "homeworld")

# If the world is defined, tell the user what it is.

if homeworld!=None :
    print "<p>This creature on planet <b>" +  homeworld + "</b> born was.</p>"
else :
    print "<p>The homeworld of this creature we know not.</p>"

# Let's check this character's size."
size = get_row_value(first_row, "size")


if size!=None :
    template = "<p>This creature %s meters tall is.</p>"
    print fill_template(template, size)
else :
    print "<p>This creature's height we know not.</p>"

# And just for a bit of extra fun, let's add a form that the user could use to
# search for character's by species, prefilling this form to this species name.

form_template = """
<p><form action="search_by_species.py" method="get">
  Enter another species:
  <input type="text" name="species" value="%s"/>
  <input type="submit"/>
</form></p>
"""

print fill_template(form_template, species)

print "<p><i>That's all, young Jedis!</i></p>"

