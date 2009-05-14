#!/usr/bin/perl

use CGI param,header;
use config;
use common;
use servcommon;
use DBI;

CheckPriv("Submit Service Order", "index",1);
$servstring=param("servstring");
$date=param("date");
$service=param("service");

my $now="date +\"%Y-%m-%d %H:%M:%S\"";

my $dbservice=$service;
$dbservice =~ s/\'/\\\'/g ;

print header();
print "<html>\n";
print $myheader;
print "<head><title>Order(s) for $service Service</title></head>\n";
print "<body>\n";
print Printable();
print "</body>\n</html>\n";
