#!/usr/bin/perl

use config;
use common;
use CGI param,header;
use DBI;

my $priv=GetPriv();
my $date=param("date");
my $olddate=param("old_date");
my $service=param("service");
my $defservice=param("defservice");
my $readonly=param("readonly");
my $mychoice=param("R1");

if ($mychoice == '3')
{
  $date="0000-00-00";
  $service=$defservice;
}
if ($mychoice == '2')
{
  split /\./, $olddate;
  $service=$_[1];
  $date=$_[0];
}
split /-/, $date;
my $year=$_[0];
my $month=$_[1];
my $day=$_[2];
#my $daysuffix = (((substr $day, -1) == 1) && ($day != 11)) ? "st" : (((substr $day, -1) == 2) ? "nd" : "th") ;
#my $servstring="$day$daysuffix $months[$month-1] $year $service";
$day=DaySuffix($day);
my $servstring="$day $months[$month-1] $year $service";
if ($mychoice == '3')
{
  $servstring="$service DEFAULT";
}
my @songs;
my $songNo;

if (($readonly == 1) || ($priv < 1))
{
	GetApprovedSongs();
	ShowReadOnly();
}
else
{
	# Generate Feature List Hash
	my $dbcursor=$dbh->prepare("SELECT DISTINCT FType from ServiceLines");
	$dbcursor->execute();
	while (my $dbrow=$dbcursor->fetchrow_hashref())
	{
		if ($basefeatures{$dbrow->{'FType'}} eq "")
		{
			$basefeatures{$dbrow->{'FType'}} = $dbrow->{'FType'};
		}
	}
	$dbcursor->finish();

	# Generate songs array
	my $dbcursor=$dbh->prepare("SELECT SongName FROM Songs ORDER BY SongName;");
	$dbcursor->execute();
	while (my $dbrow=$dbcursor->fetchrow_hashref())
	{
		$songs[$songNo]=$dbrow->{'SongName'};
		$songNo++;
	}
	$dbcursor->finish();

	print header();
	print "<html>\n";
  print $myheader;
	print "<head><title>Planner</title></head>\n";
	print "<body>\n";
	if ($noframes) { TopTable("service"); }
	print "<p align=center font=+2>$servstring Service</p>\n";
	print "</body>\n";
	print "</html>\n";
	print "<form action=\"preview.cgi";
	print "?noframes" if ($noframes);
	print "\" method=\"POST\">\n";
	print "<center>\n";
	print "<INPUT NAME=\"servstring\" TYPE=HIDDEN VALUE=\"$servstring\">\n";
	print "<INPUT NAME=\"date\" TYPE=HIDDEN VALUE=\"$date\">\n";
	print "<INPUT NAME=\"service\" TYPE=HIDDEN VALUE=\"$service\">\n";
	print "<INPUT TYPE=SUBMIT VALUE=\"Preview Service\"><br>\n";
	print "<table border=\"1\" style=\"border-collapse: collapse\" width=\"100%\">";
	
  if ($mychoice == '3')
  {
	   print "<tr><th bgcolor=\"#FF0000\">Seq</th><th bgcolor=\"#FF0000\">Type</th><th bgcolor=\"#FF0000\">Song Name / Reading etc.</th></tr>\n";
  }
  else
  {
	    print "<tr><th>Seq</th><th>Type</th><th>Song Name / Reading etc.</th></tr>\n";
  }	

	$dbcursor=$dbh->prepare("SELECT * FROM ServiceLines WHERE ServiceDate='$date' AND Service='$service' ORDER BY Sequence");
	$dbcursor->execute();
	my $rowcount=0;
	while (my $dbrow=$dbcursor->fetchrow_hashref())
	{
		$rowcount++;
		print "<tr>\n";
		GenerateSeqList($rowcount,$rowcount);
		GenerateFeatureList($rowcount, $dbrow->{'FType'});
		GenerateSongList($rowcount, $dbrow->{'Feature'}, $dbrow->{'Notes'});
		print "</tr>\n";
	}

	# Get Default Service Order for type of service
  if ($rowcount == 0)
  {
  	$dbcursor=$dbh->prepare("SELECT * FROM ServiceLines WHERE ServiceDate='0000-00-00' AND Service='$service' ORDER BY Sequence");
  	$dbcursor->execute();
  	while (my $dbrow=$dbcursor->fetchrow_hashref())
  	{
  		$rowcount++;
  		print "<tr>\n";
  		GenerateSeqList($rowcount,$rowcount);
  		GenerateFeatureList($rowcount, $dbrow->{'FType'});
  		GenerateSongList($rowcount, $dbrow->{'Feature'}, $dbrow->{'Notes'});
  		print "</tr>\n";
  	}
  }

	$rowcount++;
	my $i;
	for ($i=$rowcount;$i<=$maxfeatures;$i++)
	{
		print "<tr>\n";
		GenerateSeqList($i,$i);
		GenerateFeatureList($i, "");
		GenerateSongList($i, "", "");
		print "</tr>\n";
	}
	print "</table>\n";
	print "<INPUT TYPE=SUBMIT VALUE=\"Preview Service\">\n";
	print "</CENTER>\n";
	print "</FORM>\n";
}

