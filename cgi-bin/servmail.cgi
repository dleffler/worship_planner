#!/usr/bin/perl

use CGI header,param;
use config;
use common;
use servcommon;
use DBI;
use Mail::Sender;

CheckPriv("Service Planner", "index",2);

$servstring = param("servstring");
$date = param("date");
$service = param("service");

my $user = $ENV{'REMOTE_USER'};
my $sender;

#Generate the list of emails
my $maillist = "";
my @nosend;
my $dbcursor = $dbh->prepare("SELECT Name, Email, Telephone, Username FROM Team");
$dbcursor->execute();
my $first = 0;
while(my $dbrow = $dbcursor->fetchrow_hashref())
{
	my $name = $dbrow->{'Name'};
	my $email = $dbrow->{'Email'};
	my $telnum = $dbrow->{'Telephone'};
	my $username = $dbrow->{'Username'};
	$sender = $email if($username eq $user);
	if(param($name) == 1)
	{
		if($first !=0) { $maillist = $maillist."," };
		$first = 1;
		$maillist = $maillist.$email;
	}
	else
	{
		push @nosend, "$name Tel:$telnum Email:$email";
	}
}
$dbcursor->finish();
if (param("email")) 
{
	if($first !=0) { $maillist = $maillist."," };
  $maillist .= param("email");
}

#Create the html rota attachment
#my $outfile="$tempdir/$servstring.html";
#open OUTFILE, ">$outfile" or ReportError("Could not create Temp File","rota");
#select OUTFILE;
my $mailhtml .= param("message");
$mailhtml =~ s/\r?\n/<br>/g;
$mailhtml =  "<html>\n<body>\n$mailhtml<br><hr>";
$mailhtml .= Printable();
$mailhtml .= "<br><hr>\n";
my $mailhtml1 = PrintTxt();
$mailhtml1 =~ s/\r?\n/<br>/g;
$mailhtml .= $mailhtml1 . "</body>\n</html>\n";
#select STDOUT;
#close OUTFILE;
my $mailtext = param("message") . "\n\n" . PrintTxt();
my $mailmime = genMime($mailtext, $mailhtml);

#begin the web page
print header();
print "<html>\n";
print $myheader;
print "<head><title>Order(s) for $servstring Service(s)</title></head>\n";
print "<body>\n";

#Send the email
#my $message=new Mail::Sender {smtp => $mailserver, from => $sender};
#$message->Open({ to => $maillist, subject => "Order for $servstring Service"});
#$message->SendLine($mailmime);
#$message->Close();

SmtpSendMail($sender, $mailserver, $maillist, $mailserver, "Order for $servstring Service", $mailmime);
#$message->MailFile({to => $maillist, subject => "Order for $servstring Service", msg => param("message"), file => $outfile});
#my $done=`rm $outfile`;

if ($noframes) { TopTable("index"); }
print "<p>Mail Sent from $sender to $maillist\n";
print "<p>Click the continue button below for a printable copy of the service order.\n";
print "<form action=\"servmail1.cgi";
print "?noframes" if ($noframes);
print "\" method=\"POST\">\n";
print "<INPUT type=hidden name=\"servstring\" value=\"$servstring\">\n";
print "<INPUT type=hidden name=\"date\" value=\"$date\">\n";
print "<INPUT type=hidden name=\"service\" value=\"$service\">\n";
print "<INPUT TYPE=SUBMIT VALUE=\"Continue\">\n";
ShowHidden();
print "</CENTER>\n";
print "</FORM>\n";

print "<p>Click the Service Planner button below to return to that page.\n";
print "<form action=\"servicepick.cgi";
print "?noframes" if ($noframes);
print "\" method=\"POST\">\n";
print "<INPUT TYPE=SUBMIT VALUE=\"Service Planner\">\n";
print "</CENTER>\n";
print "</FORM>\n";

print "</body>\n</html>\n";

sub Whinge
{
}
