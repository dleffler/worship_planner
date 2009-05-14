#!/usr/bin/perl

use config;
use DBI;
use CGI param,header;
use common;

CheckPriv("Delete Book", "dataman",1);
my $bookcode=param("bookcode");
my $error;

my $dbbookcode=$bookcode;
$dbbookcode =~ s/\'/\\\'/g ;

my $numBooks=0;

print header();
print "<html>\n";
print $myheader;
print "<head><title>Book Delete</title></head>\n";
print "<body>\n";

if ($noframes) { TopTable("dataman"); }
my $dbcursor=$dbh->prepare("SELECT SongName, Book FROM Songs WHERE Book='$dbbookcode'");
$dbcursor->execute();
my $dbrow=$dbcursor->fetchrow_hashref();
if ($dbrow != NULL)
{
	print "<p>That book cannot be deleted since the following songs are recorded as being contained therein.<br>\n";
	print "<select name=\"songs\">\n";
	do
	{
		my $songname=$dbrow->{'SongName'};
		print "<option value=\"$songname\">$songname\n";
	} while ($dbrow=$dbcursor->fetchrow_hashref());
	print "</select>\n";
	print "<p>Please update or delete these songs if you still wish to delete this book.\n";
	$dbcursor->finish();
}
else
{
	$dbcursor->finish();

	$dbh->do("DELETE FROM Books WHERE BINARY Code='$dbbookcode'");
	my $user = $ENV{'REMOTE_USER'};
	my $date=`date +\"%Y-%m-%d %H:%M:%S\"`;
	$dbh->do("INSERT INTO Activity VALUES ('$date', '$user', 'Deleted Book; $dbbookcode')");

	print "<p>Book Deleted.\n";
}
print "</body></html>\n";