sub GenerateSeqList
{
	my $number=shift;
	my $default=shift;

	print "<td valign=\"top\">";
	print "<select name=\"seq$number\">\n";
	my $i;
	for ($i=0; $i<=$maxfeatures; $i++)
	{
		print "<option value=\"$i\"";
		print " selected" if ($i == $default);
		print ">$i\n";
	}
	print "</select><br>\n";
	print "<a href=\"$url/$htmldir/seqhelp.html\" target=\"_blank\">Help?</a>\n";
	print "</td>\n";
}

sub GenerateFeatureList
{
	my $number=shift;
	my $default=shift;
	print "<!number is $number, default is $default>\n";
	print "<td valign=\"top\">\n";
	print "Select: <select name=\"featuresel$number\">\n";
	print "<option value=\"nothing\">\n";
	while (($name, $value) = each %basefeatures)
	{
		$name  =~ s/<//g ;
		$name  =~ s/>//g ;
		$value =~ s/<//g ;
		$value =~ s/>//g ;
		if ($name ne "")
		{
			print "<option value=\"$name\"";
			print " selected" if ($name eq $default);
			print ">$value\n";
		}
	}
	print "</select>\n";
	print "<br> or Enter: <input name=\"featureinp$number\" type=text size=10 maxlength=20><br>\n";
	print "<a href=\"$url/$htmldir/fthelp.html\" target=\"_blank\">Help?</a>\n";
	print "</td>\n";
}

sub GenerateSongList
{
	my $number=shift;
	my $default=shift;
	my $notes=shift;
	my $defdone=0;
	
	print "<td valign=\"top\">\n";
	print "Select: <select name=\"songsel$number\">\n";
	print "<option value=\"nothing\">\n";
	my $i;
	for ($i=0; $i<(scalar @songs);$i++)
	{
		$songs[$i] =~ s/<//g ;
		$songs[$i] =~ s/>//g ;
		print "<option value=\"$songs[$i]\"";
		if ($songs[$i] eq $default)
		{
			print " selected";
			$defdone=1;
		}
		print ">$songs[$i]\n";
	}
	print "</select><a href=\"$url/$htmldir/featurehelp.html\" target=\"_blank\">Help?</a>\n";
	print "<br>or Enter:<input name=\"songinp$number\" type=text size=40 maxlength=80";
	print " value=\"$default\"" if ($defdone == 0);
	print ">\n";
	print "<br><textarea name=\"notes$number\" rows=\"2\" cols=\"60\">";
	print "Notes:-" if ($notes eq "");
	print "$notes" if ($notes ne "");
	print "</textarea>\n";
	print "</td>\n";
}

sub ShowReadOnly
{
	print header();
	print "<html>\n";
  print $myheader;
	print "<head><title>Preview</title></head>\n";
	print "<body>\n";
	print "<center>\n";
	print "<font size=\"+2\">Service $servstring</font>\n";
	print "<table border=\"1\" style=\"border-collapse: collapse\" width=\"100%\">\n";
	my $i;
	my $dbcursor=$dbh->prepare("SELECT * FROM ServiceLines WHERE ServiceDate='$date' AND Service='$service' ORDER BY Sequence");
	$dbcursor->execute();
	while (my $dbrow=$dbcursor->fetchrow_hashref())
	{
		my $ftype = $dbrow->{'FType'};
		$ftype =~ s/</&lt;/g ;
		$ftype =~ s/>/&gt;/g ;
		my $feature = $dbrow->{'Feature'};
		$feature =~ s/</&lt;/g ;
		$feature =~ s/>/&gt;/g ;
		my $notes = $dbrow->{'Notes'};
		$notes =~ s/</&lt;/g ;
		$notes =~ s/>/&gt;/g ;

		$approvedSongs{$feature} =~ s/</&lt;/g ;
		$approvedSongs{$feature} =~ s/>/&gt;/g ;

		print "<tr>\n";
		print "<td align=\"left\" valign=\"top\">$ftype&nbsp;</td>\n";
		print "<td align=\"left\" valign=\"top\">$feature&nbsp;";
		print "<br>$notes<br><br>";
		print "</td>\n";
		print "<td align=\"right\" valign=\"top\">";
		print "$approvedSongs{$feature}" if ($approvedSongs{$feature} !~ /Unknown/);
		print "&nbsp;</td>\n";
		print "</tr>\n";
	}
	print "</table>\n";
	print "</center>\n";
	print "</body>\n";
	print "</html>\n";
}
