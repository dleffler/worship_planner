#!/usr/bin/perl

use CGI::Carp qw(fatalsToBrowser);
use config;
use DBI;
use CGI header;
use common;

CheckPriv("Manage Team Structure","team",1);

print header();
print "<html>\n";
print $myheader;
print "<head><title>Manage Team Structure</title></head>\n";
print "<body>\n";
if ($noframes) { TopTable("team"); }
print "</body></html>\n";
print "<form action=\"teamstruct1.cgi";
print "?noframes" if ($noframes);
print "\" method=\"POST\">\n";
print "<p>Choose which team to edit:\n";
print "<select name=\"team\">\n";
my $dbcursor=$dbh->prepare("SELECT DISTINCT Team FROM TeamStruct ORDER BY Team");
$dbcursor->execute();
while (my $dbrow=$dbcursor->fetchrow_hashref())
{
	my $team=$dbrow->{'Team'};
	print "<option value=\"$team\">$team\n";
}
$dbcursor->finish();
print "</select>\n";
print "<br>Or enter another name below to create a new team: \n";
print "<INPUT NAME=\"newname\" TYPE=TEXT SIZE=10 MAXLENGTH=10>\n";
print "<CENTER>\n";
print "<INPUT TYPE=SUBMIT VALUE=\"Choose Team\">\n";
print "</CENTER>\n";
print "</FORM>\n";
