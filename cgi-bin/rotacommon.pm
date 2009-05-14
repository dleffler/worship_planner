package rotacommon;

use CGI::Carp qw(fatalsToBrowser);
use config;
use common;
use CGI param,header;
use DBI;
use Date::Pcalc qw(Date_to_Days Add_Delta_Days Day_of_Week);
use base 'Exporter';
@EXPORT = qw($dbh @rotalines %lineindex Printable CreateRotaLines PopulateRotaLines GenerateTable $fromday $frommonth $fromyear $today $tomonth $toyear @chosenservs DateMung $start $end $services @servs @startbitz @endbitz);

$dbh = DBI->connect("DBI:mysql:database=$database;host=$dbHost",
                       $dbUser, $dbPasswd,
                      {'RaiseError' => 0});

sub CreateRotaLines
{
	my $numlines=0;
	my $start = Date_to_Days($fromyear,$frommonth,$fromday);
	my $end = Date_to_Days($toyear,$tomonth,$today);

	my $thisday,$thismonth,$thisyear;

	my $daynum;
	for($daynum=$start;$daynum<=$end;$daynum++)
	{
		($thisyear,$thismonth,$thisday) = Add_Delta_Days(1,1,1, $daynum - 1);
		$thisday=sprintf "%2d", $thisday;
		$thismonth=sprintf "%2d", $thismonth;
		$thisday=~ s/ /0/g ;
		$thismonth=~ s/ /0/g ;
		my $servsel;
		for($servsel=0;$servsel<(scalar @chosenservs);$servsel++)
		{
			my $dayname = $days[(Day_of_Week($thisyear,$thismonth,$thisday)-1)];
			if(($servicedays{$chosenservs[$servsel]} =~ /$dayname/) || ($servicedays{$chosenservs[$servsel]} =~ /All/))
			{
				$rotalines[$numlines]="$thisyear-$thismonth-$thisday;$chosenservs[$servsel];;;;;";
				my $index="$thisyear-$thismonth-$thisday-$chosenservs[$servsel]";
				$lineindex{$index}=$numlines;
				$numlines++;
			}
		}
	}
	return $numlines;
}

sub DateMung
{
	$fromday=param("from_day");
	$frommonth=param("from_month");
	$fromyear=param("from_year");
	$today=param("to_day");
	$tomonth=param("to_month");
	$toyear=param("to_year");
	@chosenservs=param("service");

	$fromday = ((($frommonth == 4) || ($frommonth == 6) 
				 || ($frommonth == 9) || ($frommonth == 11))
				 && ($fromday == 31)) ? 30 : $fromday ;

	$fromday = (($frommonth == 2) && ($fromday >= 29)) ? 
				  ((($fromyear % 4) == 0) ? 29 : 28 )
				  : $fromday ;
			 
	$today = ((($tomonth == 4) || ($tomonth == 6) 
				 || ($tomonth == 9) || ($tomonth == 11))
				 && ($today == 31)) ? 30 : $today ;

	$today = (($tomonth == 2) && ($today >= 29)) ? 
				  ((($toyear % 4) == 0) ? 29 : 28 )
				  : $today ;

	$today=sprintf "%2d", $today;
	$tomonth=sprintf "%2d", $tomonth;
	$fromday=sprintf "%2d", $fromday;
	$frommonth=sprintf "%2d", $frommonth;

	$today=~ s/ /0/g ;
	$tomonth=~ s/ /0/g ;
	$fromday=~ s/ /0/g ;
	$frommonth=~ s/ /0/g ;
}

sub PopulateRotaLines()
{
	my $start = sprintf "%4d-%2d-%2d", $fromyear,$frommonth,$fromday;
	$start =~ s/ /0/g ;
	my $end = sprintf "%4d-%2d-%2d", $toyear,$tomonth,$today;
	$end =~ s/ /0/g ;
	my $selstring = "SELECT * FROM Rota WHERE ServiceDate>='$start' AND ServiceDate<='$end' AND (";
	my $first=0;
	foreach $servdate (@chosenservs)
	{
		if($first != 0) { $selstring=$selstring." OR "; }
		$first=1;
		$selstring=$selstring."Service='$servdate'";
	}
	$selstring=$selstring.")";
	my $dbcursor=$dbh->prepare($selstring);
	$dbcursor->execute();
	while(my $dbrow=$dbcursor->fetchrow_hashref())
	{
		my $index=$dbrow->{'ServiceDate'}."-".$dbrow->{'Service'};
		my $linenum=$lineindex{$index};
		my $servicedate=$dbrow->{'ServiceDate'};
		$servicedate =~ s/;/:/g ;
		my $service=$dbrow->{'Service'};
		$service =~ s/;/:/g ;
		my $team=$dbrow->{'Team'};
		$team =~ s/;/:/g ;
		my $leader=$dbrow->{'Leader'};
		$leader =~ s/;/:/g ;
		my $preacher=$dbrow->{'Preacher'};
		$preacher =~ s/;/:/g ;
		my $notes=$dbrow->{'Notes'};
		$notes =~ s/;/:/g ;
		$rotalines[$linenum]="$servicedate;$service;$team;$leader;$preacher;$notes;";
		print "<!Creating Rotaline $rotalines[$linenum]>";
	}
	$dbcursor->finish();
}

