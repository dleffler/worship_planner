#!/usr/bin/perl

use CGI::Carp qw(fatalsToBrowser);
use config;
use common;
use DBI;
use CGI header;

CheckPriv("Add Team Member","team",1);

print header();
print "<html>\n";
print $myheader;
print "<head><title>Team Manager</title></head>\n";
print "<body>\n";
if ($noframes) { TopTable("team"); }
print "</body></html>\n";
print "<form action=\"teamadd1.cgi";
print "?noframes" if ($noframes);
print "\" method=\"POST\">\n";
print "View current team members on this list:\n";
print "<select name=\"current\">\n";
my $dbcursor=$dbh->prepare("SELECT Name FROM Team ORDER BY Name");
$dbcursor->execute();
while (my $dbrow=$dbcursor->fetchrow_hashref())
{
	my $name=$dbrow->{'Name'};
	print "<option value=\"$name\">$name\n";
}
$dbcursor->finish();
print "</select><br>\n";
print "Enter the new member's name:\n";
print "<input name=memname type=TEXT size=30 maxlength=40>\n";
print "<br>Enter their telephone number:\n";
print "<input name=telnum type=TEXT size=20 maxlength=15 value=\"Unknown\">\n";
print "<br>Enter their email address:\n";
print "<input name=email type=TEXT size=30 maxlength=60 value=\"Unknown\">\n";
print "<br>Give this person a login name for this system:\n";
print "<input name=username type=TEXT size=20 maxlength=20>\n";
print "<br>Give this person a login password:\n";
print "<input name=pass1 type=PASSWORD size=20 maxlength=20>\n";
print "<br>Re-enter the login password:\n";
print "<input name=pass2 type=PASSWORD size=20 maxlength=20>\n";
print "<br>Select this person's privilege level:\n";
my $priv = GetPriv();
print "<select name=priv><option value=\"0\" selected>member<option value=\"1\">leader<option value=\"2\">admin</select>\n" if ($priv > 1);
print "<select name=priv><option value=\"0\" selected>member<option value=\"1\">leader</select>\n" if ($priv == 1);
print "<br>Enter a comma separated list of musical instruments this member plays and any other roles they fill within the team.<br>\n";
print "<input name=roles type=TEXT size=30 maxlength=255><br>\n";
GetRoles();
PrintRoles();
print "<CENTER><br>\n";
print "<INPUT TYPE=SUBMIT VALUE=\"Submit New Member\">\n";
print "</CENTER>\n";
print "</FORM>\n";

sub PrintRoles
{
	print "Current instruments / roles are ";
	my $rolenum=0;
	while (($name, $value) = each %roles)
	{
		if ($rolenum != 0) { print ", "; }
		$rolenum=1;
		print "$name";
	}
	print ". Or feel free to create your own.\n";
}
