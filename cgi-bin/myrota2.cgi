#!/usr/bin/perl

use config;
use common;
use DBI;
use CGI header,param;

my $username=$ENV{'REMOTE_USER'};
my $dbuser=$username;
$dbuser =~ s/\'/\\\'/g ;

print header();
print "<HTML>\n";
print $myheader;
print "<HEAD><TITLE>Rota Changes</TITLE></HEAD>\n";
print "<BODY>\n";
if ($noframes) { TopTable("rota"); }
print "<p><font size=\"+2\">Rota Changes Accepted</font>\n";
print "<p>Your changes to the following services have been accepted<br><br>\n";

my $dbcursor=$dbh->prepare("SELECT Name, Email from Team WHERE Username='$dbuser'");
$dbcursor->execute();
my $dbrow=$dbcursor->fetchrow_hashref();
my $name=$dbrow->{'Name'};
my $email=$dbrow->{'Email'};
$dbcursor->finish();

my $linenum=1;
my $available = param("available$linenum");

while($available ne "")
{
	my $index=param("index$linenum");
	my $oldval=param("oldval$linenum");

	my ($servicedate, $service, $role, $main) = split /;/, $index;
	my ($thisyear, $thismonth, $thisday) = split /-/, $servicedate;
	
	$dbcursor=$dbh->prepare("SELECT Team FROM Rota WHERE ServiceDate='$servicedate' AND Service='$service'");
	$dbcursor->execute();
	$dbrow=$dbcursor->fetchrow_hashref();
	my $team=$dbrow->{'Team'};
	$dbcursor->finish();

	if ($available != $oldval)
	{
		print "<b>$service $thisday/$thismonth/$thisyear</b><br>\n";
		my $sub;
		if(($oldval == 1) && ($available == 0))
		{
			print "You have indicated that you will not be available for the role of $role at this service.<br>\n";
			
			#Member has indicated they will not be available. Update RotaSub, 
			#email the next substitute and let the team leaders know.
			my $subnum;
			if($main ne $name)
			{
				#Member is not the main team member and a substitution has already been made
				$dbcursor=$dbh->prepare("SELECT Sub FROM RotaSub WHERE ServiceDate='$servicedate' AND Service='$service' AND Role='$role' AND Main='$main'");
				$dbcursor->execute();
				$dbrow=$dbcursor->fetchrow_hashref();
				my $subpos=$dbrow->{'Sub'};
				$dbcursor->finish();
				$subnum = substr $subpos, 3;
				$subnum++;
				$dbcursor->do("UPDATE RotaSub SET Sub='Sub$subnum' WHERE ServiceDate='$servicedate' AND Service='$service' AND Role='$role' AND Main='$main'");
			}
			else
			{
				#Member is the main team member. A substitution has not yet been made so we make one here.
				
				#Create a record in RotaSub
				$subnum=1;
				$dbh->do("INSERT INTO RotaSub VALUES ('$servicedate', '$service', '$role', '$main', 'Sub1')");
			}
			#Get the name of the next sub.
			my $subpos="Sub$subnum";
			$dbcursor=$dbh->prepare("SELECT $subpos FROM TeamStruct WHERE Team='$team' AND Role='$role' AND Main='$main'");
			$dbcursor->execute();
			$dbrow=$dbcursor->fetchrow_hashref();
			$sub=$dbrow->{$subpos};
			$dbcursor->finish();
			my $nosub;
			if ($sub eq "")
			{
				# There is no sub, warn the team leaders
				$nosub=1;
			}
			else
			{
				$nosub=0;
			}
			my $message="$name will not be available for the role of $role at the $service service on $thisday/$thismonth/$thisyear.";
			if ($nosub)
			{
				$message=$message." Unfortunately there is no official substitute. Please make the necessary arrangements to fill this role if it is important.";
			}
			else
			{
				$message=$message." $sub is next in line to take on this role and will have been made aware of this change either by automatic email, or directly by $name getting in touch.";
			}
			$message=$message." To see whom you can expect at each service please see $url/team.cgi";

			EmailLeaders($message,$team,$role,$service,$thisday,$thismonth,$thisyear);
			#OK, we've emailed the leaders. Now to email the substitute.
			if ($nosub)
			{
				print "Unfortunately there is no-one else to take your place.<br>\n";
			}
			else
			{
				$dbcursor=$dbh->prepare("SELECT Telephone, Email FROM Team WHERE Name='$sub'");
				$dbcursor->execute();
				$dbrow=$dbcursor->fetchrow_hashref();
				my $submail=$dbrow->{'Email'};
				$dbcursor->finish();
				if ($submail eq "Unknown")
				{
					print "$sub is the next in line to take over from you, but is not currently contactable via email";
					if ($dbrow->{'Telephone'} eq "Unknown")
					{
						print " and this system does not have a record of a telephone number. Please get in touch with $sub regarding your unavailability and perhaps to give an encouragement to visit $url/mydet.cgi and provide email and telephone details.<br>\n";
					}
					else
					{
						print ". Please get in touch on ".$dbrow->{'Telephone'}." to advise of your unavailability.\n";
					}
				}
				else
				{
					print "$sub is the next in line to take over from you and will receive an email regarding your unavailability.<br>\n";
					$message="$name cannot fulfill the role of $role at the $service service on $thisday/$thismonth/$thisyear. As the next in line you are now responsible for this role. Please visit $url/mydet.cgi to view your responsibilities and indicate any that you are unable to fulfill.";
					#print "<! sending submail to $sub $submail >\n";
					my $subject="$role at $service service on $thisday/$thismonth/$thisyear";
					SendEmail($submail,$message,$subject);
				}
			}
		}
		elsif(($oldval == 0) && ($available == 1))
		{
			#Member has indicated they will now be available. Update or delete RotaSub, 
			#email the next substitute and let the team leader know.
			print "You have indicated that you are once again available for the role of $role at this service.<br>\n";
			# $subnum will contain the number of the current substitute. This is the person whom is no longer required.
			my $subnum=0;
			#Member is not the main team member and a substitution has already been made
			#Find out the substiute number
			$dbcursor=$dbh->prepare("SELECT Sub FROM RotaSub WHERE ServiceDate='$servicedate' AND Service='$service' AND Role='$role' AND Main='$main'");
			$dbcursor->execute();
			$dbrow=$dbcursor->fetchrow_hashref();
			my $subpos=$dbrow->{'Sub'};
			$dbcursor->finish();
			$subnum = substr $subpos, 3;
			#Use $subnum to get the name of the current sub
			$dbcursor=$dbh->prepare("SELECT $subpos FROM TeamStruct WHERE Team='$team' AND Role='$role' AND Main='$main'");
			$dbcursor->execute();
			$dbrow=$dbcursor->fetchrow_hashref();
			my $subname=$dbrow->{$subpos};
			$dbcursor->finish();
			#Use the name to get their email
			$dbcursor=$dbh->prepare("SELECT Telephone, Email FROM Team WHERE Name='$subname'");
			$dbcursor->execute();
			$dbrow=$dbcursor->fetchrow_hashref();
			my $email=$dbrow->{'Email'};
			my $telephone=$dbrow->{'Telephone'};
			$dbcursor->finish();
			#Do the emailing first before the database is updated
			#Email the sub.
			if($email !~ /Unknown/)
			{
				my $message="$name has indicated availability for the role of $role at the $service service on $thisday/$thismonth/$thisyear.\nThis means that you are no longer required to fill in.\nThanks for your willingness to be involved.\n";
				print "$subname will be emailed to advise of your availability.<br>\n";
				my $subject="$role at $service service on $thisday/$thismonth/$thisyear";
				SendEmail($email, $message,$subject);
			}
			else
			{
				if ($telephone =~ /Unknown/)
				{
					print "$subname\'s email address is not available to this system. Please telephone $telephone to advise regarding your availability change.<br>\n";
				}
				else
				{
					print "Nither $subname\'s email address nor telephon number are available to this system. Please get in touch to advise of your availability change and perhaps give an encouragement to visit $url/mydet.cgi to provide an email address and telephone number.<br>\n";
				}
			}
			#Email the leaders.
			$message="$name has indicated availability for the role of $role at the $service service on $thisday/$thismonth/$thisyear.\nTo see whom you can expect at each service please see $url/team.cgi\n";
			EmailLeaders($message,$team,$role,$service,$thisday,$thismonth,$thisyear);
			if($main ne $name)
			{
				#Find out what Sub I am and set Rotasub to my number
				$dbcursor=$dbh->prepare("SELECT Sub2, Sub3, Sub4 FROM TeamStruct WHERE Team='$team' AND Role='$role' AND Main='$main'");
				$dbcursor->execute();
				$dbrow=$dbcursor->fetchrow_hashref();
				my $newsub;
				if($dbrow->{'Sub2'} eq $name) { $newsub=2; }
				if($dbrow->{'Sub3'} eq $name) { $newsub=3; }
				if($dbrow->{'Sub4'} eq $name) { $newsub=4; }
				$dbcursor->finish();
				$dbcursor->do("UPDATE RotaSub SET Sub='Sub$newsub' WHERE ServiceDate='$servicedate' AND Service='$service' AND Role='$role' AND Main='$main'");
			}
			else
			{
				#Member is the main team member. So delete the appropriate 
				#record in rotasub.
				
				#Delete a record in RotaSub
				$dbh->do("DELETE FROM RotaSub WHERE ServiceDate='$servicedate' AND Service='$service' AND Role='$role' AND Main='$main'");
			}
		}
	}

	$linenum++;
	$available = param("available$linenum");
}

