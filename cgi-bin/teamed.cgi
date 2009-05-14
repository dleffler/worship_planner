#!/usr/bin/perl

use CGI::Carp qw(fatalsToBrowser);
use config;
use common;
use DBI;
use CGI header,param;

CheckPriv("Edit Team Member","team",1);

print header();
print "<html>\n";
print $myheader;
print "<head><title>Team Member Editor</title></head>\n";
print "<body>\n";
if ($noframes) { TopTable("team"); }
print "</body>\n";
print "<form action=\"teamed1.cgi";
print "?noframes" if ($noframes);
print "\" method=\"POST\">\n";
print "<br>Select the Team Member you wish to edit:\n";
print "<select name=\"name\">\n";
my $dbcursor=$dbh->prepare("SELECT Name FROM Team ORDER BY Name");
$dbcursor->execute();
while (my $dbrow=$dbcursor->fetchrow_hashref)
{
	my $Name = $dbrow->{'Name'};
	print "<option value=\"$Name\">$Name\n";
}
print "</select>\n";
print "<CENTER><br>\n";
print "<INPUT TYPE=SUBMIT VALUE=\"Edit Team Member\">\n";
print "</CENTER>\n";
print "</FORM>\n";
