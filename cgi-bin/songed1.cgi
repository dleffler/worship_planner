#!/usr/bin/perl

use config;
use common;
use DBI;
use CGI header,param;

my $selected=param("song");
my $dbselected = $selected;
$dbselected =~ s/\'/\\\'/g ;

CheckPriv("Edit Song", "dataman",1);

my $dbcursor=$dbh->prepare("SELECT * FROM Songs WHERE SongName='$dbselected'");
$dbcursor->execute();
my $dbrow=$dbcursor->fetchrow_hashref();
my $songName   = $dbrow->{'SongName'};
$songName =~ s/</&lt;/g ;
$songName =~ s/>/&gt;/g ;
my $songBook   = $dbrow->{'Book'};
$songBook =~ s/</&lt;/g ;
$songBook =~ s/>/&gt;/g ;
my $songNum    = $dbrow->{'Number'};
$songNum =~ s/</&lt;/g ;
$songNum =~ s/>/&gt;/g ;
my $style      = $dbrow->{'Style'};
$style =~ s/</&lt;/g ;
$style =~ s/>/&gt;/g ;
my $categories = $dbrow->{'Categories'};
$categories =~ s/</&lt;/g ;
$categories =~ s/>/&gt;/g ;
my $words = $dbrow->{'Words'};

print header();
print "<html>\n";
print $myheader;
print "<head><title>Song Editor</title>";
print <<p1;
<script type="text/javascript" src="/apps/fckeditor/fckeditor.js"></script>
    <script type="text/javascript">
      window.onload = function()
      {
        var oFCKeditor = new FCKeditor( 'content' ) ;
        oFCKeditor.BasePath = "/apps/fckeditor/" ;
        oFCKeditor.ReplaceTextarea() ;
        oFCKeditor.Height = 400 ; // 400 pixels
      }
    </script>
p1

print "</head>\n";
print "<body>\n";
if ($noframes) { TopTable("dataman"); }
print "</body></html>\n";
print "<form action=\"songed2.cgi";
print "?noframes" if ($noframes);
print "\" method=\"POST\">\n";
print "Song name:\n";
print "<input name=oldsongname type=HIDDEN size=30 maxlength=40 value=\"$songName\">\n";
print "<input name=songname type=TEXT size=30 maxlength=40 value=\"$songName\">\n";
print "<br>This song is in the following book:\n";
print "<input name=oldbook type=HIDDEN size=30 maxlength=40 value=\"$songBook\">\n";
print "<select name=\"book\">\n";
print "<option value=\"Unknown\"";
print " selected" if ($songBook eq "Unknown");
print ">Unknown\n";
my $dbcursor=$dbh->prepare("SELECT BookName, Code FROM Books ORDER BY BookName");
$dbcursor->execute();
while (my $dbrow=$dbcursor->fetchrow_hashref())
{
	my $code=$dbrow->{'Code'};
	my $name=$dbrow->{'BookName'};
	print "<option value=\"$code\"";
	print " selected" if ($code eq $songBook);
	print ">$name\n";
}
$dbcursor->finish();
print "</select>\n";
print "<br>and is song number\n";
print "<input name=oldsongnum type=HIDDEN size=10 maxlength=10 value=\"$songNum\">\n";
print "<input name=songnum type=TEXT size=10 maxlength=10 value=\"$songNum\">\n";
print "<br>This song matches the following musical styles.<br>\n";
print "<input name=styles type=TEXT size=30 maxlength=255 value=\"$style\"><br>\n";
GetStyles();
PrintStyles();
print "<br>This song matches the following lyrical categories.<br>\n";
print "<input name=categories type=TEXT size=30 maxlength=255 value=\"$categories\"><br>\n";
GetCategories();
PrintCategories();
print "<br>The words to the song are:<br>\n";
print "<textarea name=content cols=80 rows=25 maxlength=65000 wrap=soft>" . $words . "</textarea><br>";
print "<CENTER>\n";
print "<INPUT TYPE=SUBMIT VALUE=\"Update Song\">\n";
print "</CENTER>\n";
print "</FORM>\n";

sub PrintStyles
{
	print "Current styles are ";
	my $stylenum=0;
	while (($name, $value) = each %styles)
	{
		if ($stylenum != 0) { print ", "; }
		$stylenum=1;
		print "$name";
	}
	print ". Or feel free to create your own.\n";
}

sub PrintCategories
{
	print "Current categories are ";
	my $catnum=0;
	while (($name, $value) = each %categories)
	{
		if ($catnum != 0) { print ", "; }
		$catnum=1;
		print "$name";
	}
	print ". Or feel free to create your own.\n";
}
