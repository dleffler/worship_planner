#!/usr/bin/perl

use config;
use DBI;
use CGI param,header;
use common;

my %songs;

my $fromday=param("from_day");
my $frommonth=param("from_month");
my $fromyear=param("from_year");
my $today=param("to_day");
my $tomonth=param("to_month");
my $toyear=param("to_year");
my @services=param("service");
my $numsongs=param("numsongs");

$numsongs =~ s/\D//g ;

my @dbservices;
my $servstring="(";
my $first=0;
foreach $service (@services)
{
	my $dbservice= $service;
	$dbservice =~ s/\'/\\\'/g ;
	push @dbservices, $dbservice;
	if ($first == 1) { $servstring = $servstring." OR "; }
	$servstring = $servstring."Service='$dbservice'";
	$first=1;
}
$servstring=$servstring.")";

my $fromday = ((($frommonth == 4) || ($frommonth == 6) 
             || ($frommonth == 9) || ($frommonth == 11))
             && ($fromday == 31)) ? 30 : $fromday ;

my $fromday = (($frommonth == 2) && ($fromday >= 29)) ? 
              ((($fromyear % 4) == 0) ? 29 : 28 )
              : $fromday ;
		 
my $today   = ((($tomonth == 4) || ($tomonth == 6) 
             || ($tomonth == 9) || ($tomonth == 11))
             && ($today == 31)) ? 30 : $today ;

my $today   = (($tomonth == 2) && ($today >= 29)) ? 
              ((($toyear % 4) == 0) ? 29 : 28 )
              : $today ;
		 
my $startdate = "$fromyear-$frommonth-$fromday";
my $enddate   = "$toyear-$tomonth-$today";

my $selectstring= "SELECT COUNT(Feature), Feature FROM ServiceLines WHERE (ServiceDate >= '$startdate' AND ServiceDate <= '$enddate') AND (FType LIKE '\%Song\%' OR FType LIKE '\%Hymn\%') AND $servstring GROUP BY Feature";
my $maxuses=0;
my $dbcursor=$dbh->prepare($selectstring);
$dbcursor->execute();
while (my @dbrow=$dbcursor->fetchrow_array())
{
	if($songs{$dbrow[0]} eq "")
	{
		$songs{$dbrow[0]}=$dbrow[1];
	}
	else
	{
		$songs{$dbrow[0]}=$songs{$dbrow[0]}.";".$dbrow[1];
	}
	if ($dbrow[0] > $maxuses) { $maxuses = $dbrow[0]; }
}

my $scale= ($maxuses > 100) ? 200 : (($maxuses > 50) ? 100 : (($maxuses > 20) ? 50 : (($maxuses > 10) ? 20 : 10 ))) ;

print header();
print "<html>\n";
print $myheader;
print "<head><title>$numsongs Most Popular Songs</title></head>\n";
print "<body>\n";
if ($noframes) { TopTable("stats"); }
print "<center>\n";
print "<font size=\"+2\">The $numsongs most popular songs between $fromday/$frommonth/$fromyear and $today/$tomonth/$toyear<br>\n";
print "For @services Services</font><br><br>\n";
print "<table width=\"100%\"border=\"1\" style=\"border-collapse: collapse\">\n";
print "<tr><th align=\"left\" valign=\"top\">Song</th>\n";
print "<th align=\"left\" valign=\"top\">\n";
print "<table border=\"0\" width=\"100%\"><tr><th>Number of Uses</th></tr><tr><td><img src=\"$url/$imagedir/scale$scale.png\"></td></tr></table>\n";
print "</th><th align=\"left\" valign=\"top\">Services used in</th></tr>\n";
my $songcount=0;
my $i;
for($i=$maxuses;$i>0;$i--)
{
	if($songs{$i} ne "")
	{
		split /;/, $songs{$i};
		my $j;
		for($j=0;$j<(scalar @_);$j++)
		{
			$_[$j] =~ s/</&lt;/g ;
			$_[$j] =~ s/>/&gt;/g ;
			print "<tr>\n";
			print "<td align=\"left\" valign=\"top\">$_[$j]</td>";
			print "<td align=\"left\" valign=\"top\">\n";
			print "<table border=\"0\">\n";
			my $width = ($i * 500) / $scale;
			my $balance = 512 - $width;
			print "<tr><td width=\"$width\" bgcolor=\"red\" align=\"center\">$i</td>\n";
			print "<td width=\"$balance\">&nbsp;</td></tr>\n";
			print "</table>\n";
			print "</td>\n";
			print "<td>";
			ServiceList($_[$j]);
			print "</td>\n";
			print "</tr>\n";
			$songcount++;
			last if ($songcount == $numsongs);
		}
	}
	last if ($songcount == $numsongs);
}
print "</table>\n";
print "</center>\n";
print "</body></html>\n";

sub ServiceList
{
	my $song=shift;
	my $dbsong=$song;
	$dbsong =~ s/\'/\\\'/g ;
	$dbcursor=$dbh->prepare("SELECT ServiceDate, Service FROM ServiceLines WHERE Feature='$dbsong' AND ServiceDate >= '$startdate' AND ServiceDate <= '$enddate' AND $servstring ORDER BY ServiceDate DESC, Service ASC");
	$dbcursor->execute();
	print "<select name=\"$song\">\n";
	while ($dbrow=$dbcursor->fetchrow_hashref())
	{
		my $sdate=$dbrow->{'ServiceDate'};
		my $chosen=$dbrow->{'Service'};
		print "<option value=\"$sdata$chosen\">$sdate $chosen\n";
	}
	print "</select>\n";
}
