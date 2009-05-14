#!/usr/bin/perl

# Redisplay copy of service order after mailing

use CGI param,header;
use config;
use common;
use servcommon;
use DBI;

CheckPriv("View Service Orders", "index",2);
#$servstring=param("servstring");
$date=param("date");
#$service=param("service");
split /-/, $date;
my $year=$_[0];
my $month=$_[1];
my $day=$_[2];
#my $daysuffix = (((substr $day, -1) == 1) && ($day != 11)) ? "st" : (((substr $day, -1) == 2) ? "nd" : "th") ;
$day=DaySuffix($day);
my $now="date +\"%Y-%m-%d %H:%M:%S\"";

my $dbservice=$service;
$dbservice =~ s/\'/\\\'/g ;

print header();
print "<html>\n";
print $myheader;
print "<head><title>Order(s) for $dbservice Service</title></head>\n";
print "<body>\n";
for ($k=0; $k<(scalar @services); $k++) # go thorough all service types for a given date
{
  $service=$services[$k];
  $servstring="$day $months[$month-1] $year $service";
  print Printable();
  print "<br>\n";
}
print "</body>\n</html>\n";
