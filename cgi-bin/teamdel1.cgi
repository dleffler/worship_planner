#!/usr/bin/perl

use CGI::Carp qw(fatalsToBrowser);
use config;
use DBI;
use CGI param,header;
use common;

CheckPriv("Delete Team Member","team",2);

my $name=param("member");
my $error;

my $dbname=$name;
$dbname =~ s/\'/\\\'/g ;

my $numBooks=0;

print header();
print "<html>\n";
print $myheader;
print "<head><title>Team Member Delete</title></head>\n";
print "<body>\n";

if ($noframes) { TopTable("team"); }
my $dbcursor=$dbh->prepare("SELECT * FROM Team WHERE Name='$dbname'");
$dbcursor->execute();
my $dbrow=$dbcursor->fetchrow_hashref();
print "<p>You are about to delete the following team member.\n";
print "<p>$name, tel:".$dbrow->{'Telephone'}.", Email: ".$dbrow->{'Email'}.", Roles: ".$dbrow->{'Roles'}."\n";
my $username=$dbrow->{'Username'};
$dbcursor->finish();

$dbcursor=$dbh->prepare("SELECT Team, Role, Main, Sub1, Sub2, Sub3, Sub4 FROM TeamStruct WHERE Main='$dbname' OR Sub1='$dbname' OR Sub2='$dbname' OR Sub3='$dbname' OR Sub4='$dbname'");
$dbcursor->execute();
my $found=0;
while ($dbrow=$dbcursor->fetchrow_hashref())
{
	my $position = ($dbrow->{'Main'} eq $name) ? "Main Person" : (($dbrow->{'Sub1'} eq $name) ? "Sub1" : (($dbrow->{'Sub2'} eq $name) ? "Sub2" : (($dbrow->{'Sub3'} eq $name) ? "Sub3" : (($dbrow->{'Sub4'} eq $name) ? "Sub4" : ""))));
	if ($position ne "")
	{
		$found=1;
		print "<br>$name is in ".$dbrow->{'Team'}." with the role of ".$dbrow->{'Role'}." as $position.\n";
	}
}
if($found == 1)
{
	print "<p>If you choose to continue with this deletion the system will remove $name from these teams and shuffle those with lower substitution levels up one level to compensate. You are advised to check the Team Structures if you continue with this delete.\n";
}
print "</body></html>\n";
print "<form action=\"teamdel2.cgi";
print "?noframes" if ($noframes);
print "\" method=\"POST\">\n";
print "<input name=\"name\" type=hidden value=\"$name\">\n";
print "<input name=\"username\" type=hidden value=\"$username\">\n";
print "<CENTER>\n";
print "<input type=submit value=\"Delete $name\">\n";
print "</form>\n";
