
#  ---------------------------------------------------------------
#  DESCRIPTION	: Add/Alter tables for Worship Planner 0.3.1
#
#  This sql file will add a column called words to the 
#  Songs table. 
#  ---------------------------------------------------------------

ALTER TABLE Songs ADD `Words` text NOT NULL;