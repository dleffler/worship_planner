#!/usr/bin/perl

use CGI::Carp qw(fatalsToBrowser);
use config;
use DBI;
use CGI header;
use common;

CheckPriv("Delete Team Member","team",2);

print header();
print "<html>\n";
print $myheader;
print "<head><title>Delete a Team Member</title></head>\n";
print "<body>\n";
if ($noframes) { TopTable("team"); }
print "</body></html>\n";
print "<form action=\"teamdel1.cgi";
print "?noframes" if ($noframes);
print "\" method=\"POST\">\n";
print "<p>Please note that deleting a team member will automatically remove them from any teams to which they are assigned.\n";
print "<p>Choose which Team member to delete:\n";
print "<select name=\"member\">\n";
my $dbcursor=$dbh->prepare("SELECT Name FROM Team ORDER BY Name");
$dbcursor->execute();
while (my $dbrow=$dbcursor->fetchrow_hashref())
{
	my $name=$dbrow->{'Name'};
	print "<option value=\"$name\">$name\n";
}
$dbcursor->finish();
print "</select>\n";
print "<CENTER><br>\n";
print "<INPUT TYPE=SUBMIT VALUE=\"Delete Member\">\n";
print "</CENTER>\n";
print "</FORM>\n";
