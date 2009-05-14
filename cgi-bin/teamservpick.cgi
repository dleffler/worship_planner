#!/usr/bin/perl

use CGI::Carp qw(fatalsToBrowser);
use config;
use common;
use CGI header;
use servicepicker;

$_=$ENV{'QUERY_STRING'};

split /\+/;

my $date=$_[0];
my $mydate=`date +\"%Y-%m-%d\"`;
my $priv=GetPriv();

	print header();
	print "<html>\n";
  print $myheader;
	print "<head><title>Service Picker</title>";
  print "</head>\n";
	print "<body>\n";
	if ($noframes) { TopTable("service"); }
	print "<form action=\"teamserv.cgi\" method=\"POST\">\n" if (!$noframes);
	print "<form action=\"teamserv.cgi?noframes\" method=\"POST\">\n" if ($noframes);
  print "Services have been created for:\n";
  print "<select name=\"date\">\n";
  my $dbcursor=$dbh->prepare("SELECT DISTINCT ServiceDate, Service FROM ServiceLines WHERE ServiceDate != '0000-00-00' ORDER BY ServiceDate DESC");
  $dbcursor->execute();
  while (my $dbrow=$dbcursor->fetchrow_hashref)
  {
  	my $ServiceDate = $dbrow->{'ServiceDate'};
  	my $Service = $dbrow->{'Service'};
  	print "<option value=\"$ServiceDate.$Service\">$ServiceDate - $Service\n";
  }
  print "</select><br>\n";
 	print "<center>\n";
  print "<INPUT TYPE=SUBMIT VALUE=\"Show Team\">\n";
  print "</CENTER>\n";
  print "</FORM>\n";
