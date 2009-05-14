#!/usr/bin/perl

use config;
use DBI;
use CGI param,header;
use common;

CheckPriv("Edit Book", "dataman",1);

my $bookcode=param("bookcode");
my $bookname=param("bookname");
my $oldcode=param("oldcode");
my $oldname=param("oldname");
my $error;

my $dbbookname=$bookname;
$dbbookname =~ s/\'/\\\'/g ;
my $dboldname=$bookname;
$dboldname =~ s/\'/\\\'/g ;
my $dbbookcode=$bookcode;
$dbbookcode =~ s/\'/\\\'/g ;
my $dboldcode=$bookcode;
$dboldcode =~ s/\'/\\\'/g ;

my $numBooks=0;

if ( $bookname ne $oldname )
{
	my $dbcursor=$dbh->prepare("SELECT BookName, Code FROM Books WHERE BookName='$dbbookname'");
	$dbcursor->execute();
	my $dbrow=$dbcursor->fetchrow_hashref();
	if ($dbrow != NULL)
	{
		my $foundcode = $dbrow->{'Code'};
		$error = "A book with the name $bookname already exists in the database with code $foundcode.";
		$dbcursor->finish();
		ReportError($error,"dataman");
		exit;
	}
	$dbcursor->finish();
}

if ( $bookcode ne $oldcode )
{
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
}

$dbh->do("DELETE FROM Books WHERE BINARY Code='$oldcode'");
$dbh->do("INSERT INTO Books (BookName, Code) VALUES ('$dbbookname', '$dbbookcode')");
$dbh->do("UPDATE Songs SET Book='$bookcode' WHERE Book='$oldcode'");
my $user = $ENV{'REMOTE_USER'};
my $date=`date +\"%Y-%m-%d %H:%M:%S\"`;
$dbh->do("INSERT INTO Activity VALUES ('$date', '$user', 'Update Book; $dboldname, $dboldcode to $dbbookname, $dbbookcode')");

print header();
print "<html>\n";
print $myheader;
print "<head><title>Book Manager</title></head>\n";
print "<body>\n";
if ($noframes) { TopTable("dataman"); }
print "<p>Book Updated.\n";
print "</body></html>\n";
