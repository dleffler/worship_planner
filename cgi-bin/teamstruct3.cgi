#!/usr/bin/perl

use CGI::Carp qw(fatalsToBrowser);
use config;
use common;
use tscommon;
use DBI;
use CGI param,header;

CheckPriv("Manage Team Structure","team",1);
my %approvedSongs;

my @invalids;
my @badroles;

$team=param("team");
$dbteam=$team;
$dbteam =~ s/\'/\\\'/g ;

print header();
print "<html>\n";
print $myheader;
print "<head><title>Team Manager</title></head>\n";
print "<body>\n";
if ($noframes) { TopTable("team"); }

ReadInputs();
SubmitTeam();
CheckChanges();
