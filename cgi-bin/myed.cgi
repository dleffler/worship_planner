#!/usr/bin/perl

use config;
use common;
use DBI;
use CGI header,param;

my $username=$ENV{'REMOTE_USER'};
my $dbname=$username;
$dbname =~ s/\'/\\\'/g ;
my $dbcursor=$dbh->prepare("SELECT * FROM Team WHERE Username='$dbname'");
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
print "<head><title>Edit My Details</title></head>\n";
print "<body>\n";
if ($noframes) { TopTable("mydet"); }
print "</body></html>\n";
print "<form action=\"myed1.cgi";
print "?noframes" if ($noframes);
print "\" method=\"POST\">\n";
print "Name:\n";
print "<input name=memname type=TEXT size=30 maxlength=40 value=\"$name\"> (in case we spelt it wrong)\n";
print "<br>Telephone number:\n";
print "<input name=telnum type=TEXT size=20 maxlength=15 value=\"$telnum\">\n";
print "<br>Email address:\n";
print "<input name=email type=TEXT size=30 maxlength=60 value=\"$email\">\n";
print "<br>If you wish to change your password please enter your new one here:\n";
print "<input name=pass1 type=PASSWORD size=20 maxlength=20>\n";
print "<br>Re-enter your new password:\n";
print "<input name=pass2 type=PASSWORD size=20 maxlength=20>\n";
print "<br>Privilege level: $privlevels[$priv] (sorry, you can't update your own privilege level)\n";
print "<br>Comma separated list of musical instruments you play and any other roles you fill within the team.<br>\n";
print "<input name=roles type=TEXT size=30 maxlength=255 value=\"$roles\"><br>\n";
GetRoles();
PrintRoles();
print "<input name=\"oldname\" type=HIDDEN value=\"$name\">\n";
print "<CENTER><br>\n";
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
