#!/usr/bin/perl

use CGI::Carp qw ( fatalsToBrowser );
use config;
use common;
use DBI;
use CGI header,param;
use rotacommon;
use rotaslot;
use Date::Pcalc qw(Date_to_Days);

my $username=$ENV{'REMOTE_USER'};
my $dbuser=$username;
$dbuser =~ s/\'/\\\'/g ;
my $dbcursor=$dbh->prepare("SELECT Name FROM Team WHERE Username='$dbuser'");
$dbcursor->execute();
my $dbrow=$dbcursor->fetchrow_hashref();
my $name=$dbrow->{'Name'};
my $dbname=$name;
$dbname =~ s/\'/\\\'/g ;

DateMung();

print header();
print "<html>\n";
print $myheader;
print "<head><title>Rota Manager</title></head>\n";
print "<body>\n";
if ($noframes) { TopTable("rota"); }
print "<CENTER>\n";
print "<p>Worship Rota from $fromday/$frommonth/$fromyear to $today/$tomonth/$toyear for $name\n";

#my @rotalines;
#my @rotasorted;
#my @positions;
#my @substitutions;
#my %linehashes;

print "</CENTER>\n";
print "</body>\n";
print "<form action=\"myrota2.cgi";
print "?noframes" if ($noframes);
print "\" method=\"POST\">\n";
print "<CENTER>\n";
GetPositions();
GetRota();
SortRota();
GetSubstitutions();
DisplayRota();
print "<INPUT TYPE=SUBMIT VALUE=\"Submit Availability\">\n";
print "</CENTER>\n";
print "</form>\n";


sub GetPositions
{
	my $rolecursor=$dbh->prepare("SELECT Role, Team, Main FROM TeamStruct WHERE Main='$dbname' OR Sub1='$dbname' OR Sub2='$dbname' OR Sub3='$dbname' OR Sub4='$dbname'");
	$rolecursor->execute();
	while (my $rolerow=$rolecursor->fetchrow_hashref())
	{
		my $team = $rolerow->{'Team'};
		my $role = $rolerow->{'Role'};
		my $main = $rolerow->{'Main'};
		push @positions, "$team;$role;$main;";
		print "<! Creating Position $team;$role;$main; >\n";
	}
	$rolecursor->finish();
}

sub GetRota
{
	my $numpos=1;
	my $fromdate="$fromyear-$frommonth-$fromday";
	my $todate="$toyear-$tomonth-$today";

	foreach $position (@positions)
	{
		split /;/, $position;
		my $team=$_[0];
		my $role=$_[1];
		my $main=$_[2];
		foreach $service (@chosenservs)
		{
			my $dbcursor=$dbh->prepare("SELECT ServiceDate, Service, Team FROM Rota WHERE Team='$team' AND Service='$service' AND ServiceDate>='$fromdate' AND ServiceDate<='$todate' ORDER BY ServiceDate");
			$dbcursor->execute();
			while (my $dbrow = $dbcursor->fetchrow_hashref())
			{
				my $rotaline = rotaslot->new();
				$rotaline->servicedate($dbrow->{'ServiceDate'});
				$rotaline->service($dbrow->{'Service'});
				$rotaline->team($dbrow->{'Team'});
				$rotaline->main($main);
				$rotaline->role($role);
				push @rotalines, $rotaline;
				print "<! Created rotaline ".$dbrow->{'ServiceDate'}." ".$dbrow->{'Service'}." ".$dbrow->{'Team'}." $main $role >\n";
				my $hashindex=$dbrow->{'ServiceDate'}.";".$dbrow->{'Service'}.";$role;$main";
				$linehashes{$hashindex}=$numpos;
				$numpos++;
			}
			$dbcursor->finish();
		}
	}
}

sub SortRota
{
	my $root;
	foreach $rotaline (@rotalines)
	{
		insert($root, $rotaline);
	}
	inorder($root);
}

sub insert
{
	my ($tree, $value) = @_;
	unless ($tree)
	{
		$tree = {};
		$tree->{VALUE} = $value;
		$tree->{LEFT}  = undef;
		$tree->{RIGHT} = undef;
		$_[0] = $tree;
		return;
	}
	my $result = rotacmp($tree->{VALUE}, $value);
	if    ($result < 0) { insert ($tree->{LEFT},  $value); }
	elsif ($result > 0) { insert ($tree->{RIGHT}, $value); }
}

sub rotacmp
{
	my ($old, $new) = @_;
	my $oldDate = $old->getservicedate();
	my $newDate = $new->getservicedate();
	my $oldService = $old->getservice();
	my $newService = $new->getservice();
	my $oldRole = $old->getrole();
	my $newRole = $new->getrole();
	if($newDate ne $oldDate)
	{
		#Sort based on date
		split /-/, $oldDate;
		my $oldDays = Date_to_Days($_[0],$_[1],$_[2]);
		split /-/, $newDate;
		my $newDays = Date_to_Days($_[0],$_[1],$_[2]);
		if ($oldDays > $newDays) { return -1;}
		elsif ($oldDays < $newDays) { return 1;}
		else {return 0;}
	}
	elsif($oldService ne $newService)
	{
		#Sort based on Service
		my $oldService = $old->getservice();
		my $newService = $new->getservice();
		if ($oldService eq $newService) { return 0;}
		my $oldPos,$newPos;
		my $i;
		for($i=0;$i<(scalar @services);$i++)
		{
			if ($oldService eq $services[$i]) { $oldPos = $i; }
			if ($newService eq $services[$i]) { $newPos = $i; }
		}
		if ($oldPos > $newPos) { return -1;}
		elsif ($oldPos < $newPos) { return 1;}
		else {return 0;}
	}
	elsif($oldRole ne $newRole)
	{
		if ($oldRole gt $newRole) { return -1;}
		elsif ($oldRole lt $newRole ) { return 1;}
		else {return 0;}
	}
	else
	{
		return 0;
	}
}

