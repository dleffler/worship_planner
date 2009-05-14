#!/usr/bin/perl

use config;
use common;
use DBI;
use CGI header,param;

CheckPriv("Edit Song","dataman",1);

print header();
print "<html>\n";
print $myheader;
print "<head><title>Song Editor</title></head>\n";
print "<body>\n";
if ($noframes) { TopTable("dataman"); }
print "</body>\n";
print "<form action=\"songed1.cgi";
print "?noframes" if ($noframes);
print "\" method=\"POST\">\n";
print "Select the Song you wish to edit:\n";
print "<select name=\"song\">\n";
my $dbcursor=$dbh->prepare("SELECT SongName FROM Songs ORDER BY SongName");
$dbcursor->execute();
while (my $dbrow=$dbcursor->fetchrow_hashref)
{
	my $SongName = $dbrow->{'SongName'};
	print "<option value=\"$SongName\">$SongName\n";
}
print "</select>\n";
print "<CENTER><br>\n";
print "<INPUT TYPE=SUBMIT VALUE=\"Edit Song\">\n";
print "</CENTER>\n";
print "</FORM>\n";
