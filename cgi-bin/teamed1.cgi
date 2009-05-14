#!/usr/bin/perl

use CGI::Carp qw(fatalsToBrowser);
use config;
use common;
use DBI;
use CGI header,param;

CheckPriv("Edit Team Member","team",1);

my $name=param("name");
my $dbcursor=$dbh->prepare("SELECT * FROM Team WHERE Name='$name'");
$dbcursor->execute();
my $dbrow=$dbcursor->fetchrow_hashref();
my $roles=$dbrow->{'Roles'};
my $telnum=$dbrow->{'Telephone'};
my $email=$dbrow->{'Email'};
my $priv=$dbrow->{'Privilege'};

$telnum="Unknown" if ($telnum eq "");
$email="Unknown" if ($email eq "");

print header();
print "<html>\n";
print $myheader;
print "<head><title>Team Manager</title></head>\n";
print "<body>\n";
if ($noframes) { TopTable("team"); }
print "</body></html>\n";
print "<form action=\"teamed2.cgi";
print "?noframes" if ($noframes);
print "\" method=\"POST\">\n";
print "Edit the member's name:\n";
print "<input name=memname type=TEXT size=30 maxlength=40 value=\"$name\">\n";
print "<br>Enter their telephone number:\n";
print "<input name=telnum type=TEXT size=20 maxlength=15 value=\"$telnum\">\n";
print "<br>Enter their email address:\n";
print "<input name=email type=TEXT size=30 maxlength=60 value=\"$email\">\n";
print "<br>Select this person's privilege level:\n";
print "<select name=priv><option value=\"0\"";
print " selected" if ($priv == 0);
print ">member<option value=\"1\"";
print " selected" if ($priv == 1);
print ">leader";
print "<option value=\"2\" selected>admin" if ($priv == 2);
print "</select>\n";
print "<br>Enter a comma separated list of musical instruments this member plays and any other roles they fill within the team.<br>\n";
print "<input name=roles type=TEXT size=30 maxlength=255 value=\"$roles\"><br>\n";
GetRoles();
PrintRoles();
print "<input name=\"oldname\" type=HIDDEN value=\"$name\">\n";
print "<CENTER>\n";
print "<INPUT TYPE=SUBMIT VALUE=\"Submit Editted Details\">\n";
print "</CENTER>\n";
print "</FORM>\n";

sub PrintRoles
{
	print "Current instruments / roles are ";
	my $rolenum=0;
	while (($hashname, $value) = each %roles)
	{
		if ($rolenum != 0) { print ", "; }
		$rolenum=1;
		print "$hashname";
	}
	print ". Or feel free to create your own.\n";
}