sub EmailLeaders
{
	my ($message,$team,$role,$service,$thisday,$thismonth,$thisyear)=@_;
	# We've updated the database, now to send the emails
	# First work out the team leaders and send an email to them
	my @leadernames;
	my $leaderlist="";
	my @leadermails;
	my @noleadermails;
	#print "<! Working with team - $team >\n";
	$dbcursor=$dbh->prepare("SELECT Main, Sub1, Sub2, Sub3, Sub4 FROM TeamStruct WHERE Team='$team' AND Role='Team Leader'");
	$dbcursor->execute();
	$dbrow=$dbcursor->fetchrow_hashref();
	if ($dbrow->{'Main'} ne "") { push @leadernames, $dbrow->{'Main'}; }
	if ($dbrow->{'Sub1'} ne "") { push @leadernames, $dbrow->{'Sub1'}; }
	if ($dbrow->{'Sub2'} ne "") { push @leadernames, $dbrow->{'Sub2'}; }
	if ($dbrow->{'Sub3'} ne "") { push @leadernames, $dbrow->{'Sub3'}; }
	if ($dbrow->{'Sub4'} ne "") { push @leadernames, $dbrow->{'Sub4'}; }
	$dbcursor->finish();
	my $first=0;
	foreach $leader ( @leadernames )
	{
		#print "<! Here's a leader - $leader >\n";
		$dbcursor=$dbh->prepare("SELECT Telephone, Email FROM Team WHERE Name='$leader'");
		$dbcursor->execute();
		$dbrow=$dbcursor->fetchrow_hashref();
		if ($dbrow->{'Email'} eq "Unknown")
		{
			push @noleadermails, "$leader Tel:".$dbrow->{'Telephone'}." Email:Unknown";
		}
		else
		{
			push @leadermails, $leader;
			if($first !=0) { $leaderlist=$leaderlist.","; }
			$first=1;
			$leaderlist=$leaderlist.$dbrow->{'Email'};
		}
	}
	#print "<! $leaderlist >\n";
	if ($leaderlist ne "")
	{
		my $subject="$role at $service service on $thisday/$thismonth/$thisyear";
		SendEmail($leaderlist, $message,$subject);
		print "The following team leaders will automatically receive an email from you to let them know. ";
		$first=0;
		foreach $leader (@leadermails)
		{
			if($first !=0) { print ", "; }
			$first=1;
			print "$leader";
		}
		print ".<br>\n";
	}
	if ($noleadermails[0] ne "")
	{
		print "The following team leaders are not contactable via email. Please get in touch directly to inform them of your availability changes.<br>\n";
		foreach $leader (@noleadermails)
		{
			print "$leader<br>\n";
		}
	}
}
