#!/usr/bin/perl

use CGI::Carp qw(fatalsToBrowser);
use config;
use common;
use DBI;
use CGI header,param;

print header();
print "<html>\n";
print $myheader;
print "<head><title>Team Member Summary</title></head>\n";
print "<body>\n";
if ($noframes) { TopTable("team"); }
print "</body>\n";
print "<form action=\"teamsum1.cgi";
print "?noframes" if ($noframes);
print "\" method=\"POST\">\n";
print "<br>Select the format for your summary\n";
print "<select name=\"format\">\n";
print "<option value=\"teams\">Show all Teams\n";
print "<option value=\"people\">List people and their roles\n";
print "<option value=\"roles\">List roles and their people\n";
print "</select>\n";
print "<CENTER><br>\n";
print "<INPUT TYPE=SUBMIT VALUE=\"Show Summary\">\n";
print "</CENTER>\n";
print "</FORM>\n";
