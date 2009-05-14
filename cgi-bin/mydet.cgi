#!/usr/bin/perl

use CGI::Carp qw (fatalsToBrowser);
use config;
use CGI header;
use common;

my $username=$ENV{'REMOTE_USER'};
my $dbuser=$username;
$dbuser =~ s/\'/\\\'/g ;

my $dbcursor=$dbh->prepare("SELECT * FROM Team WHERE Username='$username'");
$dbcursor->execute();
my $dbrow=$dbcursor->fetchrow_hashref();
my $name=$dbrow->{'Name'};
my $roles=$dbrow->{'Roles'};
my $telnum=$dbrow->{'Telephone'};
my $email=$dbrow->{'Email'};
my $priv=$dbrow->{'Privilege'};

$telnum="Unknown" if ($telnum eq "");
$email="Unknown" if ($email eq "");

print header();
print "<html>\n";
print $myheader;
print "<head><title>My Details</title></head>\n";
print "<body>\n";
if ($noframes) { TopTable("team"); }
print "<h1>$name\'s Details</h1>\n";
print "<p>Your recorded details are:\n";
print "<center>\n";
print "<table cellspacing=10 border=\"0\">\n";
print "<tr>\n";
print "<td align=\"left\" valign=\"top\">\n";
print "Name: $name<br>\n";
print "Tel: $telnum<br>\n";
print "Email: $email<br>\n";
print "Privilege: $privlevels[$priv]<br>\n";
print "Roles: $roles\n";
print "</td>\n";
print "<td align=\"left\" valign=\"top\">\n";
print "Current Responsibilities:<br>\n";

$_ = $dbrow->{'Roles'};
split /,/ ;
my $i;
for($i=0;$i<(scalar @_);$i++)
{
	while ((substr $_[$i],0,1) eq " ")
	{
		$_[$i] = (substr $_[$i],1);
	}
	while ((substr $_[$i],(length $_[$i])) eq " ")
	{
		$_[$i] = (substr $_[$i],0,(length $_[$i]));
	}
	if($i != 0) { print "<br>"; }
	print "<b>$_[$i]</b>: ";
	my $rolecursor=$dbh->prepare("SELECT Role, Team, Main, Sub1, Sub2, Sub3, Sub4 FROM TeamStruct WHERE Role='$_[$i]' AND (Main='$name' OR Sub1='$name' OR Sub2='$name' OR Sub3='$name' OR Sub4='$name')");
	$rolecursor->execute();
	my $numroles=0;
	while (my $rolerow=$rolecursor->fetchrow_hashref())
	{
		my $team = $rolerow->{'Team'};
		if($numroles != 0) { print ", "; }
		if($rolerow->{'Main'} eq $name) { print "Main Member in $team"; }
		elsif($rolerow->{'Sub1'} eq $name) { print "Sub1 in $team"; }
		elsif($rolerow->{'Sub2'} eq $name) { print "Sub2 in $team"; }
		elsif($rolerow->{'Sub3'} eq $name) { print "Sub3 in $team"; }
		elsif($rolerow->{'Sub4'} eq $name) { print "Sub4 in $team"; }
		$numroles++;
	}
	$rolecursor->finish();
	if ($numroles == 0) { print "unallocated"; }
}
print "</td></tr>\n";
print "<tr>\n";
print "<td align=\"center\" valign=\"top\">\n";
print "<a href=\"myed.cgi?noframes\">" if ($noframes);
print "<a href=\"myed.cgi\" target=\"Work\">" if (!$noframes);
print "Edit Details</a><br>\n";
print "</td>\n";
print "<td align=\"left\" valign=\"top\">\n";
print "<a href=\"myrota.cgi?noframes\">" if ($noframes);
print "<a href=\"myrota.cgi\" target=\"Work\">" if (!$noframes);
print "View Rota and Advise any Absences</a><br>\n";
print "</td>\n";
print "</tr>\n";
print "</table>\n";
print "</center>\n";
print "</body></html>\n";
