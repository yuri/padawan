#!/usr/bin/padawan
print "Content-Type: text/html; encoding=utf8"
print

# The three lines above are absolutely essential. Make sure that your file has
# them and that they are _exactly_ like shown. When in doubt - copy and paste!
# If you do have those lines, have placed the file in the right directory
# (public_html/dynamic) and have set the right permissions (allowing "owner" to
# execute and prohibiting "group" and "other" from writing) then you should get
# the error page with Yoda in the worst case.

# Now let's connect to the database.
#
# !!! Make sure to replace "okenobi" with your username.!!!
#
# Also, replace "starwars" with another database
# name if you want to use another database.
connect_to_db("starwars", "okenobi")

# Now let's tell the user what then can do with this page.
print """<p>To see who belongs to each species, on the species name click
you must!</p>
"""

# In this script we are always going to issue the same query, just to get the
# list of species.
query = """
select distinct(species) from persona where species is not null;
"""

# Let's send this query to the database.
execute_query(query)

# Now let's go through all the results and make an HTML link for each one.
# To do this we will need a template for the link. Note that this template will
# generate a link with a URL that points to "search_by_species" setting the
# value of "species" to whatever is filled into the template.
# Note that we are going to generate an extremely ugly HTML page, because we
# don't really care about esthetics at all in this class. You can do the same
# in your final assignment. (Just make sure it's usable.)

link_template = """
<a href="search_by_species.py?species=%s">%s</a><br/>
"""

for row in fetch_all_rows() :
    species = get_row_value(row, "species")
    
    # We are providing the value of species twice, because the first value
    # goes into the URL and the second goes into the text of the link.
    print fill_template(link_template, species, species)

print "<p><i>That's all, young Jedis!</i></p>"
