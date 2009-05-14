#!/usr/bin/perl

use CGI::Carp qw(fatalsToBrowser);
use config;
use common;
use DBI;
use CGI header,param;

my $format=param("format");

print header();
print "<html>\n";
print $myheader;
print "<head><title>Team Summary</title></head>\n";
print "<body>\n";
if ($noframes) { TopTable("team"); }
if ($format eq "teams") { ShowTeams(); }
elsif ($format eq "people") { ShowPeeps(); }
elsif ($format eq "roles") { ShowRoles(); }
else { print "<p>Unrecognised format.\n"; }
print "</body></html>\n";

sub ShowTeams
{
	print "<CENTER>\n";
	my $numpeeps=0;
	my $first=1;
	my $team="";
	$dbcursor=$dbh->prepare("SELECT * FROM TeamStruct ORDER BY Team");
	$dbcursor->execute();
	while ($dbrow=$dbcursor->fetchrow_hashref())
	{
		if($dbrow->{'Team'} ne $team)
		{
			if($first != 1)
			{
				print "</table><br><br>\n";
			}
			$first = 0;
			$team = $dbrow->{'Team'};
			print "<font size=\"+2\">Team Structure for $team</font>\n";
			print "<table border=\"1\" style=\"border-collapse: collapse\">\n";
			print "<tr><th>Role</th><th>Main Person</th><th>Sub 1</th><th>Sub 2</th><th>Sub 3</th><th>Sub 4</th></tr>\n";
		}
		$numpeeps++;
		print "<tr>\n";
		print "<td>".$dbrow->{'Role'}."&nbsp;</td>\n";
		print "<td>".$dbrow->{'Main'}."&nbsp;</td>\n";
		print "<td>".$dbrow->{'Sub1'}."&nbsp;</td>\n";
		print "<td>".$dbrow->{'Sub2'}."&nbsp;</td>\n";
		print "<td>".$dbrow->{'Sub3'}."&nbsp;</td>\n";
		print "<td>".$dbrow->{'Sub4'}."&nbsp;</td>\n";
		print "</tr>\n";
	}
	$dbcursor->finish();
	print "</table></center>\n";
}

sub ShowPeeps
{
	print "<font size=\"+2\">List of Team Members</font><br><br>\n";
	my $dbcursor=$dbh->prepare("SELECT Name, Roles FROM Team ORDER BY Name");
	$dbcursor->execute();
	while(my $dbrow=$dbcursor->fetchrow_hashref())
	{
		my $memname=$dbrow->{'Name'};
		print "$memname - ";
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
			if($i != 0) { print ", "; }
			print "<b>$_[$i]</b>: ";
			my $rolecursor=$dbh->prepare("SELECT Role, Team, Main, Sub1, Sub2, Sub3, Sub4 FROM TeamStruct WHERE Role='$_[$i]' AND (Main='$memname' OR Sub1='$memname' OR Sub2='$memname' OR Sub3='$memname' OR Sub4='$memname')");
			$rolecursor->execute();
			my $numroles=0;
			while (my $rolerow=$rolecursor->fetchrow_hashref())
			{
				my $team = $rolerow->{'Team'};
				if($numroles != 0) { print ", "; }
				if($rolerow->{'Main'} eq $memname) { print "Main Member in $team"; }
				elsif($rolerow->{'Sub1'} eq $memname) { print "Sub1 in $team"; }
				elsif($rolerow->{'Sub2'} eq $memname) { print "Sub2 in $team"; }
				elsif($rolerow->{'Sub3'} eq $memname) { print "Sub3 in $team"; }
				elsif($rolerow->{'Sub4'} eq $memname) { print "Sub4 in $team"; }
				$numroles++;
			}
			$rolecursor->finish();
			if ($numroles == 0) { print "unallocated"; }
		}
		print "<br>\n";
	}
	$dbcursor->finish();
}

sub ShowRoles
{
	print "<font size=\"+2\">List of Team Roles</font><br><br>\n";
	GetRoles();
	while (($role,$value) = each %roles)
	{
		print "$role - ";
		my $dbcursor=$dbh->prepare("SELECT Name, Roles FROM Team WHERE Roles LIKE '\%$role\%'");
		$dbcursor->execute();
		my $numpeeps=0;
		while (my $dbrow=$dbcursor->fetchrow_hashref())
		{
			if ($numpeeps != 0) { print ", "; }
			$numpeeps++;
			my $memname=$dbrow->{'Name'};
			print "<b>$memname</b>: ";
			my $rolecursor=$dbh->prepare("SELECT Role, Team, Main, Sub1, Sub2, Sub3, Sub4 FROM TeamStruct WHERE Role='$role' AND (Main='$memname' OR Sub1='$memname' OR Sub2='$memname' OR Sub3='$memname' OR Sub4='$memname')");
			$rolecursor->execute();
			my $numroles=0;
			while (my $rolerow=$rolecursor->fetchrow_hashref())
			{
				my $team = $rolerow->{'Team'};
				if($numroles != 0) { print ", "; }
				if($rolerow->{'Main'} eq $memname) { print "Main Member in $team"; }
				elsif($rolerow->{'Sub1'} eq $memname) { print "Sub1 in $team"; }
				elsif($rolerow->{'Sub2'} eq $memname) { print "Sub2 in $team"; }
				elsif($rolerow->{'Sub3'} eq $memname) { print "Sub3 in $team"; }
				elsif($rolerow->{'Sub4'} eq $memname) { print "Sub4 in $team"; }
				$numroles++;
			}
			$rolecursor->finish();
			if ($numroles == 0) { print "unallocated"; }
		}
		print "<br>\n";
	}
}
