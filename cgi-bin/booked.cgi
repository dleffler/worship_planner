#!/usr/bin/perl

use config;
use DBI;
use CGI header;
use common;

CheckPriv("Edit Book", "dataman",1);

print header();
print "<html>\n";
print $myheader;
print "<head><title>Book Editor</title></head>\n";
print "<body>\n";
if ($noframes) { TopTable("dataman"); }
print "</body></html>\n";
print "<form action=\"booked1.cgi";
print "?noframes" if ($noframes);
print "\" method=\"POST\">\n";
print "Select the Book you wish to edit:\n";
print "<select name=\"bookcode\">\n";
my $dbcursor=$dbh->prepare("SELECT BookName, Code FROM Books ORDER BY BookName");
$dbcursor->execute();
while (my $dbrow=$dbcursor->fetchrow_hashref())
{
	my $code=$dbrow->{'Code'};
	my $name=$dbrow->{'BookName'};
	$code =~ s/</&lt;/g ;
	$code =~ s/>/&gt;/g ;
	$name =~ s/</&lt;/g ;
	$name =~ s/>/&gt;/g ;
	print "<option value=\"$code\">$name; Code - $code\n";
}
$dbcursor->finish();
print "</select>\n";
print "<CENTER><br>\n";
print "<INPUT TYPE=SUBMIT VALUE=\"Edit Selected Book\">\n";
print "</CENTER>\n";
print "</FORM>\n";
