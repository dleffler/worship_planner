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
my $threshold=param("threshold");

$threshold =~ s/\D//g ;

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

my $dbcursor=$dbh->prepare("SELECT SongName FROM Songs ORDER BY SongName");
$dbcursor->execute();
while (my $dbrow=$dbcursor->fetchrow_hashref())
{
	my $songname=$dbrow->{'SongName'};
	my $dbsongname=$songname;
	$dbsongname =~ s/\'/\\\'/g ;

	my $selectstring = "SELECT COUNT(Feature), Feature FROM ServiceLines WHERE (ServiceDate >= '$startdate' AND ServiceDate <= '$enddate') AND (FType LIKE '\%Song\%' OR FType LIKE '\%Hymn\%') AND $servstring AND Feature='$dbsongname' GROUP BY Feature";
	my $cursor2=$dbh->prepare($selectstring);
	$cursor2->execute();
	my @row2=$cursor2->fetchrow_array();
	my $songnum=$row2[0];
	$cursor2->finish();
	$songnum = 0 if ($songnum == NULL);

	if ($songnum <= $threshold)
	{
		if ($songs{$songnum} eq "")
		{
			$songs{$songnum}=$songname;
		}
		else
		{
			$songs{$songnum}=$songs{$songnum}.";".$songname;
		}
	}
}
$dbcursor->finish();

print header();
print "<html>\n";
print $myheader;
print "<head><title>Least Popular Songs</title></head>\n";
print "<body>\n";
if ($noframes) { TopTable("stats"); }
print "<center>\n";
print "<font size=\"+2\">The least popular songs between $fromday/$frommonth/$fromyear and $today/$tomonth/$toyear<br>\n";
print "For @services Services</font><br><br>\n";
print "</center>\n";
my $i;
for($i=0;$i<=$threshold;$i++)
{
	if($songs{$i} ne "")
	{
		if ($i == 0)
		{
			print "<font size=\"+2\">These songs have not been used at all during any";
			print " @services";
		}
		else
		{
			print "<font size=\"+2\">These songs have been used ";
			print "once " if ($i == 1);
			print "twice " if ($i == 2);
			print "$i times " if ($i > 2);
			print "during @services";
		}
		print " services between $fromday/$frommonth/$fromyear and $today/$tomonth/$toyear</font><br>\n";
		split /;/, $songs{$i};
		my $j;
		for($j=0;$j<(scalar @_);$j++)
		{
			$_[$j] =~ s/</&lt;/g ;
			$_[$j] =~ s/>/&gt;/g ;
			print "$_[$j]<br>";
		}
	}
}
print "</body>\n";
print "</html>\n";