sub inorder
{
	my $tree = shift;
	return unless $tree;
	inorder($tree->{LEFT});
	push @rotasorted, $tree->{VALUE};
	inorder($tree->{RIGHT});
}

sub GetSubstitutions
{
	foreach $rotaline (@rotasorted)
	{
		my $servicedate = $rotaline->getservicedate();
		my $service = $rotaline->getservice();
		my $role = $rotaline->getrole();
		my $main = $rotaline->getmain();
		my $dbcursor=$dbh->prepare("SELECT Sub FROM RotaSub WHERE ServiceDate='$servicedate' AND Service='$service' AND Role='$role' AND Main='$main'");
		$dbcursor->execute();
		while (my $dbrow=$dbcursor->fetchrow_hashref())
		{
			my $substitute = $dbrow->{'Sub'};
			$rotaline->substitute($substitute);
		}
		$dbcursor->finish();
	}
}

sub DisplayRota
{
	print "<table border=\"1\" style=\"border-collapse: collapse\">\n";
	print "<tr><th>Date</th><th>Service</th><th>Role</th><th>I'll Be There</th><th>No Can Do</th></tr>\n";

	my $linenum=1;
	foreach $rotaline (@rotasorted)
	{
		my $servicedate = $rotaline->getservicedate();
		my $service = $rotaline->getservice();
		my $team = $rotaline->getteam();
		my $role = $rotaline->getrole();
		my $rotamain = $rotaline->getmain();
		my $rotasub = $rotaline->getsubstitute();
		my $lineindex="$servicedate;$service;$role;$rotamain";
		split /-/, $servicedate;
		my ($thisyear, $thismonth, $thisday)=@_;
		if (($rotamain eq $name) && ($rotasub eq ""))
		{
			#I'll Be There
			print "<tr><td>$thisday/$thismonth/$thisyear</td><td>$service</td><td>$role</td><td><input type=radio name=\"available$linenum\" value=\"1\" checked></td><td><input type=radio name=\"available$linenum\" value=\"0\"><input type=hidden name=\"index$linenum\" value=\"$lineindex\"><input type=hidden name=\"oldval$linenum\" value=\"1\"></td>\n";
		}
		elsif (($rotamain eq $name) && ($rotasub ne ""))
		{
			#I'll Not be there
			print "<tr><td>$thisday/$thismonth/$thisyear</td><td>$service</td><td>$role</td><td><input type=radio name=\"available$linenum\" value=\"1\"></td><td><input type=radio name=\"available$linenum\" value=\"0\" checked><input type=hidden name=\"index$linenum\" value=\"$lineindex\"><input type=hidden name=\"oldval$linenum\" value=\"0\"></td>\n";
		}
		elsif (($rotamain ne $name) && ($rotasub ne ""))
		{
			my $rotasublevel = substr $rotasub, 3;
			my $dbcursor=$dbh->prepare("SELECT * FROM TeamStruct WHERE Team='$team' AND Role='$role' AND Main='$rotamain'");
			$dbcursor->execute();
			my $dbrow=$dbcursor->fetchrow_hashref();
			if($dbrow)
			{
				my $sublevel=0;
				if ($dbrow->{'Sub4'} eq $name) { $sublevel=4; }
				if ($dbrow->{'Sub3'} eq $name) { $sublevel=3; }
				if ($dbrow->{'Sub2'} eq $name) { $sublevel=2; }
				if ($dbrow->{'Sub1'} eq $name) { $sublevel=1; }
				if ($sublevel == $rotasublevel)
				{
					#I'll Be There
					print "<tr><td>$thisday/$thismonth/$thisyear</td><td>$service</td><td>$role</td><td><input type=radio name=\"available$linenum\" value=\"1\" checked></td><td><input type=radio name=\"available$linenum\" value=\"0\"><input type=hidden name=\"index$linenum\" value=\"$lineindex\"><input type=hidden name=\"oldval$linenum\" value=\"1\"></td>\n";
				}
				elsif($sublevel < $rotasublevel)
				{
					#I'll Not be there
					print "<tr><td>$thisday/$thismonth/$thisyear</td><td>$service</td><td>$role</td><td><input type=radio name=\"available$linenum\" value=\"1\"></td><td><input type=radio name=\"available$linenum\" value=\"0\" checked><input type=hidden name=\"index$linenum\" value=\"$lineindex\"><input type=hidden name=\"oldval$linenum\" value=\"0\"></td>\n";
				}
			}
			$dbcursor->finish();
		}
		$linenum++;
	}

	print "</table>\n";
}
#my $posnum=0;
#foreach $rotaline (@rotalines)
#{
#print "<br>Rotaline $posnum is ".$rotaline->getservicedate()." ".$rotaline->getservice()." ".$rotaline->getteam()." ".$rotaline->getrole()." ".$rotaline->getmain()." ".$rotaline->getsubstitute()."\n";
#$posnum++;
#}
