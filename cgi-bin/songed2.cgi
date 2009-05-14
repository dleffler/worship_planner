#!/usr/bin/perl

use config;
use DBI;
use CGI param,header;
use common;

CheckPriv("Edit Song", "dataman",1);

my $songname=param("songname");
$songname =~ s/</&lt;/g ;
$songname =~ s/>/&gt;/g ;
my $oldsongname=param("oldsongname");
$oldsongname =~ s/</&lt;/g ;
$oldsongname =~ s/>/&gt;/g ;
my $bookcode=param("book");
$bookcode =~ s/</&lt;/g ;
$bookcode =~ s/>/&gt;/g ;
my $oldbookcode=param("oldbook");
$oldbookcode =~ s/</&lt;/g ;
$oldbookcode =~ s/>/&gt;/g ;
my $songnum=param("songnum");
$songnum =~ s/</&lt;/g ;
$songnum =~ s/>/&gt;/g ;
my $oldsongnum=param("oldsongnum");
$oldsongnum =~ s/</&lt;/g ;
$oldsongnum =~ s/>/&gt;/g ;
my $styles=param("styles");
$styles =~ s/</&lt;/g ;
$styles =~ s/>/&gt;/g ;
my $categories=param("categories");
$categories =~ s/</&lt;/g ;
$categories =~ s/>/&gt;/g ;
my $words=param("content");
my $error="";

my $dbbookcode=$bookcode;
$dbbookcode =~ s/\'/\\\'/g ;
my $dbsongname=$songname;
$dbsongname =~ s/\'/\\\'/g ;
my $dboldsongname=$oldsongname;
$dboldsongname =~ s/\'/\\\'/g ;
my $dbstyles=$styles;
$dbstyles =~ s/\'/\\\'/g ;
my $dbcategories=$categories;
$dbcategories =~ s/\'/\\\'/g ;
my $dboldbookcode=$oldbookcode;
$dboldbookcode =~ s/\'/\\\'/g ;

my $numBooks=0;
my $dbcursor;
my $dbrow;

$dbcursor=$dbh->prepare("SELECT Songs.SongName, Songs.Number, Songs.Book, Books.BookName FROM Songs, Books WHERE (BINARY SongName='$songname' OR (Book='$dbbookcode' AND Number='$dbsongnum')) AND Books.Code = Songs.Book");
$dbcursor->execute();
$dbrow=$dbcursor->fetchrow_hashref();
if ($dbrow != NULL)
{
	my $dbSong = $dbrow->{'SongName'};
	my $dbNum = $dbrow->{'Number'};
	my $dbBook = $dbrow->{'Book'};
	my $dbBookName = $dbrow->{'BookName'};
	if(($songname eq $dbSong) && ($oldsongname ne $songname))
	{
		$error = "Song Name clashes ";
		$dbcursor->finish();
		ReportError($error,"dataman");
		exit;
	}
	if(((($bookcode eq $dbBook) && ($songnum eq $dbNum)) && (($bookcode ne "Unknown") && ($songnum ne "Unknown"))) && (($bookcode ne $oldbookcode) || ($songnum ne $oldsongnum)))
	{
		$error = $error . "Book and Number clashes ";
		$error = $error . "with $dbSong; number $dbNum in $dbBookName.";
		$dbcursor->finish();
		ReportError($error,"dataman");
		exit;
	}
}
$dbcursor->finish();

$dbh->do("DELETE FROM Songs WHERE BINARY SongName='$dboldsongname'");
$dbh->do("INSERT INTO Songs (SongName, Book, Number, Style, Categories, Words) VALUES ('$dbsongname', '$dbbookcode', '$songnum', '$dbstyles', '$dbcategories', '$words')");
$dbh->do("UPDATE ServiceLines SET Feature='$dbsongname' WHERE BINARY Feature='$dboldsongname'");
my $user = $ENV{'REMOTE_USER'};
my $date=`date +\"%Y-%m-%d %H:%M:%S\"`;
$dbh->do("INSERT INTO Activity VALUES ('$date', '$user', 'Updated Song; $dboldsongname, $dboldbookcode, $oldsongnum to $dbsongname, $dbbookcode, $songnum')");

print header();
print "<html>\n";
print $myheader;
print "<head><title>Song Manager</title></head>\n";
print "<body>\n";
if ($noframes) { TopTable("dataman"); }
print "<p>Song Updated.\n";
print "</body></html>\n";
