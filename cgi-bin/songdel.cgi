#!/usr/bin/perl

use config;
use common;
use DBI;
use CGI header;

CheckPriv("Delete Song","dataman",1);

print header();
print "<html>\n";
print $myheader;
print "<head><title>Song Delete</title></head>\n";
print "<body>\n";
if ($noframes) { TopTable("dataman"); }
print "</body></html>\n";
print "<form action=\"songdel1.cgi";
print "?noframes" if ($noframes);
print "\" method=\"POST\">\n";
print "<p>Please note that a song cannot be deleted if it is recorded as having been used in any service.\n";
print "<p>Select the Song you wish to delete:\n";
print "<select name=\"song\">\n";
my $dbcursor=$dbh->prepare("SELECT SongName FROM Songs ORDER BY SongName");
$dbcursor->execute();
while (my $dbrow=$dbcursor->fetchrow_hashref())
{
	my $name=$dbrow->{'SongName'};
	print "<option value=\"$name\">$name\n";
}
$dbcursor->finish();
print "</select><br>\n";
print "<CENTER><br>\n";
print "<INPUT TYPE=SUBMIT VALUE=\"Delete Song\">\n";
print "</CENTER>\n";
print "</FORM>\n";
