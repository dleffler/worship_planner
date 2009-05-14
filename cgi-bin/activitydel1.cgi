#!/usr/bin/perl

use config;
use DBI;
use CGI param,header;
use common;

CheckPriv("Delete Activity Log", "activity",1);
my $error;

my $numBooks=0;

print header();
print "<html>\n";
print $myheader;
print "<head><title>Clear Activity Log</title></head>\n";
print "<body>\n";

if ($noframes) { TopTable("stats"); }

$dbh->do("TRUNCATE TABLE `Activity`");
my $user = $ENV{'REMOTE_USER'};
my $date=`date +\"%Y-%m-%d %H:%M:%S\"`;
$dbh->do("INSERT INTO Activity VALUES ('$date', '$user', 'Cleared Activity Log')");

print "<p>Activiy Log Cleared.</p>\n";
print "</body></html>\n";
