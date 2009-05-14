#!/usr/bin/perl

use config;
use common;
use rotacommon;
use DBI;
use CGI header,param;

CheckPriv("Rota Manager","rota",2);

$start=param("start");
$end=param("end");
$services=param("services");
@servs=split /;/, $services;
@startbitz=split /-/, $start;
@endbitz=split /-/, $end;
my $mailflag=param("email");

print header();
print "<html>\n";
print $myheader;
print "<head><title>Rota Manager</title></head>\n";
print "<body>\n";

if($mailflag)
{
	Email();
}
else
{
	Printable();
}

sub Email
{
	if ($noframes) { TopTable("rota"); }
	print "</body>\n";
	print "<form action=\"rotamail2.cgi";
	print "?noframes" if ($noframes);
	print "\" method=\"POST\">\n";
	print "<p align=center>Worship Rota for $startbitz[2]/$startbitz[1]/$startbitz[0] to $endbitz[2]/$endbitz[1]/$endbitz[0] for ";
	foreach $serv (@servs) { print "$serv "; }
	print "services</p>\n";
	print "<table border=\"0\" width=\"100%\">\n";
	print "<tr>\n";
	print "<td valign=top>\n";
	print "Enter your message below:-\n";
	my $user = $ENV{'REMOTE_USER'};
	my $dbcursor=$dbh->prepare("SELECT Name, Username FROM Team WHERE Username='$user'");
	$dbcursor->execute();
	my $dbrow=$dbcursor->fetchrow_hashref();
	my $name=$dbrow->{'Name'};
	$dbcursor->finish();
	print "<br><textarea name=\"message\" rows=\"15\" cols=\"60\">";
	print "Dear Worship Team Members,\n";
	print "Please find attached the most recent worship rota for $startbitz[2]/$startbitz[1]/$startbitz[0] to $endbitz[2]/$endbitz[1]/$endbitz[0] for ";
	foreach $serv (@servs) { print "$serv "; }
	print "services.\n";
	print "The most up-to-date rota can always be viewed from within the Rota Manager section of our Service Planning system at $url\n";
	print "Please visit $url/cgi-bin/mydet.cgi to view your own personal commitments over this period. If you are unable to fulfill any of your commitments then please indicate this on the form at $url/cgi-bin/mydet.cgi or let me know personally. This way we can attempt to get someone else to fill in.\n";
	print "Please get in touch with me if you have any other issues regarding this rota.\n";
	print "$name.\n";
	print "</textarea>\n";
	print "<input type=SUBMIT value=\"Send Email\"><br><br><br>\n";
	print "<input type=hidden name=\"start\" value=\"$start\">\n";
	print "<input type=hidden name=\"end\" value=\"$end\">\n";
	print "<input type=hidden name=\"services\" value=\"$services\">\n";
	print "</td>\n";
	print "<td valign=top>\n";
	print "Please select the team members to whom you wish to send the rota.<br><br>\n";
	$dbcursor=$dbh->prepare("SELECT Name, Email FROM Team WHERE Email<>'Unknown'");
	$dbcursor->execute();
	while($dbrow=$dbcursor->fetchrow_hashref())
	{
		my $name=$dbrow->{'Name'};
		my $email=$dbrow->{'Email'};
		print "<input type=checkbox name=\"$name\" value=1 checked>&nbsp;$name &lt;$email&gt;<br>\n";
	}
	$dbcursor->finish();
	print "</td>\n";
	print "</tr>\n";
	print "</table>\n";
}
