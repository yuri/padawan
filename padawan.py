
import cgi
import MySQLdb
import os
import getpass
import sys

class PadawanError (Exception) :
    pass
    
class PadawanExit (Exception) :
    pass    

def insist(test, message) :
    """ A replacement for assert."""
    if not test :
       raise PadawanError, message

def make_and_check_config_file_path(username) :
   """ Create a config file path for the username and check that it's valid. """
   insist(username, "User name not specified.")
   config_file = "/home/" + username + "/.my.cnf"
   insist(os.path.exists(config_file),
          "There is no config file for user '%s'. (Looking for '%s'.)" % (username, config_file))
   insist(os.access(config_file, os.R_OK),
          "Access to config file '%s' for user '%s' denied to user '%s'. " % (config_file, username, getpass.getuser()))
   return config_file


class State :

   def __init__(self) :
      self.form = cgi.FieldStorage()
      self.conn = None
      self.cursor = None
      self.fetched_rows = None

   def get_form_field_value(self, key) :
      insist(self.form.has_key(key),
                "The form does not have a value for field '%s'." % key)
      return self.form[key].value

   def print_form(self) :
      for name in self.form.keys() :
         print name, "=", self.get_form_field_value(name)

   def connect_to_db(self, db_name, username) :

      config_file = make_and_check_config_file_path(username)
      try :
         self.conn = MySQLdb.connect(db=db_name, read_default_file=config_file)
      except MySQLdb.OperationalError as e:
         insist(False, "Couldn't connect to the database:<br/>" + str(e))
      try :
         self.cursor=self.conn.cursor()
         self.cursor.connection.autocommit(True)
      except MySQLdb.OperationalError as e:
         insist(False, "Couldn't obtain a database cursor:<br/>" + str(e))

   def form_has_field(self, name) :
      return self.form.has_key(name)

   def escape_string(self, text) :
      return self.conn.escape_string(text)

   def check_connection(self) :
      insist(self.conn,
             "You do not seem to be connected to the database server.")

   def execute_query(self, sql) :
      self.check_connection()
      self.cursor.execute(sql);
      self.fetched_rows = None
      self.field_hash = {}
      counter = 0
      if self.cursor.description :
          for field in self.cursor.description :
              self.field_hash[field[0]]=counter
              counter += 1

   def commit(self) :
      self.check_connection()
      self.conn.commit()      

   def results_have_field(self, name) :
      return self.field_hash.has_key(name)

   def get_row_count(self) :
      self.check_connection()
      return self.cursor.rowcount

   def fetch_all_rows(self) :
      self.check_connection()
      self.fetched_rows = self.cursor.fetchall()
      return self.fetched_rows

   def get_row(self, i) :
      insist(self.fetched_rows, "You haven't fetched any rows from the last query.")
      count = self.get_row_count()
      insist(i<count, "You have %d rows, so you cannot get row %d." % (count, i))
      return self.fetched_rows[i]

   def get_row_value(self, row, field_name) :
      insist(self.results_have_field(field_name), "Current resultset does not have field '%s'." % field_name)
      return row[self.field_hash[field_name]]

   def fill_template(self, template, *args) :
      try :
         return template % args
      except Exception as e:
         raise PadawanError, str(e)

global padawan
padawan = State()

def get_form_field_value(key) :
   global padawan
   return padawan.get_form_field_value(key)

def print_form() :
   global padawan
   padawan.print_form()

def connect_to_db(config_file, db_name) :
   global padawan
   padawan.connect_to_db(config_file, db_name)

def form_has_field(name) :
   global padawan
   return padawan.form_has_field(name)

def escape_string(text) :
   global padawan
   return padawan.escape_string(text)

def execute_query(sql) :
   global padawan
   padawan.execute_query(sql)

def commit() :
   global padawan
   padawan.commit()

def get_row_count() :
   global padawan
   return padawan.get_row_count()

def fetch_all_rows() :   
   global padawan
   return padawan.fetch_all_rows()

def get_row(i) :   
   global padawan
   return padawan.get_row(i)

def get_row_value(row, field) :
   global padawan
   return padawan.get_row_value(row, field)

def fill_template(*args) :
   global padawan
   return padawan.fill_template(*args)

def exit() :
   raise PadawanExit

