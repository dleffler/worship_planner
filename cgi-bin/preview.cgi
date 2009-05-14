#!/usr/bin/perl

use CGI param,header;
use config;
use common;
use DBI;
use CGI::Carp qw(fatalsToBrowser);

CheckPriv("Edit Service Plan", "index",1);
print header();

my @seqs;
my @ftypes;
my @features;
my @notes;
my @songnums;
my %order;

my $servstring=param("servstring");
my $date=param("date");
my $service=param("service");
GetApprovedSongs();
ReadInputs();
GeneratePreview();
GenerateHiddenForm();

sub ReadInputs
{
	my $i;
	for ($i=1;$i<=$maxfeatures;$i++)
	{
		my $seqpar="seq".$i;
		my $ftselpar="featuresel".$i;
		my $ftinppar="featureinp".$i;
		my $songselpar="songsel".$i;
		my $songinppar="songinp".$i;
		my $notespar="notes".$i;

		my $seq=param($seqpar);
		my $ftsel=param($ftselpar);
		$ftsel =~ s/</&lt;/g ;
		$ftsel =~ s/>/&gt;/g ;
		my $ftinp=param($ftinppar);
		$ftinp =~ s/</&lt;/g ;
		$ftinp =~ s/>/&gt;/g ;
		my $songsel=param($songselpar);
		$songsel =~ s/</&lt;/g ;
		$songsel =~ s/>/&gt;/g ;
		my $songinp=param($songinppar);
		$songinp =~ s/</&lt;/g ;
		$songinp =~ s/>/&gt;/g ;
		my $notes=param($notespar);
		$notes =~ s/</&lt;/g ;
		$notes =~ s/>/&gt;/g ;
		print "<! $seq , $ftsel , $ftinp , $songsel , $songinp , $notes . >\n";

		if (($seq != 0) &&
			(($ftsel ne "nothing") || ($ftinp ne "") || ($songsel ne "nothing") || ($songinp ne "") ||
			 ( ($notes ne "") && ($notes ne "Notes:-") )))
	 	{
			# Deal with the line
			$seqs[$i]=$seq;
			$ftypes[$i] = ($ftsel ne "nothing") ? $ftsel : $ftinp ;
			$features[$i] = ($songsel ne "nothing") ? $songsel : $songinp ;
			$notes[$i] = ($notes ne "Notes:-") ? $notes : "";
			$songnums[$i] = $approvedSongs{$features[$i]};
			# Arrange the order hash
			if ($order{$seq} eq "")
			{
				$order{$seq} = $i;
			}
			else
			{
				#Shuffle everything above $seq up one
				my $highpos=$seq+1;
				while ($order{$highpos} ne "")
				{
					$highpos++;
				}
				my $movepos;
				for ($movepos=$highpos ; $movepos > $seq ; $movepos--)
				{
					$order{$movepos} = $order{$movepos-1};
				}
				$order{$seq+1}=$i;
			}
		}
	}
}

sub GeneratePreview
{
	my $warning = 0;
	print "<html>\n";
print $myheader;
	print "<head><title>Preview</title></head>\n";
	print "<body>\n";
	print "<center>\n";
	if ($noframes) { TopTable("index"); }
	print "<font size=\"+2\">$servstring Service</font>\n";
	print "<table border=\"1\" style=\"border-collapse: collapse\" width=\"100%\">\n";
	my $i;
	for ($i=1;$i<=$maxfeatures;$i++)
	{
		if ($order{$i} ne "")
		{
			$seq = $order{$i};
			print "<tr>\n";
			print "<td align=\"left\" valign=\"top\">$ftypes[$seq]&nbsp;</td>\n";
			print "<td align=\"left\" valign=\"top\"";
			if ((($ftypes[$seq] =~ /Song/) || ($ftypes[$seq] =~ /Hymn/)) && ($approvedSongs{$features[$seq]} eq ""))
			{
				print " bgcolor=\"red\"";
				$warning=1;
			}
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
	if ($warning == 1)
	{
		print "<p><b>WARNING</b> - You have entered a song that does not appear on our list. This will mess up our stats.\n";
		print "If the song is on our list under a slightly different name (you can check this using the Song Picker on the left) then hit the Back button on your browser and select the song using the drop-down box. If the song is not on our list then please add it using the song manager on the left, submit your service plan as-is (using the submit button below) then re-select your service using the Service Selector in the frame above. You should then find that your newly added song is on the list and can be chosen from the appropriate drop-down box.\n" if (!$noframes);
		print "The song may be on our list under a different name. Click the Back button on your browser to return to the service planner and see if it is on the list. If not, could you please add the song to our list using the Song Manager once you have submitted your service order.\n" if ($noframes);
	}
	print "<p>Click the \"Submit\" button below to commit this service order to the database, or click the back button on your browser to go back and amend it. You can come back at any time and amend the service order. Clicking \"Submit\" will also generate a printable version of the order.\n";
	if ($noframes)
	{
		print "<p><b>NOTE for \"No Frames\" Users - In order to keep your printable service order free of cruft but still giving you a link so you can move around this application the top line of the printable service order will be a link back to the main index.</b>\n";
	}
	else
	{
		print "Click inside the preview frame before printing and your browser should allow you to print only the current frame.\n";
	}
	print "</body>\n";
	print "</html>\n";
}

sub GenerateHiddenForm
{
	print "<form action=\"servsub.cgi";
	print "?noframes" if ($noframes);
	print "\" method=\"POST\">\n";
	my $i;
	my $numLines=0;
	for ($i=1; $i<=$maxfeatures; $i++)
	{
		if ($order{$i} ne "")
		{
			$numLines++;
			print "<INPUT NAME=\"seq$service$numLines\" TYPE=HIDDEN VALUE=\"$numLines\">\n";
			print "<INPUT NAME=\"ftype$service$numLines\" TYPE=HIDDEN VALUE=\"$ftypes[$order{$i}]\">\n";
			print "<INPUT NAME=\"feature$service$numLines\" TYPE=HIDDEN VALUE=\"$features[$order{$i}]\">\n";
			print "<INPUT NAME=\"notes$service$numLines\" TYPE=HIDDEN VALUE=\"$notes[$order{$i}]\">\n";
			print "<INPUT NAME=\"songnum$service$numLines\" TYPE=HIDDEN VALUE=\"";
			if ($songnums[$order{$i}] !~ /Unknown/) { print "$songnums[$order{$i}]"; }
			else { print "&nbsp;"; }
			print "\">\n";
		}
	}
	print "<INPUT NAME=\"servstring\" TYPE=HIDDEN VALUE=\"$servstring\">\n";
	print "<INPUT NAME=\"date\" TYPE=HIDDEN VALUE=\"$date\">\n";
	print "<INPUT NAME=\"service\" TYPE=HIDDEN VALUE=\"$service\">\n";
	print "<CENTER>\n";
	print "<input type=checkbox name=\"email\" value=\"1\">Send Service Order By Email&nbsp;&nbsp;&nbsp;\n";
	print "<INPUT TYPE=SUBMIT VALUE=\"Submit\">\n";
	print "</CENTER>\n";
	print "</FORM>\n";
}
