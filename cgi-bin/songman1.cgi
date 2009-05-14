#!/usr/bin/perl

use config;
use DBI;
use CGI param,header;
use common;

CheckPriv("Add Song", "dataman",1);

my $songname=param("songname");
$songname =~ s/</&lt;/g ;
$songname =~ s/>/&gt;/g ;
my $bookcode=param("book");
$bookcode =~ s/</&lt;/g ;
$bookcode =~ s/>/&gt;/g ;
my $songnum=param("songnum");
$songnum =~ s/</&lt;/g ;
$songnum =~ s/>/&gt;/g ;
my $styles=param("styles");
$styles =~ s/</&lt;/g ;
$styles =~ s/>/&gt;/g ;
my $categories=param("categories");
$categories =~ s/</&lt;/g ;
$categories =~ s/>/&gt;/g ;
my $words=param("content");
my $error="";

my $dbsongname=$songname;
$dbsongname =~ s/\'/\\\'/g ;
my $dbbookcode=$bookcode;
$dbbookcode =~ s/\'/\\\'/g ;
$styles =~ s/\'/\\\'/g ;
$categories =~ s/\'/\\\'/g ;
my $numBooks=0;
my $dbcursor;
my $dbrow;

$dbcursor=$dbh->prepare("SELECT Songs.SongName, Songs.Number, Songs.Book, Books.BookName FROM Songs, Books WHERE (SongName='$dbsongname' OR (Book='$dbbookcode' AND Number='$songnum')) AND Books.Code = Songs.Book");
$dbcursor->execute();
$dbrow=$dbcursor->fetchrow_hashref();
if ($dbrow != NULL)
{
	my $dbSong = $dbrow->{'SongName'};
	my $dbNum = $dbrow->{'Number'};
	my $dbBook = $dbrow->{'Book'};
	my $dbBookName = $dbrow->{'BookName'};
	if($songname eq $dbSong)
	{
		$error = "Song Name clashes with $dbSong; number $dbNum in $dbBookName.";
		ReportError($error,"dataman");
		$dbcursor->finish();
		exit;
	}
	if((($bookcode eq $dbBook) && ($songnum eq $dbNum)) && (($bookcode ne "Unknown") && ($songnum ne "Unknown")))
	{
		$error = $error . "Book and Number clashes with $dbSong; number $dbNum in $dbBookName.";
		ReportError($error,"dataman");
		$dbcursor->finish();
		exit;
	}
}
$dbcursor->finish();

$dbh->do("INSERT INTO Songs (SongName, Book, Number, Style, Categories, Words) VALUES ('$dbsongname', '$dbbookcode', '$songnum', '$styles', '$categories', '$words')");
my $user = $ENV{'REMOTE_USER'};
my $date=`date +\"%Y-%m-%d %H:%M:%S\"`;
$dbh->do("INSERT INTO Activity VALUES ('$date', '$user', 'Added New Song; $dbsongname, $dbbookcode, $songnum')");

print header();
print "<html>\n";
print $myheader;
print "<head><title>Song Manager</title></head>\n";
print "<body>\n";
if ($noframes) { TopTable("dataman"); }
print "<p>New Song Accepted.\n";
print "Before this song is available to the Service Planner you must click the \"Submit and Refresh\" button in the Service Planner Window.\n" if (!$noframes);
print "<p><a href=\"songman.cgi";
print "?noframes" if ($noframes);
print "\">Click here</a> to add another song.\n";
print "</body></html>\n";
