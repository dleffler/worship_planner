#!/usr/bin/perl

use config;
use common;
use DBI;
use CGI header,param;

$start=param("start");
$next=param("prevnext");

if ($next ne "") 
{
 if ($next eq "Prev")
 {
    $start=$start-30;
    if ($start<0) {$start=0}
 }
 else
 {
    $start=$start+30;
 }
}
else
{
  $start=0;
}

my %unlisted;

print header();
print "<html>\n";
print $myheader;
print "<head><title>Activity Log</title></head>\n";
print "<body>\n";
if ($noframes) { TopTable("stats"); }
print "<p>The following activity has taken place:</p>\n";
print "<table border=\"1\" style=\"border-collapse: collapse\" width=\"100%\">\n";
	
my $dbcursor=$dbh->prepare("SELECT * FROM `Activity` ORDER BY `Acttime` DESC LIMIT $start , 30");
$dbcursor->execute();

	my $rowcount=0;
	while (my $dbrow=$dbcursor->fetchrow_hashref())
	{
		$rowcount++;
		print "<tr><td>\n";
		print "On ";
		print $dbrow->{'Acttime'};
		print ", ";
		print $dbrow->{'Who'};
		print " ";
		print $dbrow->{'What'};
		print "</td></tr>\n";
	}

print "</table>\n";
print "<FORM action=\"activity.cgi\" method=\"post\">\n";
print "<INPUT NAME=\"start\" TYPE=HIDDEN VALUE=\"$start\">\n";
print "<CENTER>\n";
print "<INPUT type=\"submit\" name=\"prevnext\" value=\"Prev\">\n" if ($start>0);
print "<INPUT type=\"submit\" name=\"prevnext\" value=\"Next\">\n" if ($rowcount==30);
print "</CENTER>\n";
print "</FORM>\n";
print "<FORM action=\"activitydel1.cgi\" method=\"post\">\n";
print "<CENTER>\n";
print "<INPUT type=\"submit\" name=\"delete\" value=\"Clear Activity Log\">\n";
print "</CENTER>\n";
print "</FORM>\n";
print "</body>\n";
