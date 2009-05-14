#!/usr/bin/perl

use CGI::Carp qw(fatalsToBrowser);
use config;
use common;
use DBI;
use CGI header,param;
use rotacommon;
use Mail::Sender;

CheckPriv("Rota Manager", "rota",2);

$start=param("start");
$end=param("end");
$services=param("services");
@servs=split /;/, $services;
@startbitz=split /-/, $start;
@endbitz=split /-/, $end;

$fromyear=$startbitz[0];
$fromyear =~ s/^0//g ;
$frommonth=$startbitz[1];
$frommonth =~ s/^0//g ;
$fromday=$startbitz[2];
$fromday =~ s/^0//g ;
$toyear=$endbitz[0];
$toyear =~ s/^0//g ;
$tomonth=$endbitz[1];
$tomonth =~ s/^0//g ;
$today=$endbitz[2];
$today =~ s/^0//g ;

$user=$ENV{'REMOTE_USER'};

#Generate the list of emails
$maillist="";
$dbcursor=$dbh->prepare("SELECT Name, Email, Telephone, Username FROM Team");
$dbcursor->execute();
$first=0;
while($dbrow=$dbcursor->fetchrow_hashref())
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

#Create the html rota attachment
$outfile="$tempdir/rota.html";
open OUTFILE, ">$outfile" or ReportError("Could not create Temp File","rota");
select OUTFILE;
print "<html>\n";
print $myheader;
print "<head><title>Rota Manager</title></head>\n";
print "<body>\n";
Printable();
select STDOUT;
close OUTFILE;

print header();
print "<html>\n";
print $myheader;
print "<head><title>Rota Manager</title></head>\n";
print "<body>\n";

#Send the email
$message=new Mail::Sender {smtp => $mailserver, from => $sender};
$message->MailFile({to => $maillist, subject => 'Worship Rota', msg => param("message"), file => $outfile});
$done = `rm $outfile`;
if ($noframes) { TopTable("rota"); }
print "<p>Mail Sent from $sender to $maillist\n";
print "<p>The following people did not receive the rota. Please get in touch with those whom you wish to receive the rota and let them know their responsibilities or give them a printed copy.\n";
print "<p>\n";
foreach $person ( @nosend )
{
	print "$person<br>\n";
}
print "<p>Click the continue button below for a printable copy of the rota.\n";
print "</body>\n";
print "<form action=\"rotamail1.cgi";
print "?noframes" if ($noframes);
print "\" method=\"POST\">\n";
print "<INPUT type=hidden name=\"start\" value=\"$fromyear-$frommonth-$fromday\">\n";
print "<INPUT type=hidden name=\"end\" value=\"$toyear-$tomonth-$today\">\n";
print "<INPUT type=hidden name=\"services\" value=\"";
foreach $service (@chosenservs)
{
	$service =~ s/;/:/g ;
	print "$service;";
}
print "\">\n";
print "<INPUT TYPE=SUBMIT VALUE=\"Continue\">\n";
print "</CENTER>\n";
print "</FORM>\n";
