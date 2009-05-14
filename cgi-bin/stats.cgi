#!/usr/bin/perl

use config;
use CGI header;
use common;

print header();
print "<html>\n";
print $myheader;
print "<head><title>Statistical Analysis</title></head>\n";
print "<body>\n";
if ($noframes) { TopTable("stats"); }
print "<h1>Statistical Analysis</h1>\n";
print "<p>Current analyses are:<br>\n";
print "<table cellspacing=10 border=\"0\">\n";
print "<tr>\n";
print "<td align=\"left\" valign=\"top\">\n";
print "<a href=\"mostpop.cgi?noframes\">" if ($noframes);
print "<a href=\"mostpop.cgi\" target=\"Work\">" if (!$noframes);
print "Most Popular Songs</a><br>\n";
print "<a href=\"songpop.cgi?noframes\">" if ($noframes);
print "<a href=\"songpop.cgi\" target=\"Work\">" if (!$noframes);
print "How popular is a particular song</a><br>\n";
print "<a href=\"least.cgi?noframes\">" if ($noframes);
print "<a href=\"least.cgi\" target=\"Work\">" if (!$noframes);
print "Least Used Songs</a><br>\n";
print "</td>\n";
print "<td align=\"left\" valign=\"top\">\n";
print "<a href=\"unlisted.cgi?noframes\">" if ($noframes);
print "<a href=\"unlisted.cgi\" target=\"Work\">" if (!$noframes);
print "Unlisted Songs</a><br>\n";
print "<a href=\"mostpopread.cgi?noframes\">" if ($noframes);
print "<a href=\"mostpopread.cgi\" target=\"Work\">" if (!$noframes);
print "Most Popular Readings</a><br>\n";print "</td>\n";
print "<td align=\"left\" valign=\"top\">\n";
print "<a href=\"activity.cgi?noframes\">" if ($noframes);
print "<a href=\"activity.cgi\" target=\"Work\">" if (!$noframes);
print "Activity Log</a><br>\n";
print "</td>\n";
print "</tr>\n";
print "</table>\n";
print "</body></html>\n";
