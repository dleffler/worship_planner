#!/usr/bin/perl

use CGI param,header;
use config;
use common;
use servcommon;
use DBI;

CheckPriv("Submit Service Order", "index",1);
$servstring=param("servstring");
$date=param("date");
$service=param("service");
my $mailflag=param("email");

#my $now="date +\"%Y-%m-%d %H:%M:%S\"";
my $now=`date +\"%Y-%m-%d %H:%M:%S\"`;

my $dbservice=$service;
$dbservice =~ s/\'/\\\'/g ;

$dbh->do("DELETE FROM ServiceLines WHERE ServiceDate='$date' AND Service='$dbservice'");
my $user = $ENV{'REMOTE_USER'};
$dbh->do("INSERT INTO Activity VALUES ('$now', '$user', 'Added or Updated $dbservice Service for $date')");

my $i=1;
my $seqpar="seq".$service.$i;
my $seq=param($seqpar);
while ($seq ne "")
{
	my $ftypepar="ftype".$service.$i;
	my $ftype=param($ftypepar);
	$ftype =~ s/</&lt;/g ;
	$ftype =~ s/>/&gt;/g ;
	my $featurepar="feature".$service.$i;
	my $feature=param($featurepar);
	$feature =~ s/</&lt;/g ;
	$feature =~ s/>/&gt;/g ;
	my $notespar="notes".$service.$i;
	my $notes=param($notespar);
	$notes =~ s/</&lt;/g ;
	$notes =~ s/>/&gt;/g ;
	my $songnumpar="songnum".$service.$i;
	my $songnum=param($songnumpar);
	$songnum =~ s/</&lt;/g ;
	$songnum =~ s/>/&gt;/g ;

	my $dbftype=$ftype;
	$dbftype =~ s/\'/\\\'/g ;
	my $dbfeature=$feature;
	$dbfeature =~ s/\'/\\\'/g ;
	my $dbnotes=$notes;
	$dbnotes =~ s/\'/\\\'/g ;

	my $dbftype=$ftype;
	$dbftype =~ s/\'/\\\'/g ;
	my $dbfeature=$feature;
	$dbfeature =~ s/\'/\\\'/g ;
	my $dbnotes=$notes;
	$dbnotes =~ s/\'/\\\'/g ;

	$dbh->do("INSERT INTO ServiceLines Values ('$date', '$dbservice', '$seq', '$dbftype', '$dbfeature', '$dbnotes')");

	$i++;
	$seqpar="seq".$service.$i;
	$seq=param($seqpar);
}
print header();

if($mailflag)
{
	Email();
}
else
{
  print "<html>\n";
  print $myheader;
  print "<head><title>Order(s) for $servstring Service</title></head>\n";
  print "<body>\n";
	print Printable();
}
print "</body>\n</html>\n";

