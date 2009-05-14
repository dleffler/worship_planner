#!/usr/bin/perl

# Send e-mail using new temp file, ask to see printable again?

use CGI header,param;
use config;
use common;
use servcommon;
use DBI;
use Mail::Sender;

CheckPriv("Service Order Mailer", "index",2);

#$servstring=param("servstring");
$date = param("date");
#$service=param("service");
split /-/, $date;
my $year = $_[0];
my $month = $_[1];
my $day = $_[2];
#my $daysuffix = (((substr $day, -1) == 1) && ($day != 11)) ? "st" : (((substr $day, -1) == 2) ? "nd" : "th") ;
$day = DaySuffix($day);

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
		if($first != 0) { $maillist = $maillist."," };
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
my $mailtext = ""; my $mailtext1 = "";
my $mailhtml .= param("message");
$mailhtml =~ s/\r?\n/<br>/g;
$mailhtml =  "<html>\n<body>\n$mailhtml";
for ($k=0; $k<(scalar @services); $k++) # go thorough all service types for a given date
{
  $mailhtml .= "<br><hr>\n";
  $service = $services[$k];
  $servstring = "$day $months[$month-1] $year $service";
  $mailhtml .= Printable() . "\n";
  $mailtext1 = PrintTxt();
  $mailtext1 =~ s/\r?\n/<br>\n/g;
  $mailtext .= $mailtext1 . "\n<br>\n";
}
$mailhtml .= $mailtext . "</body>\n</html>\n";
$mailtext = param("message") . "\n\n" . $mailtext;
my $mailmime = genMime($mailtext, $mailhtml);

#begin the web page
print header();
print "<html>\n";
print $myheader;
$servstring="$day $months[$month-1] $year";
print "<head><title>Order(s) for $servstring Service(s)</title></head>\n";
print "<body>\n";

#Send the email
SmtpSendMail($sender, $mailserver, $maillist, $mailserver, "Order for $servstring Service(s)", $mailmime);

if ($noframes) { TopTable("index"); }
print "<p>Mail Sent from $sender to $maillist\n";
print "<p>Click the continue button below for a printable copy of the service order.\n";
print "<form action=\"servmailx1.cgi";
print "?noframes" if ($noframes);
print "\" method=\"POST\">\n";
#print "<INPUT type=hidden name=\"servstring\" value=\"$servstring\">\n";
print "<INPUT type=hidden name=\"date\" value=\"$date\">\n";
#print "<INPUT type=hidden name=\"service\" value=\"$service\">\n";
print "<INPUT TYPE=SUBMIT VALUE=\"Continue\">\n";
for ($k=0; $k<(scalar @services); $k++) # go thorough all service types for a given date
{
  $service = $services[$k];
  $servstring = "$day $months[$month-1] $year $service";
  ShowHidden();
}
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
