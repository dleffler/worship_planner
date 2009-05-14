#!/usr/bin/perl

use CGI::Carp qw(fatalsToBrowser);
use config;
use common;
use DBI;
use CGI header,param;

my $wholeteam = (param("name0") eq "") ? 1 : 0;

print header();
print "<html>\n";
print $myheader;
print "<head><title>Email Team</title></head>\n";
print "<body>\n";
if ($noframes) { TopTable("team"); }
print "</body>\n";
print "<form action=\"teammail1.cgi";
print "?noframes" if ($noframes);
print "\" method=\"POST\">\n";
print "<p align=center><font size=+2>Email Team</font></p>\n";
print "<p>Please note that this system does not currently support the sending of attachments. If you wish to send anything more complicated than a plain text email then select your recipients below and click continue. You will then be given a list of email addresses that you can copy and paste into your email client</p>\n";
print "<table border=\"0\" width=\"100%\">\n";
print "<tr>\n";
print "<td valign=top>\n";
#If this email is to the team involved in a particular service then display them in the left column
my %involved;
if($wholeteam == 0)
{
	print "These are the team members involved.<br>Check the box beside those you wish to email.<br>\n";
	my $counter=0;
	my $person=param("name$counter");
	while($person ne "")
	{
		if (($person ne "blank") && ($involved{$person} eq ""))
		{
			my $dbcursor=$dbh->prepare("SELECT Email, Telephone FROM Team WHERE Name='$person'");
			$dbcursor->execute();
			my $dbrow=$dbcursor->fetchrow_hashref();
			my $email=$dbrow->{'Email'};
			my $telephone=$dbrow->{'Telephone'};
			$involved{$person}=$email;
			if($email eq "Unknown")
			{
				print "$person - Tel:$telephone does not have a recorded email address.<br>\n";
			}
			else
			{
				print "<input type=checkbox name=\"$person\" value=1 checked>&nbsp;$person &lt;$email&gt;<br>\n";
			}
		}
		$counter++;
		$person=param("name$counter");
	}
}
my $subject=param("subject");
print "Subject: <input type=text name=\"subject\" size=40 maxlength=80 value=\"$subject\"><br>\n";
print "Enter your message below:-\n";
my $user = $ENV{'REMOTE_USER'};
my $dbcursor=$dbh->prepare("SELECT Name, Username FROM Team WHERE Username='$user'");
$dbcursor->execute();
my $dbrow=$dbcursor->fetchrow_hashref();
my $name=$dbrow->{'Name'};
$dbcursor->finish();
print "<br><textarea name=\"message\" rows=\"15\" cols=\"60\">";
print "Dear Team,\n";
print "\n";
print "$name.\n";
print "</textarea>\n";
print "<input type=SUBMIT value=\"Continue\"><br><br><br>\n";
print "</td>\n";
print "<td valign=top>\n";
print "Please select any other worship team members to whom you wish to send this email.<br><br>\n" if ($wholeteam == 0);
print "Please select the worship team members to whom you wish to send this email.<br><br>\n" if ($wholeteam == 1);
$dbcursor=$dbh->prepare("SELECT Name, Email FROM Team WHERE Email<>'Unknown'");
$dbcursor->execute();
while($dbrow=$dbcursor->fetchrow_hashref())
{
	my $name=$dbrow->{'Name'};
	my $email=$dbrow->{'Email'};
	if(($wholeteam == 1) || ($involved{$name} eq ""))
	{
		print "<input type=checkbox name=\"$name\" value=1";
		print " checked" if ($wholeteam);
		print ">&nbsp;$name &lt;$email&gt;<br>\n";
	}
}
$dbcursor->finish();
print "</td>\n";
print "</tr>\n";
print "</table>\n";
