#!/usr/bin/perl

use CGI::Carp qw(fatalsToBrowser);
use config;
use common;
use tscommon;
use DBI;
use CGI param,header;

CheckPriv("Manage Team Structure","team",1);
my %approvedSongs;

my @invalids;
my @badroles;
my @changes;

$team=param("team");
$dbteam=$team;
$dbteam =~ s/\'/\\\'/g ;

print header();
print "<html>\n";
print $myheader;
print "<head><title>Team Manager</title></head>\n";
print "<body>\n";
if ($noframes) { TopTable("team"); }

ReadInputs();
ValidateInputs();
if(((scalar @invalids) > 0) || ((scalar @badroles) > 0))
{
	ShowWarning();
	HiddenForm();
}
else
{
	SubmitTeam();
	CheckChanges();
}

sub ValidateInputs
{
	my $par;
	for ($par=1;$par<(scalar @roles);$par++)
	{
		if(($deletes[$i] != 1) && ($roles[$par] ne "Team Leader"))
		{
			NameSearch($defaults[$par],$par,1) if ($defaults[$par] ne "");
			NameSearch($sub1s[$par],$par,2) if ($sub1s[$par] ne "");
			NameSearch($sub2s[$par],$par,3) if ($sub2s[$par] ne "");
			NameSearch($sub3s[$par],$par,4) if ($sub3s[$par] ne "");
			NameSearch($sub4s[$par],$par,5) if ($sub4s[$par] ne "");
		}
	}
}

sub NameSearch
{
	my $name = shift;
	my $par = shift;
	my $start = shift;
	#Make sure that no-one has been given a role for which they are not qualified
	my $dbcursor = $dbh->prepare("SELECT Roles FROM Team WHERE Name='$name'");
	$dbcursor->execute();
	my @dbrow=$dbcursor->fetchrow_array();
	if ($dbrow[0] !~ /$roles[$par]/)
	{
		push @badroles, "$name;$roles[$par]";
	}
	$dbcursor->finish();

	#Next, search to see if someone has been given more than one role within the team
	my $i;
	for($i=$par;$i<(scalar @roles);$i++)
	{
		if(($deletes[$i] != 1) && ($roles[$i] ne "Team Leader"))
		{
			if(($i > $par) || ($start > 1))
			{
				if($name eq $defaults[$i])
				{
					push @invalids, $name;
					last;
				}
			}
			if(($i > $par) || ($start > 2))
			{
				if($name eq $sub1s[$i])
				{
					push @invalids, $name;
					last;
				}
			}
			if(($i > $par) || ($start > 3))
			{
				if($name eq $sub2s[$i])
				{
					push @invalids, $name;
					last;
				}
			}
			if(($i > $par) || ($start > 4))
			{
				if($name eq $sub3s[$i])
				{
					push @invalids, $name;
					last;
				}
			}
			if(($i > $par) || ($start > 5))
			{
				if($name eq $sub4s[$i])
				{
					push @invalids, $name;
					last;
				}
			}
		}
	}
}

sub ShowWarning
{
	print "<p><b>Warning</b> - The following descrepancies exist in your team structure:</p>\n";
	print "<p>\n";
	my $i;
	for($i=0;$i<(scalar @invalids);$i++)
	{
		print "$invalids[$i] has been allocated more than one responsibility within the team.<br>\n";
	}
	for($i=0;$i<(scalar @badroles);$i++)
	{
		my @line = split /;/, $badroles[$i];
		print "$line[0] has been given the role of $line[1]. This is not listed as one of $line[0]\'s skills / roles.<br>\n";
	}
	print "<p>Use the back button on your browser and fix these, or hit the continue button, below, to force this team structure.\n";
	print "</body></html>\n";
}

sub HiddenForm
{
	print "<form action=\"teamstruct3.cgi";
	print "?noframes" if ($noframes);
	print "\" method=\"POST\">\n";
	print "<input type=hidden name=\"team\" value=\"$team\">\n";
	for($i=1;$i<(scalar @roles);$i++)
	{
		print "<input type=hidden name=\"role$i\" value=\"$roles[$i]\">\n";
		print "<input type=hidden name=\"oldrole$i\" value=\"$oldroles[$i]\">\n";
		print "<input type=hidden name=\"default$i\" value=\"$defaults[$i]\">\n";
		print "<input type=hidden name=\"olddefault$i\" value=\"$olddefaults[$i]\">\n";
		print "<input type=hidden name=\"sub1$i\" value=\"$sub1s[$i]\">\n";
		print "<input type=hidden name=\"oldsub1$i\" value=\"$oldsub1s[$i]\">\n";
		print "<input type=hidden name=\"sub2$i\" value=\"$sub2s[$i]\">\n";
		print "<input type=hidden name=\"oldsub2$i\" value=\"$oldsub2s[$i]\">\n";
		print "<input type=hidden name=\"sub3$i\" value=\"$sub3s[$i]\">\n";
		print "<input type=hidden name=\"oldsub3$i\" value=\"$oldsub3s[$i]\">\n";
		print "<input type=hidden name=\"sub4$i\" value=\"$sub4s[$i]\">\n";
		print "<input type=hidden name=\"oldsub4$i\" value=\"$oldsub4s[$i]\">\n";
		print "<input type=hidden name=\"delete$i\" value=\"$deletes[$i]\">\n";
	}
	print "<CENTER>\n";
	print "<INPUT TYPE=SUBMIT VALUE=\"Continue\">\n";
	print "</CENTER>\n";
	print "</FORM>\n";
}
