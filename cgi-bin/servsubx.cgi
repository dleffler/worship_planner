#!/usr/bin/perl

# prepare for mailing, get addressees

use CGI param,header;
use config;
use common;
use servcommon;
use DBI;

CheckPriv("E-Mail Service Plans", "index", 2);

$date=param("date");
split /-/, $date;
my $year=$_[0];
my $month=$_[1];
my $day=$_[2];
my $daysuffix = (((substr $day, -1) == 1) && ($day != 11)) ? "st" : (((substr $day, -1) == 2) ? "nd" : "th") ;

#my $now=`date +\"%Y-%m-%d %H:%M:%S\"`;
print header();
Email();
print "</body>\n</html>\n";

for ($k=0; $k<(scalar @services); $k++) # go thorough all service types for a given date
{
  $service=$services[$k];
  $servstring="$day$daysuffix $months[$month-1] $year $service";
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
  
  	$i++;
  	$seqpar="seq".$service.$i;
  	$seq=param($seqpar);
  }

  #Create hidden fields containing the service plan so that the data will perpetuate.
	ShowHidden();
}

sub Email
{
  $servstring="$day$daysuffix $months[$month-1] $year";
	print "<html>\n";
	print $myheader;
	print "<title>Order(s) for $servstring Service(s)</title></head>\n";
	print "<body>\n";
	if ($noframes) { TopTable("index"); }
	print "</body>\n";
	print "<form action=\"servmailx.cgi";
	print "?noframes" if ($noframes);
	print "\" method=\"POST\">\n";
	print "<b><p align=center>Order(s) for $servstring Service(s)</p></b>\n";
	print "<table border=\"0\" width=\"100%\">\n";
	print "<tr>\n";
	print "<td valign=top width=\"50%\">\n";

	print "<b>The E-Mail:</b><br>Subject: Service Order(s) for $servstring<br>\n";
	print "Enter your message below:\n";
	my $user = $ENV{'REMOTE_USER'};
	my $dbcursor=$dbh->prepare("SELECT Name, Username FROM Team WHERE Username='$user'");
	$dbcursor->execute();
	my $dbrow=$dbcursor->fetchrow_hashref();
	my $name=$dbrow->{'Name'};
	$dbcursor->finish();
	print "<br><textarea name=\"message\" rows=\"8\" cols=\"60\">";
	print "Dear Team,\n";
	print "Here is the planned service order(s) for $servstring.\n\n";
	print "$name";
	print "</textarea><br>Preview of attached order(s) is below:\n";
	print "<br><textarea name=\"message1\" rows=\"8\" cols=\"60\">";
	for ($k=0; $k<(scalar @services); $k++) # go thorough all service types for a given date
	{
		$service=$services[$k];
		$servstring="$day$daysuffix $months[$month-1] $year $service";
		print PrintTxt();
	}
	print "</textarea>\n";
	print "<input type=hidden name=\"date\" value=\"$date\">\n";
	print "<input type=SUBMIT value=\"Send Email\"><br><br><br>\n";
	print "</td>\n";
	print "<td valign=top>\n";
	print "Please select members to whom you wish to send this email.<br><br>\n";
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
}
