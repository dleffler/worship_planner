#!/usr/bin/perl

use config;
use common;
use DBI;
use CGI header,param;
use rotacommon;
use Date::Pcalc qw(Date_to_Days Add_Delta_Days Day_of_Week);

DateMung();

print header();
print "<html>\n";
print $myheader;
print "<head><title>Rota Manager</title></head>\n";
print "<body>\n";
if ($noframes) { TopTable("rota"); }
CreateRotaLines();
PopulateRotaLines();
print "<CENTER>\n";
print "<p>Worship Rota from $fromday/$frommonth/$fromyear to $today/$tomonth/$toyear\n";
GenerateTable("ro");
print "</CENTER>\n";
print "</body>\n";
