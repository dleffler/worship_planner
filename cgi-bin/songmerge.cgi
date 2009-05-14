#!/usr/bin/perl

use config;
use common;
use DBI;
use CGI header;

CheckPriv("Merge Songs","team",1);

my @songs;
my $songcount=0;

my $dbcursor=$dbh->prepare("SELECT SongName FROM Songs ORDER BY SongName");
$dbcursor->execute();
while (my $dbrow=$dbcursor->fetchrow_hashref())
{
	$songs[$songcount]=$dbrow->{'SongName'};
	$songcount++;
}
$dbcursor->finish();

print header();
print "<html>\n";
print $myheader;
print "<head><title>Song Merge</title></head>\n";
print "<body>\n";
if ($noframes) { TopTable("dataman"); }
print "</body></html>\n";
print "<form action=\"songmerge1.cgi";
print "?noframes" if ($noframes);
print "\" method=\"POST\">\n";
print "<p>Select the Song you wish to retain:\n";
print "<select name=\"retain\">\n";
my $i;
for ($i=0;$i<$songcount;$i++)
{
	my $name=$songs[$i];
	print "<option value=\"$name\">$name\n";
}
print "</select><br>\n";
print "<p>Select the Song you wish to merge:\n";
print "<select name=\"merge\">\n";
my $i;
for ($i=0;$i<$songcount;$i++)
{
	my $name=$songs[$i];
	print "<option value=\"$name\">$name\n";
}
print "</select><br>\n";
print "<CENTER><br>\n";
print "<INPUT TYPE=SUBMIT VALUE=\"Merge Songs\">\n";
print "</CENTER>\n";
print "</FORM>\n";
