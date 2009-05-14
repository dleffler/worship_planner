#!/usr/bin/perl

use CGI::Carp qw(fatalsToBrowser);
use config;
use CGI header;
use common;

my $priv = GetPriv();

print header();
print "<html>\n";
print $myheader;
print "<head><title>Rota Manager</title></head>\n";
print "<body>\n";
if ($noframes) { TopTable("rota"); }
print "<h1>Rota Manager</h1>\n";
print "<p>Current features of the Rota Manager are:<br>\n";
print "<table cellspacing=10 border=\"0\">\n";
print "<tr>\n";
print "<td align=\"left\" valign=\"top\">\n";
print "<a href=\"viewrota.cgi?noframes\">" if ($noframes);
print "<a href=\"viewrota.cgi\" target=\"Work\">" if (!$noframes);
print "View Rota</a><br>\n";
if ($priv > 1)
{
	print "<a href=\"rotaman.cgi?noframes\">" if ($noframes);
	print "<a href=\"rotaman.cgi\" target=\"Work\">" if (!$noframes);
	print "Manage Rota</a><br>\n";
}
print "</td>\n";

print "</tr>\n";
print "</table>\n";
print "</body></html>\n";