sub GenerateTable
{
	my $mode=shift;
	print "<table border=\"1\" style=\"border-collapse: collapse\">\n";
	print "<tr><th>Date</th><th>Service</th><th>Team</th><th>Leader</th><th>Preacher</th><th>Notes</th></tr>\n";
	my $numlines=0;
	foreach $line (@rotalines)
	{
		$line =~ s/;;/;Empty;/g ;
		$line =~ s/;;/;Empty;/g ;
		my @linebits = split /;/, $line;
		if (($mode eq "rw") || ($linebits[2] ne "Empty") || ($linebits[3] ne "Empty") || ($linebits[4] ne "Empty") || ($linebits[5] ne "Empty") || ($linebits[1] ne "Other"))
		{
			print "<tr>\n";
			my $i=0;
			foreach $bit (@linebits)
			{
				print "<td valign=top";
				print " align=right" if($i==1);
				print ">\n";
				if($i == 0)
				{
					@bitz = split /-/, $bit;
					print "$bitz[2]-$bitz[1]-$bitz[0]\n";
					print "<input type=hidden name=\"sdate$numlines\" value=\"$bit\">\n" if ($mode eq "rw");
				}
				elsif($mode eq "rw")
				{
					if($i == 1)
					{
						print "$bit\n";
						print "<input type=hidden name=\"service$numlines\" value=\"$bit\">\n";
					}
					if($i == 2)
					{
						print "<select name=\"team$numlines\">\n";
						print "<option value=\"\">&nbsp;\n";
						my $dbcursor=$dbh->prepare("SELECT DISTINCT Team FROM TeamStruct");
						$dbcursor->execute();
						while (my $dbrow=$dbcursor->fetchrow_hashref())
						{
							my $team=$dbrow->{'Team'};
							print "<option value=\"$team\"";
							print " selected" if ($team eq $bit);
							print ">$team\n";
						}
						print "<option value=\"Misc\">Misc\n";
						print "</select>\n";
						$dbcursor->finish();
					}
					if($i == 3)
					{
						print "<select name=\"leader$numlines\">\n";
						print "<option value=\"\">&nbsp;\n";
						my $dbcursor=$dbh->prepare("SELECT Name FROM Team WHERE Roles LIKE '\%Worship Leader\%'");
						$dbcursor->execute();
						while (my $dbrow=$dbcursor->fetchrow_hashref())
						{
							my $name=$dbrow->{'Name'};
							print "<option value=\"$name\"";
							print " selected" if ($name eq $bit);
							print ">$name\n";
						}
						print "</select>\n";
						$dbcursor->finish();
					}
					if($i == 4)
					{
						print "<input type=text size=20 maxlength=40 name=\"preacher$numlines\" value=\"";
						print "$bit" if ($bit ne "Empty");
						print "\">\n"
					}
					if($i == 5)
					{
						print "<input type=text size=40 maxlength=255 name=\"notes$numlines\" value=\"";
						print "$bit" if ($bit ne "Empty");
						print "\">\n"
					}
				}
				else
				{
					print "$bit\n" if ($bit ne "Empty");
					print "&nbsp;\n" if ($bit eq "Empty");
				}
				print "</td>\n";
				$i++;
			}
			print "</tr>\n";
		}
		$numlines++;
	}
	print "</table>\n";
}

sub Printable
{
	$fromyear=$startbitz[0];
	$frommonth=$startbitz[1];
	$fromday=$startbitz[2];
	$toyear=$endbitz[0];
	$tomonth=$endbitz[1];
	$today=$endbitz[2];
	@chosenservs=split /;/, $services;
	CreateRotaLines();
	PopulateRotaLines();
	print "<CENTER>\n";
	print "<a href=\"rota.cgi?noframes\">\n" if ($noframes);
	print "<p>Worship Rota from $fromday/$frommonth/$fromyear to $today/$tomonth/$toyear for ";
	foreach $serv (@servs) { print "$serv "; }
	print "services.";
	print "</a>\n" if ($noframes);
	GenerateTable("ro");
	print "</CENTER>\n";
	print "</body>\n";
}

1;
