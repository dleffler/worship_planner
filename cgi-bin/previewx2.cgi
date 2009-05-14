#!/usr/bin/perl

# Preview all service orders for a given date

use CGI param,header;
use config;
use common;
use DBI;
use CGI::Carp qw(fatalsToBrowser);

CheckPriv("Preview Service Orders", "index", 0);
print header();

#my $servstring=param("servstring");
my $date=param("view_date");
#my $service=param("service");
split /-/, $date;
my $year=$_[0];
my $month=$_[1];
my $day=$_[2];
#my $daysuffix = (((substr $day, -1) == 1) && ($day != 11)) ? "st" : (((substr $day, -1) == 2) ? "nd" : "th") ;
$day=DaySuffix($day);

GetApprovedSongs();
	print "<html>\n";
print $myheader;
	print "<head><title>Service Order Preview</title></head>\n";
	print "<body>\n";
	print "<form action=\"null.cgi";
	print "?noframes" if ($noframes);
	print "\" method=\"POST\">\n";
  my @seqs = ();
  my @ftypes = ();
  my @features = ();
  my @notes = ();
  my @songnums = ();
  my @order = ();
  my $myfeatures;  	
  for ($k=0; $k<(scalar @services); $k++) # go thorough all service types for a given date
  {
    $service=$services[$k];
    $servstring="$day $months[$month-1] $year $service";
    if (ReadInputs()) {
      GeneratePreview();
    }
    undef (@seqs);
    undef (@seqs);
    undef (@ftypes);
    undef (@features);
    undef (@notes);
    undef (@songnums);
    undef (@order);
  }

	print "</FORM>\n";
  print "</body>\n";
	print "</html>\n";

sub ReadInputs
{
	my $i;
	$dbcursor=$dbh->prepare("SELECT * FROM ServiceLines WHERE ServiceDate='$date' AND Service='$service' ORDER BY Sequence");
	$dbcursor->execute();
	my $i=0;
	while (my $dbrow=$dbcursor->fetchrow_hashref())
	{
		$i++;
		
		my $seq=$dbrow->{'Sequence'};
		my $ftsel=$dbrow->{'FType'};
		my $songsel=$dbrow->{'Feature'};
		my $notes=$dbrow->{'Notes'};
		print "<! $seq , $ftsel , $songsel , $notes . >\n";

		if (($seq != 0) &&
			(($ftsel ne "nothing") || ($songsel ne "nothing") ||
			 ( ($notes ne "") && ($notes ne "Notes:-") )))
	 	{
			# Deal with the line
			$seqs[$i]=$seq;
			$ftypes[$i] = $ftsel;
			$features[$i] = $songsel ;
			$notes[$i] = ($notes ne "Notes:-") ? $notes : "";
			$songnums[$i] = $approvedSongs{$features[$i]};
			if (($ftsel ne "") && ($seq ne "")) 
      {
        $order{$seq} = $i;
        if ($order{$i} ne "") {$myfeatures = $i}
      }
		}
	}
	return $i;
}

sub GeneratePreview
{
	print "<center>\n";
	if ($noframes) { TopTable("index"); }
	print "<font size=\"+2\">$servstring Service</font>\n";
	print "<table border=\"1\" style=\"border-collapse: collapse\" width=\"100%\">\n";
	my $i;
	for ($i=1;$i<=$myfeatures+1;$i++)
	{
		if ($order{$i} ne "")
		{
			$seq = $order{$i};
			print "<tr>\n";
			print "<td align=\"left\" valign=\"top\">$ftypes[$seq]&nbsp;</td>\n";
			print "<td align=\"left\" valign=\"top\"";
			print ">$features[$seq]&nbsp;";
			print "<br>$notes[$seq]<br>";
			print "</td>\n";
			print "<td align=\"right\" valign=\"top\">";
			print "$approvedSongs{$features[$seq]}" if ($approvedSongs{$features[$seq]} !~ /Unknown/);
			print "&nbsp;</td>\n";
			print "</tr>\n";
		}
	}
	print "</table>\n";
	print "</center>\n";
  print "<br>\n";
}