sub Email
{
	print "<html>\n";
print $myheader;
	print "<title>$servstring Service</title></head>\n";
	print "<body>\n";
	if ($noframes) { TopTable("index"); }
	print "</body>\n";
	print "<form action=\"servmail.cgi";
	print "?noframes" if ($noframes);
	print "\" method=\"POST\">\n";
	print "<p align=center>Order for $servstring Service</p>\n";

	#Get Team from Rota
	my $dbcursor=$dbh->prepare("SELECT Team FROM Rota WHERE ServiceDate='$date' AND Service='$service'");
	$dbcursor->execute();
	my $dbrow=$dbcursor->fetchrow_hashref();
	my $team=$dbrow->{'Team'};
	$dbcursor->finish();

	# Get team structure and substitutes
	my @teamNames;
	$dbcursor=$dbh->prepare("SELECT * FROM TeamStruct WHERE Team='$team' ORDER BY Role");
	$dbcursor->execute();
	my $counter=0;
	while ($dbrow=$dbcursor->fetchrow_hashref())
	{
		print "<tr>\n";
		my $role=$dbrow->{'Role'};
		my $main=$dbrow->{'Main'};
		my $subcursor=$dbh->prepare("SELECT Sub FROM RotaSub WHERE ServiceDate='$date' AND Service='$service' AND Role='$role' AND Main='$main'");
		$subcursor->execute();
		my $subrow=$subcursor->fetchrow_hashref();
		if($subrow == NULL)
		{
			#No substitutions
			push @teamNames, $main;
		}
		else
		{
			#Show substitute
			print "<td align=\"left\" valign=\"top\">\n";
			my $sub=$subrow->{'Sub'};
			if($sub ne "Sub5")
			{
				push @teamNames, $dbrow->{$sub};
			}
			print "</td>\n";
		}
		$subcursor->finish();
		print "</tr>\n";
		$counter++;
	}
	$dbcursor->finish();
	print "<table border=\"0\" width=\"100%\">\n";
	print "<tr>\n";
	print "<td valign=top width=\"50%\">\n";
	my %involved;
	print "These team members are involved:<br>Check the box beside those you wish to email.<br>\n";
	my $counter=0;
	foreach $person (@teamNames)
	{
		if (($person ne "blank") && ($involved{$person} eq ""))
		{
			my $dbcursor=$dbh->prepare("SELECT Email, Telephone FROM Team WHERE Name='$person'");
			$dbcursor->execute();
			my $dbrow=$dbcursor->fetchrow_hashref();
			my $email=$dbrow->{'Email'};
			my $telephone=$dbrow->{'Telephone'};
			$involved{$person}=$email;
			if($email eq "Unknown")
			{
				print "$person - Tel:$telephone does not have a recorded email address.<br>\n";
			}
			else
			{
				print "<input type=checkbox name=\"$person\" value=1 checked>&nbsp;$person &lt;$email&gt;<br>\n";
			}
		}
		$counter++;
	}
	print "<b>- No one is scheduled!</b><br>" if !$counter;
	print "<hr><b>The E-Mail:</b><br>Subject: Order for $servstring Service<br>\n";
	print "Enter your message below:\n";
	my $user = $ENV{'REMOTE_USER'};
	my $dbcursor=$dbh->prepare("SELECT Name, Username FROM Team WHERE Username='$user'");
	$dbcursor->execute();
	my $dbrow=$dbcursor->fetchrow_hashref();
	my $name=$dbrow->{'Name'};
	$dbcursor->finish();
	print "<br><textarea name=\"message\" rows=\"8\" cols=\"60\">";
	print "Dear Team,\n\n";
	print "Here is the planned service order for the $servstring service.\n\n";
	print "$name";
	print "</textarea><br>Preview of attached order is below:\n";	
	print "<br><textarea name=\"message1\" rows=\"8\" cols=\"60\">";	
    print PrintTxt();
	print "</textarea>\n";		
	print "<input type=hidden name=\"servstring\" value=\"$servstring\">\n";
	print "<input type=hidden name=\"date\" value=\"$date\">\n";
	print "<input type=hidden name=\"service\" value=\"$service\">\n";
	print "<input type=SUBMIT value=\"Send Email\"><br><br><br>\n";
	print "</td>\n";
	print "<td valign=top>\n";
	print "Please select any other worship team members to whom you wish to send this email.<br><br>\n";
	$dbcursor=$dbh->prepare("SELECT Name, Email FROM Team WHERE Email<>'Unknown'");
	$dbcursor->execute();
	while($dbrow=$dbcursor->fetchrow_hashref())
	{
		my $name=$dbrow->{'Name'};
		my $email=$dbrow->{'Email'};
		if($involved{$name} eq "")
		{
			print "<input type=checkbox name=\"$name\" value=1>&nbsp;$name &lt;$email&gt;<br>\n";
		}
	}
	print "<br><b>Enter additional addresses below:</b><br>";
	print "<input type=TEXT name=email size=50 maxlength=255><br>\n";
	$dbcursor->finish();
	print "</td>\n";
	print "</tr>\n";
	print "</table>\n";
	
	#Create hidden fields containing the service plan so that the data will perpetuate.
	ShowHidden();
}
