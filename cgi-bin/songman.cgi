#!/usr/bin/perl

use config;
use common;
use DBI;
use CGI header;

CheckPriv("Add Song","dataman",1);

print header();
print "<html>\n";
print $myheader;
print "<head><title>Song Manager</title>";
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
print "<form action=\"songman1.cgi";
print "?noframes" if ($noframes);
print "\" method=\"POST\">\n";
if ($noframes)
{
	print "View current songs on this list<br>\n";
	print "<select name=\"current\">\n";
	my $dbcursor=$dbh->prepare("SELECT SongName FROM Songs ORDER BY SongName");
	$dbcursor->execute();
	while (my $dbrow=$dbcursor->fetchrow_hashref())
	{
		my $name=$dbrow->{'SongName'};
		print "<option value=\"$name\">$name\n";
	}
	$dbcursor->finish();
	print "</select><br>\n";
}
print "Enter the new song's name:\n";
print "<input name=songname type=TEXT size=30 maxlength=40>\n";
print "<br>Which book does it appear in?\n";
print "<select name=\"book\">\n";
print "<option value=\"Unknown\">Unknown\n";
my $dbcursor=$dbh->prepare("SELECT BookName, Code FROM Books ORDER BY BookName");
$dbcursor->execute();
while (my $dbrow=$dbcursor->fetchrow_hashref())
{
	my $code=$dbrow->{'Code'};
	my $name=$dbrow->{'BookName'};
	print "<option value=\"$code\">$name\n";
}
$dbcursor->finish();
print "</select>\n";
print "<a href=\"songman.cgi\">Refresh book list.</a>\n" if (!$noframes);
print "<br>What number is it?\n";
print "<input name=songnum type=TEXT size=10 maxlength=10 value=\"Unknown\">\n";
print "<br>Enter a comma separated list of <em>musical</em> styles appropriate for this song.<br>\n";
print "<input name=styles type=TEXT size=30 maxlength=255><br>\n";
GetStyles();
PrintStyles();
print "<br>Enter a comma separated list of categories appropriate for the <em>words</em> of this song.<br>\n";
print "<input name=categories type=TEXT size=30 maxlength=255><br>\n";
GetCategories();
PrintCategories();
print "<br>The words to the song are:<br>\n";
print "<textarea name=content cols=80 rows=25 maxlength=65000 wrap=soft></textarea><br>";
print "<CENTER>\n";
print "<INPUT TYPE=SUBMIT VALUE=\"Submit New Song\">\n";
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
