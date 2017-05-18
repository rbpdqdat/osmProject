# osmProject
OSM Data Wrangle Project

# Introduction

This is a short project demonstrating xml parsing of Open Street Maps data, auditing/cleaning the file structures, creating a json file, creating a mongo database collection, and then performing queries of the collection.  The area of focuse for this project is the Denver Metro area.  There is a python notebook included in this repository that explains the source and some of the details: 'OSM_Data_Wrangle.ipynb' 

The code is split into 2 main sections:
1) Audit/Cleaning Code
  a) zipcodes.py
      Cleans up the zipcodes to a standard format and inserts a missing field '99999' if the 
      entered data does not match the specified format
  b) phones.py
      Cleans up the phone numbers to a standard format using the python 'phonenumbers' module
      a standard format of '+19999999999' is entered if the field has data that does not fit the 
      'US' format
  c) address.py
      Standardizes the abbreviated fields of the street names (i.e. 'Str' is changed to 'Street')
2) Creating json Code
  a) osm_create_json.py
      This program imports the above programs to clean the data and produce a new json file that
      can be imported into a mongo database colection

# License

The information in this Jupyter Notebook can be replicated under [MIT](https://choosealicense.com/licenses/mit/) license.
