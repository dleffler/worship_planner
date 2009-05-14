#!/usr/bin/perl

use CGI::Carp qw(fatalsToBrowser);
use config;
use common;
use DBI;
use CGI header,param;
use Mail::Sender;

print header();
print "<html>\n";
print $myheader;
print "<head><title>Email Team</title></head>\n";
print "<body>\n";

my $maillist=param("maillist");
my $subject=param("subject");
my $message=param("message");
my $sender=param("sender");

#Send the email
my $email=new Mail::Sender {smtp => $mailserver, from => $sender};
$email->MailMsg({to => $maillist, subject => $subject, msg => $message});
if ($noframes) { TopTable("team"); }
print "<p>Mail Sent from $sender to $maillist using $mailserver\n";
print "</body></html>\n";
