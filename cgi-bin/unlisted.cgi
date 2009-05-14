#!/usr/bin/perl

use config;
use common;
use DBI;
use CGI header,param;

print header();
print "<html>\n";
print $myheader;
print "<head><title>Unlisted Songs</title></head>\n";
print "<body>\n";
if ($noframes) { TopTable("stats"); }
print "<p>The following songs are recorded as having been used in services, but are not on the song list:</p>\n";

GetApprovedSongs();

my %unlisted;

my $dbcursor=$dbh->prepare("SELECT DISTINCT Feature FROM ServiceLines WHERE FType LIKE '\%Song\%' OR FType LIKE '\%song\%' OR FType LIKE '\%Hymn\%' OR FType LIKE '\%hymn\%'");
$dbcursor->execute();
while (my $dbrow=$dbcursor->fetchrow_hashref())
{
	my $song=$dbrow->{'Feature'};
	if ($approvedSongs{$song} eq "")
	{
		my $dbsong=$song;
		$dbsong =~ s/\'/\\\'/g ;
		my $ulcursor=$dbh->prepare("SELECT ServiceDate, Service FROM ServiceLines WHERE (FType LIKE '\%Song\%' OR FType LIKE '\%song\%' OR FType LIKE '\%Hymn\%' OR FType LIKE '\%hymn\%') AND Feature='$dbsong'");
		$ulcursor->execute();
		while(my $ulrow=$ulcursor->fetchrow_hashref())
		{
			$unlisted{$song}=$unlisted{$song}.($ulrow->{'ServiceDate'})."-".($ulrow->{'Service'})." ";
			print "<! Setting $unlisted{$song} >\n";
		}
		$ulcursor->finish();
	}
}
$dbcursor->finish();

while (($song, $service) = each %unlisted)
{
	if ($song ne "")
  {
	   print "$song used $service<br>\n";
  }
}
print "</body>\n";
