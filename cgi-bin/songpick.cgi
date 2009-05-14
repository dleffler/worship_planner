#!/usr/bin/perl

use config;
use common;
use DBI;
use CGI header,param;

my $chosenStyle=param('style');
my $chosenCat=param('category');
$chosenStyle=($chosenStyle eq "") ? "All" : $chosenStyle;
$chosenCat=($chosenCat eq "") ? "All" : $chosenCat;
GetStyles();
GetCategories();

print header();
print "<html>\n";
print $myheader;
print "<head><title>Song Picker</title></head>\n";
print "<body>\n";
if ($noframes) { TopTable("dataman"); }
print "</body>\n";
print "<form action=\"songpick.cgi";
print "?noframes" if ($noframes);
print "\" method=\"POST\">\n";
print "Select Musical Style:\n";
print "<select name=\"style\">\n";
print "<option value=\"All\"";
print " selected" if ($chosenStyle eq "All");
print ">All\n";
while (($name, $value) = each %styles)
{
	print "<option value=\"$name\"";
	print " selected" if ($chosenStyle eq $name);
	print ">$name\n";
}
print "</select>\n";

print " Select Song Category\n";
print "<select name=\"category\">\n";
print "<option value=\"All\"";
print " selected" if ($chosenCat eq "All");
print ">All\n";
while (($name, $value) = each %categories)
{
	print "<option value=\"$name\"";
	print " selected" if ($chosenCat eq $name);
	print ">$name\n";
}
print "</select>\n";

print "<br>These songs match the chosen style and category:\n";
print "<select name=\"song\">\n";

$chosenStyle =~ s/\'/\\\'/g ;
$chosenCat =~ s/\'/\\\'/g ;

if ($chosenStyle eq "All")
{
	$chosenStyle="\%";
}
else
{
	$chosenStyle="\%$chosenStyle\%";
}

if ($chosenCat eq "All")
{
	$chosenCat="\%";
}
else
{
	$chosenCat="\%$chosenCat\%";
}
my $dbcursor=$dbh->prepare("SELECT SongName, Book, Number FROM Songs WHERE Style LIKE '$chosenStyle' AND Categories LIKE '$chosenCat' ORDER BY SongName");
$dbcursor->execute();
while (my $dbrow=$dbcursor->fetchrow_hashref)
{
	my $SongName = $dbrow->{'SongName'};
	my $SongBook = $dbrow->{'Book'};
	my $SongNum = $dbrow->{'Number'};
	print "<option value=\"$SongName\">$SongName - $SongBook, $SongNum\n";
}
print "</select>\n";
print "<CENTER><br>\n";
print "<INPUT TYPE=SUBMIT VALUE=\"Filter Songs\">\n";
print "</CENTER>\n";
print "</FORM>\n";
