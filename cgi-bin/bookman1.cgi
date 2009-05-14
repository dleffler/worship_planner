#!/usr/bin/perl

use config;
use DBI;
use CGI param,header;
use common;

CheckPriv("Add Book", "dataman",1);

my $bookcode=param("bookcode");
my $bookname=param("bookname");
my $error;

$bookcode =~ s/</&lt;/g ;
$bookcode =~ s/>/&gt;/g ;
$bookname =~ s/</&lt;/g ;
$bookname =~ s/>/&gt;/g ;
my $dbbookname=$bookname;
$dbbookname =~ s/\'/\\\'/g ;
my $dbbookcode=$bookcode;
$dbbookcode =~ s/\'/\\\'/g ;

my $numBooks=0;

my $dbcursor=$dbh->prepare("SELECT BookName, Code FROM Books WHERE BookName='$dbbookname'");
$dbcursor->execute();
my $dbrow=$dbcursor->fetchrow_hashref();
if ($dbrow != NULL)
{
	my $foundcode = $dbrow->{'Code'};
	$error = "$bookname already exists in the database with code $foundcode.";
	$dbcursor->finish();
	ReportError($error,"dataman");
	exit;
}
$dbcursor->finish();

my $dbcursor=$dbh->prepare("SELECT BookName, Code FROM Books WHERE Code='$dbbookcode'");
$dbcursor->execute();
my $dbrow=$dbcursor->fetchrow_hashref();
if ($dbrow != NULL)
{
	my $foundname = $dbrow->{'BookName'};
	$error = "The Code $bookcode already exists in the database. It belongs to \"$foundname\".";
	$dbcursor->finish();
	ReportError($error,"dataman");
	exit;
}
$dbcursor->finish();

$dbh->do("INSERT INTO Books (BookName, Code) VALUES ('$dbbookname', '$dbbookcode')");
my $user = $ENV{'REMOTE_USER'};
my $date=`date +\"%Y-%m-%d %H:%M:%S\"`;
$dbh->do("INSERT INTO Activity VALUES ('$date', '$user', 'Added New Book; $dbbookname, $dbbookcode')");

print header();
print "<html>\n";
print $myheader;
print "<head><title>Book Manager</title></head>\n";
print "<body>\n";
if ($noframes) { TopTable("dataman"); }
print "<p>New Book Accepted.\n";
print "Before using the Song Manager to add songs to this book you must click the <u>refresh</u> link in the Song Manager Window.\n" if (!$noframes);
print "<p><a href=\"bookman.cgi";
print "?noframes" if ($noframes);
print "\">Click here</a> to add another book.\n";
print "</body></html>\n";
