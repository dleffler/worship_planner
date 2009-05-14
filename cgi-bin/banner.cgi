#!/usr/bin/perl

use config;
use CGI header;

my $caller=$ENV{'QUERY_STRING'};

print header();
print "<html>\n";
print $myheader;
print "<head><title>Banner</title></head>\n";
print "<body>\n";
print "<center>\n";
print "<font size=\"+2\">Worship Service Planning and Archiving System - Version 0.5</font><br>\n";
# print "Written by <a href=\"http://www.netouerkz.co.uk\">Netouerkz Computer Services</a><br>\n";
print "<table width=\"100%\" border=\"0\">\n";
print "<tr><td align=center valign=top><a href=\"$caller.cgi?";
# print "+" if ($caller eq "servicepick");
print "noframes\" target=\"_top\">No Frames Version</a></td>\n";
print "<td align=center valign=top><a href=\"$url/$htmldir/mydet.html\" target=\"_top\">My Details</a></td>\n";
print "<td align=center valign=top><a href=\"$url/$htmldir/team.html\" target=\"_top\">Team Manager</a></td>\n";
print "<td align=center valign=top><a href=\"$url/$htmldir/rota.html\" target=\"_top\">Rota Manager</a></td>\n";
print "<td align=center valign=top><a href=\"$url/$htmldir/dataman.html\" target=\"_top\">Song Manager</a></td>\n";
print "<td align=center valign=top><a href=\"$url/$htmldir/service.html\" target=\"_top\">Service Planner</a></td>\n";
print "<td align=center valign=top><a href=\"$url/$htmldir/stats.html\" target=\"_top\">Statistics</a></td>\n";
print "<td align=center valign=top><a href=\"$url/$htmldir/help.html\" target=\"_blank\">Documentation</a></td>\n";
print "</tr>\n";
print "</table>\n";
print "</center>\n";
print "</body>\n";
print "</html>\n";
