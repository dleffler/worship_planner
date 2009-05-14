#!/usr/bin/perl

use config;
use DBI;
use CGI header,param;
use common;

CheckPriv("Edit Book", "dataman",1);

my $selected=param("bookcode");
my $dbselected = $selected;
$dbselected =~ s/\'/\\\'/g ;

print header();
print "<html>\n";
print $myheader;
print "<head><title>Book Editor</title></head>\n";
print "<body>\n";
if ($noframes) { TopTable("dataman"); }
print "</body></html>\n";
print "<form action=\"booked2.cgi";
print "?noframes" if ($noframes);
print "\" method=\"POST\">\n";
my $dbcursor=$dbh->prepare("SELECT BookName, Code FROM Books WHERE Code='$dbselected'");
$dbcursor->execute();
my $dbrow=$dbcursor->fetchrow_hashref();
my $code=$dbrow->{'Code'};
my $name=$dbrow->{'BookName'};
$dbcursor->finish();
print "<br>Edit the book's name: \n";
print "<input name=bookname type=TEXT size=30 maxlength=40 value=\"$name\">\n";
print "<br>Edit the book's abbreviation code: \n";
print "<input name=bookcode type=TEXT size=10 maxlength=10 value=\"$code\"><br>\n";
print "<input name=oldcode type=hidden size=10 maxlength=10 value=\"$selected\"><br>\n";
print "<input name=oldname type=hidden size=10 maxlength=10 value=\"$name\"><br>\n";
print "<CENTER>\n";
print "<INPUT TYPE=SUBMIT VALUE=\"Update Book\">\n";
print "</CENTER>\n";
print "</FORM>\n";
