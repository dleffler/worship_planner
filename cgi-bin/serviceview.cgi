#!/usr/bin/perl

use CGI::Carp qw(fatalsToBrowser);
use config;
use common;
use CGI header;
#use servicepicker;

$_=$ENV{'QUERY_STRING'};

split /\+/;

my $date=$_[0];
my $mydate=`date +\"%Y-%m-%d\"`;
my $priv=GetPriv();

	print header();
	print "<html>\n";
  print $myheader;
	print "<head><title>Service Order Preview</title>";
  print "</head>\n";
	print "<body>\n";
	if ($noframes) { TopTable("service"); }

# Preview exisiting services for a given day
	print "<form action=\"previewx2.cgi\" method=\"POST\">\n" if (!$noframes);
	print "<form action=\"previewx2.cgi?noframes\" method=\"POST\">\n" if ($noframes);
	print "<b>View Order for:</b> ";
  print "<select name=\"view_date\">\n";
  my $dbcursor=$dbh->prepare("SELECT DISTINCT ServiceDate FROM ServiceLines WHERE ServiceDate != '0000-00-00' ORDER BY ServiceDate DESC");
  $dbcursor->execute();
  while (my $dbrow=$dbcursor->fetchrow_hashref)
  {
  	my $ServiceDate = $dbrow->{'ServiceDate'};
  	print "<option value=\"$ServiceDate\">$ServiceDate\n";
  }
  print "</select> \n";
  print "<INPUT TYPE=SUBMIT VALUE=\"VIEW Service Orders\">\n";
  print "</FORM>\n";
    
	print "</body>\n";
