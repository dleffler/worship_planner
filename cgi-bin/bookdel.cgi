#!/usr/bin/perl

use config;
use DBI;
use CGI header;
use common;

CheckPriv("Delete Book", "dataman",1);

print header();
print "<html>\n";
print $myheader;
print "<head><title>Delete a Book</title></head>\n";
print "<body>\n";
if ($noframes) { TopTable("dataman"); }
print "</body></html>\n";
print "<form action=\"bookdel1.cgi";
print "?noframes" if ($noframes);
print "\" method=\"POST\">\n";
print "<p>Please note that a book cannot be deleted if there are songs in the database that are recorded as being contained in this book.\n";
print "<p>Choose which book to delete:\n";
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
print "<INPUT TYPE=SUBMIT VALUE=\"Delete Book\">\n";
print "</CENTER>\n";
print "</FORM>\n";
