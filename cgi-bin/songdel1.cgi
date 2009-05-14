#!/usr/bin/perl

use config;
use DBI;
use CGI param,header;
use common;

CheckPriv("Delete Song","dataman",1);

my $song=param("song");
my $error;

my $dbsong=$song;
$dbsong =~ s/\'/\\\'/g ;

my $numBooks=0;

print header();
print "<html>\n";
print $myheader;
print "<head><title>Song Delete</title></head>\n";
print "<body>\n";
if ($noframes) { TopTable("dataman"); }
my $dbcursor=$dbh->prepare("SELECT Feature, Service, ServiceDate FROM ServiceLines WHERE BINARY Feature='$dbsong'");
$dbcursor->execute();
my $dbrow=$dbcursor->fetchrow_hashref();
if ($dbrow != NULL)
{
	print "<p>That song cannot be deleted since it is recorded that it was used in the following services.<br>\n";
	print "<select name=\"Services\">\n";
	do
	{
		my $service=$dbrow->{'Service'};
		my $date=$dbrow->{'ServiceDate'};
		print "<option value=\"$date$service\">$date, $service\n";
	} while ($dbrow=$dbcursor->fetchrow_hashref());
	print "</select>\n";
	$dbcursor->finish();
}
else
{
	$dbcursor->finish();

	$dbh->do("DELETE FROM Songs WHERE BINARY SongName='$dbsong'");
	my $user = $ENV{'REMOTE_USER'};
	my $date=`date +\"%Y-%m-%d %H:%M:%S\"`;
	$dbh->do("INSERT INTO Activity VALUES ('$date', '$user', 'Deleted Song; $dbsong')");

	print "<p>Song Deleted.\n";
}
print "</body></html>\n";
