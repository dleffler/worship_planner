#!/usr/bin/perl

use config;
use common;
use DBI;
use CGI header,param;
use Date::Pcalc qw(Date_to_Days Add_Delta_Days Day_of_Week);

CheckPriv("Rota Manager", "rota",2);

$start=param("start");
$end=param("end");
$services=param("services");
@startbitz=split /-/, $start;
@endbitz=split /-/, $end;
my $user = $ENV{'REMOTE_USER'};
my $date=`date +\"%Y-%m-%d %H:%M:%S\"`;
$dbh->do("INSERT INTO Activity VALUES ('$date', '$user', 'Updated Rota for $start to $end')");

print header();
print "<html>\n";
print $myheader;
print "<head><title>Rota Manager</title></head>\n";
print "<body>\n";
if ($noframes) { TopTable("rota"); }
print "<p align=\"center\"><font size=\"+2\">Rota Submitted</font></p>\n";
print "<p>Below is a preview of your rota. Click the \"Continue\" button below for a printable version of the current rota. If you select the \"Email Team\" option before clicking \"Continue\" then the rota will be emailed to all team members that have their email address stored on the system. Once emailing is complete you will then be presented with the printable rota.</p>\n";
print "<p>As a No-Frames user the top line of the printable Rota will be a link back to the Rota Manager. This is to give you a printable rota that is free of cruft, but also contains a link back into the main system.</p>\n" if ($noframes);
print "</body>\n";
print "<form action=\"rotamail1.cgi";
print "?noframes" if ($noframes);
print "\" method=\"POST\">\n";
print "<center>\n";
print "<input type=checkbox name=\"email\" value=\"1\">Send Rota By Email&nbsp;&nbsp;&nbsp;\n";
print "<input type=SUBMIT value=\"Continue\"><br><br><br>\n";
print "<input type=hidden name=\"start\" value=\"$start\">\n";
print "<input type=hidden name=\"end\" value=\"$end\">\n";
print "<input type=hidden name=\"services\" value=\"$services\">\n";
print "Worship Rota $startbitz[2]/$startbitz[1]/$startbitz[0] to $endbitz[2]/$endbitz[1]/$endbitz[0]\n";
print "<table border=\"1\" style=\"border-collapse: collapse\">\n";
print "<tr><th>Date</th><th>Service</th><th>Team</th><th>Leader</th><th>Preacher</th><th>Notes</th></tr>\n";

my $line=0;
my $dateparam="sdate$line";
my $sdate=param($dateparam);
while($sdate ne "")
{
	my $servparam="service$line";
	my $teamparam="team$line";
	my $leaderparam="leader$line";
	my $preacherparam="preacher$line";
	my $notesparam="notes$line";
	
	my $service=param($servparam);
	my $team=param($teamparam);
	my $leader=param($leaderparam);
	my $preacher=param($preacherparam);
	my $notes=param($notesparam);
	
	if(($team ne "") || ($leader ne "") || ($preacher ne "") || ($notes ne ""))
	{
		$dbh->do("DELETE FROM Rota WHERE ServiceDate='$sdate' AND Service='$service'");
		$dbh->do("INSERT INTO Rota VALUES ('$sdate', '$service', '$team', '$leader', '$preacher', '$notes')");
	}

	split /-/, $sdate;
	print "<tr><td>$_[2]-$_[1]-$_[0]&nbsp;</td><td>$service&nbsp;</td><td>$team&nbsp;</td><td>$leader&nbsp;</td><td>$preacher&nbsp;</td><td>$notes&nbsp;</td></tr>\n";

	$line++;
	$dateparam="sdate$line";
	$sdate=param($dateparam);
}
print "</table>\n";
print "</form>\n";
