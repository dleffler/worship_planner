#!/usr/bin/perl

use config;
use DBI;
use CGI param,header;
use common;

CheckPriv("Merge Songs","dataman",1);

my $retain=param("retain");
my $merge=param("merge");

my $dbmerge=$merge;
$dbmerge =~ s/\'/\\\'/g ;
my $dbretain=$retain;
$dbretain =~ s/\'/\\\'/g ;

my $numBooks=0;

print header();
print "<html>\n";
print $myheader;
print "<head><title>Song Merge</title></head>\n";
print "<body>\n";
if ($noframes) { TopTable("dataman"); }

$dbh->do("DELETE FROM Songs WHERE BINARY SongName='$dbmerge'");
$dbh->do("UPDATE ServiceLines SET Feature='$dbretain' WHERE BINARY Feature='$dbmerge'");
my $user = $ENV{'REMOTE_USER'};
my $date=`date +\"%Y-%m-%d %H:%M:%S\"`;
$dbh->do("INSERT INTO Activity VALUES ('$date', '$user', 'Merged Song $dbmerge into $dbretain')");

print "<p>Songs Merged.\n";
print "</body></html>\n";
