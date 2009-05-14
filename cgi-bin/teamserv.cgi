#!/usr/bin/perl

use CGI::Carp qw(fatalsToBrowser);
use config;
use common;
use DBI;
use CGI header,param;

my $date=param("date");
my $service=param("service");
split /\./, $date;
$service=$_[1];
$date=$_[0];
split /-/, $date;
my $year=$_[0];
my $month=$_[1];
my $day=$_[2];
#my $daysuffix = (((substr $day, -1) == 1) && ($day != 11)) ? "st" : (((substr $day, -1) == 2) ? "nd" : "th") ;
$day=DaySuffix($day);
my $servstring="$day $months[$month-1] $year";
$date = sprintf "%04d-%02d-%02d", $year, $month, $day;

# Get Team from Rota
my $dbcursor=$dbh->prepare("SELECT Team FROM Rota WHERE ServiceDate='$date' AND Service='$service'");
$dbcursor->execute();
my $dbrow=$dbcursor->fetchrow_hashref();
my $team=$dbrow->{'Team'};
$dbcursor->finish();
# Get Names and Roles from Team
print header();
print "<html>\n";
print $myheader;
print "<head><title>Team Expected</title></head>\n";
print "<body>\n";
if ($noframes) { TopTable("team"); }
print "<CENTER>\n";
print "<font size=\"+2\">Team Expected at the $service service $servstring</font>\n";
print "<br><br>\n";
print "</body>\n";
print "<form action=\"teammail.cgi";
print "?noframes" if ($noframes);
print "\" method=\"POST\">\n";
print "<table border=\"0\">\n";
$dbcursor=$dbh->prepare("SELECT * FROM TeamStruct WHERE Team='$team' ORDER BY Role");
$dbcursor->execute();
my $counter=0;
while ($dbrow=$dbcursor->fetchrow_hashref())
{
	print "<tr>\n";
	my $role=$dbrow->{'Role'};
	my $main=$dbrow->{'Main'};
	print "<td align=\"left\" valign=\"top\"><b>$role</b>:</td>\n";
	my $subcursor=$dbh->prepare("SELECT Sub FROM RotaSub WHERE ServiceDate='$date' AND Service='$service' AND Role='$role' AND Main='$main'");
	$subcursor->execute();
	my $subrow=$subcursor->fetchrow_hashref();
	if($subrow == NULL)
	{
		#No substitutions
		print "<td align=\"left\" valign=\"top\">$main<input type=hidden name=\"name$counter\" value=\"$main\"><input type=hidden name=\"role$counter\" value=\"$role\"></td>\n";
	}
	else
	{
		#Show substitute
		print "<td align=\"left\" valign=\"top\">\n";
		my $sub=$subrow->{'Sub'};
		if($sub eq "Sub5")
		{
			print "No one is available to fill in for $main.\n";
			print "<input type=hidden name=\"name$counter\" value=\"blank\"><input type=hidden name=\"role$counter\" value=\"$role\">\n";
		}
		else
		{
			print $dbrow->{$sub}." (filling in for $main).\n";
			print "<input type=hidden name=\"name$counter\" value=\"".$dbrow->{$sub}."\"><input type=hidden name=\"role$counter\" value=\"$role\">\n";
		}
		print "</td>\n";
	}
	$subcursor->finish();
	print "</tr>\n";
	$counter++;
}
$dbcursor->finish();
print "</table>\n";
print "<input type=hidden name=\"subject\" value=\"$service service on $servstring\">\n";
print "<INPUT TYPE=SUBMIT VALUE=\"Email Team\">\n";
print "</center></html>\n";
