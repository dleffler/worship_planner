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
my $songname=param("songname");

my $dbsongname=$songname;
$dbsongname =~ s/\'/\\\'/g ;
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

my $selectstring = "SELECT COUNT(Feature), Feature FROM ServiceLines WHERE (ServiceDate >= '$startdate' AND ServiceDate <= '$enddate') AND (FType LIKE '\%Song\%' OR FType LIKE '\%Hymn\%') AND $servstring AND Feature='$dbsongname' GROUP BY Feature";

my $numuses=0;
my $dbcursor=$dbh->prepare($selectstring);
$dbcursor->execute();
my @dbrow=$dbcursor->fetchrow_array();
my $numuses;
if ($dbrow[0] == NULL) { $numuses = 0;}
else { $numuses=$dbrow[0]; }

my $scale= ($numuses > 100) ? 200 : (($numuses > 50) ? 100 : (($numuses > 20) ? 50 : (($numuses > 10) ? 20 : 10 ))) ;

print header();
print "<html>\n";
print $myheader;
print "<head><title>$songname - Popularity</title></head>\n";
print "<body>\n";
if ($noframes) { TopTable("stats"); }
print "<center>\n";
print "<font size=\"+2\">$songname - Popularity between $fromday/$frommonth/$fromyear and $today/$tomonth/$toyear<br>\n";
print "For @services Services</font><br><br>\n";
if ($numuses == 0)
{
	print "<p>$songname has not been used in any @services";
	print " services between $fromday/$frommonth/$fromyear and $today/$tomonth/$toyear.\n";
}
else
{
	print "<table width=\"100%\"border=\"1\">\n";
	print "<tr><th align=\"left\" valign=\"top\">Song</th>\n";
	print "<th align=\"left\" valign=\"top\">\n";
	print "<table border=\"0\" width=\"100%\"><tr><th>Number of Uses</th></tr><tr><td><img src=\"$url/$imagedir/scale$scale.png\"></td></tr></table>\n";
	print "</th><th align=\"left\" valign=\"top\">Services used in</th></tr>\n";
	print "<tr>\n";
	print "<td align=\"left\" valign=\"top\">$songname</td>";
	print "<td align=\"left\" valign=\"top\">\n";
	print "<table border=\"0\">\n";
	my $width = ($numuses * 500) / $scale;
	my $balance = 512 - $width;
	print "<tr><td width=\"$width\" bgcolor=\"red\" align=\"center\">$numuses</td>\n";
	print "<td width=\"$balance\">&nbsp;</td></tr>\n";
	print "</table>\n";
	print "</td>\n";
	print "<td>";
	ServiceList($songname);
	print "</td>\n";
	print "</tr>\n";
	print "</table>\n";
}
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
