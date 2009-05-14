#!/usr/bin/perl

use CGI::Carp qw(fatalsToBrowser);
use config;
use common;
use DBI;
use CGI header,param;

my $user = $ENV{'REMOTE_USER'};
print header();
print "<html>\n";
print $myheader;
print "<head><title>Email Team</title></head>\n";
print "<body>\n";
if ($noframes) { TopTable("team"); }

#Generate the list of emails
my $maillist="";
my @nosend;
my $dbcursor=$dbh->prepare("SELECT Name, Email, Telephone, Username FROM Team");
$dbcursor->execute();
my $first=0;
while(my $dbrow=$dbcursor->fetchrow_hashref())
{
	my $name=$dbrow->{'Name'};
	my $email=$dbrow->{'Email'};
	my $telnum=$dbrow->{'Telephone'};
	my $username=$dbrow->{'Username'};
	$sender = $email if($username eq $user);
	if(param($name) == 1)
	{
		if($first !=0) { $maillist=$maillist."," };
		$first=1;
		$maillist=$maillist.$email;
	}
	else
	{
		push @nosend, "$name Tel:$telnum Email:$email";
	}
}
$dbcursor->finish();

print "</body>\n";
print "<form action=\"teammail2.cgi";
print "?noframes" if ($noframes);
print "\" method=\"POST\">\n";
print "<p align=center><font size=+2>Email Team</font></p>\n";
print "<p>Below is a preview of your message. Click the back button on your browser if you wish to amend anything.<br>\n";
print "These are the people to whom this message will be sent. Please copy and paste the list of emails into your mail client if you need to send an attachment to them.</p>\n";
print "<p><b>$maillist</b></p>\n";
my $subject=param("subject");
print "Subject: $subject<br>\n";
my $message=param("message");
my $mungedMessage = $message;
$mungedMessage =~ s/\n/<br>/g ;
print "$mungedMessage\n";
print "<input type=hidden name=maillist value=\"$maillist\">\n";
print "<input type=hidden name=subject value=\"$subject\">\n";
print "<input type=hidden name=message value=\"$message\">\n";
print "<input type=hidden name=sender value=\"$sender\">\n";
print "<input type=SUBMIT value=\"Send Email\"><br><br><br>\n";
