#!/usr/bin/perl

use CGI::Carp qw(fatalsToBrowser);
use config;
use DBI;
use CGI header,param;
use common;

CheckPriv("Manage Team Structure","team",1);

my $team=param("team");
if (param("newname") ne "") { $team=param("newname"); }
my $dbteam=$team;
$dbteam =~ s/\'/\\\'/g ;

GetRoles();
my @names;
my $dbcursor=$dbh->prepare("SELECT Name FROM Team ORDER BY Name");
$dbcursor->execute();
my $numnames=0;
while (my $dbrow=$dbcursor->fetchrow_hashref())
{
	$names[$numnames] = $dbrow->{'Name'};
	$numnames++;
}
$dbcursor->finish();

print header();
print "<html>\n";
print $myheader;
print "<head><title>Manage Team Structure</title></head>\n";
print "<body>\n";
if ($noframes) { TopTable("team"); }
print "</body></html>\n";
print "<form action=\"teamstruct2.cgi";
print "?noframes" if ($noframes);
print "\" method=\"POST\">\n";
print "<CENTER>\n";
print "<font size=\"+2\">Team Structure for $team</font>\n";
print "<table border=\"1\" style=\"border-collapse: collapse\">\n";
print "<tr><th>Role</th><th>Main Person</th><th>Sub 1</th><th>Sub 2</th><th>Sub 3</th><th>Sub 4</th><th>Delete?</th></tr>\n";
my $numpeeps=0;
$dbcursor=$dbh->prepare("SELECT * FROM TeamStruct WHERE Team='$dbteam'");
$dbcursor->execute();
while ($dbrow=$dbcursor->fetchrow_hashref())
{
	$numpeeps++;
	print "<tr>\n";
	print "<input type=hidden name=\"oldrole$numpeeps\" value=\"";
	print $dbrow->{'Role'};
	print "\">\n";
	print "<td><select name=\"role$numpeeps\">\n";
	print "<option value=\"\">&nbsp;\n";
	while (($role, $value) = each %roles)
	{
		print "<option value=\"$role\"";
		print " selected" if ($role eq $dbrow->{'Role'});
		print ">$role\n";
	}
	print "</select></td>\n";
	NameList("default$numpeeps", $dbrow->{'Main'});
	NameList("sub1$numpeeps", $dbrow->{'Sub1'});
	NameList("sub2$numpeeps", $dbrow->{'Sub2'});
	NameList("sub3$numpeeps", $dbrow->{'Sub3'});
	NameList("sub4$numpeeps", $dbrow->{'Sub4'});
	print "<td><input type=checkbox name=\"delete$numpeeps\" value=1>Delete</td>\n";
	print "</tr>\n";
}
$dbcursor->finish();

my $i;
for($i=0;$i<5;$i++)
{
	$numpeeps++;
	print "<tr>\n";
	print "<td><select name=\"role$numpeeps\">\n";
	print "<option value=\"\">&nbsp;\n";
	while (($role, $value) = each %roles)
	{
		print "<option value=\"$role\">$role\n";
	}
	print "</select></td>\n";
	NameList("default$numpeeps", "");
	NameList("sub1$numpeeps", "");
	NameList("sub2$numpeeps", "");
	NameList("sub3$numpeeps", "");
	NameList("sub4$numpeeps", "");
	print "<td><input type=checkbox name=\"delete$numpeeps\" value=1>Delete</td>\n";
	print "</tr>\n";
}
print "</table>\n";
print "<INPUT NAME=team TYPE=HIDDEN VALUE=\"$team\">\n";
print "<INPUT TYPE=SUBMIT VALUE=\"Submit Team\">\n";
print "</CENTER>\n";
print "</FORM>\n";

sub NameList()
{
	my $selname=shift;
	my $selected=shift;

	print "<input type=hidden name=\"old$selname\" value=\"$selected\">\n";
	print "<td><select name=\"$selname\">\n";
	print "<option value=\"\">&nbsp;\n";
	my $i;
	for ($i=0; $i<(scalar @names); $i++)
	{
		print "<option value=\"$names[$i]\"";
		print " selected" if ($names[$i] eq $selected);
		print ">$names[$i]\n";
	}
	print "</select></td>\n";
}
