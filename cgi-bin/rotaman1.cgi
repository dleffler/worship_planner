#!/usr/bin/perl

use config;
use common;
use DBI;
use CGI header,param;
use rotacommon;

CheckPriv("Rota Manager", "rota",2);

DateMung();

print header();
print "<html>\n";
print $myheader;
print "<head><title>Rota Manager</title></head>\n";
print "<body>\n";
if ($noframes) { TopTable("rota"); }
print "</body>\n";
print "<form action=\"rotaman2.cgi";
print "?noframes" if ($noframes);
print "\" method=\"POST\">\n";
CreateRotaLines();
PopulateRotaLines();
print "<CENTER>\n";
print "<p>Worship Rota from $fromday/$frommonth/$fromyear to $today/$tomonth/$toyear\n";
GenerateTable("rw");
print "<INPUT type=hidden name=\"start\" value=\"$fromyear-$frommonth-$fromday\">\n";
print "<INPUT type=hidden name=\"end\" value=\"$toyear-$tomonth-$today\">\n";
print "<INPUT type=hidden name=\"services\" value=\"";
foreach $service (@chosenservs)
{
	$service =~ s/;/:/g ;
	print "$service;";
}
print "\">\n";
print "<INPUT TYPE=SUBMIT VALUE=\"Submit Rota\">\n";
print "</CENTER>\n";
print "</FORM>\n";
