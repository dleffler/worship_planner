#!/usr/bin/perl

use config;
use DBI;
use CGI header;
use common;

CheckPriv("Add Book", "dataman",1);

print header();
print "<html>\n";
print $myheader;
print "<head><title>Book Manager</title></head>\n";
print "<body>\n";
if ($noframes) { TopTable("dataman"); }
print "</body></html>\n";
print "<form action=\"bookman1.cgi";
print "?noframes" if ($noframes);
print "\" method=\"POST\">\n";
print "View current books on this list:\n";
print "<select name=\"current\">\n";
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
print "<br>Enter the new book's name: \n";
print "<input name=bookname type=TEXT size=30 maxlength=40>\n";
print "<br>Enter an abbreviation code for the book: \n";
print "<input name=bookcode type=TEXT size=10 maxlength=10><br>\n";
print "<CENTER><br>\n";
print "<INPUT TYPE=SUBMIT VALUE=\"Submit New Book\">\n";
print "</CENTER>\n";
print "</FORM>\n";
