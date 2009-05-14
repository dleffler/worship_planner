#!/usr/bin/perl

use config;
use DBI;
use CGI param,header;
use common;

CheckPriv("Delete Service","dataman",1);

my $deldate=param("del_date");

split /\./, $deldate;
$service=$_[1];
$date=$_[0];
split /-/, $date;
my $year=$_[0];
my $month=$_[1];
my $day=$_[2];
#my $daysuffix = (((substr $day, -1) == 1) && ($day != 11)) ? "st" : (((substr $day, -1) == 2) ? "nd" : "th") ;
$day=DaySuffix($day);
my $servstring="$day $months[$month-1] $year $service";

print header();
print "<html>\n";
print $myheader;
print "<head><title>Service Delete</title></head>\n";
print "<body>\n";
if ($noframes) { TopTable("dataman"); }
$dbh->do("DELETE FROM ServiceLines WHERE ServiceDate='$date' AND Service='$service'");
print "<p>$servstring Service Deleted.</p>\n";
print "</body></html>\n";
