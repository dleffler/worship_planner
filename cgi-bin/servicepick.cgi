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
	print "<head><title>Service Picker</title>";
	print <<p1;
<link rel="stylesheet" type="text/css" media="all" href="/apps/jscalendar/calendar-system.css" title="Aqua" />
<script type="text/javascript" src="/apps/jscalendar/calendar.js"></script>
<script type="text/javascript" src="/apps/jscalendar/lang/calendar-en.js"></script>
<script type="text/javascript" src="/apps/jscalendar/calendar-setup.js"></script>
<script type="text/javascript"> 
function aSelect(radioType, mode) 
{ 
radioType[mode].checked=true; 
} 
</script> 
p1
  
  print "</head>\n";
	print "<body>\n";
	if ($noframes) { TopTable("service"); }
	print "<form name=\"myForm\" id=\"myForm\" action=\"planner.cgi\" method=\"POST\">\n" if (!$noframes);
	print "<form name=\"myForm\" id=\"myForm\" action=\"planner.cgi?noframes\" method=\"POST\">\n" if ($noframes);
	print "<input type=\"hidden\" name=\"date\" id=\"date\" value=\"$mydate\">";
  print "<b>Create or Edit a Service Plan:</b><br>";
	print <<p1;
<table border="0" style="border-collapse: collapse">
    <tr>
      <td valign="top" style="text-align: left"><input type="radio" checked name="R1" value="1">Create a Plan for a  
p1

	print "<select onclick=\"aSelect(document.myForm.R1,0)\" name=\"service\">\n";
	for ($i=0; $i<(scalar @services); $i++)
	{
		print "<option value=\"$services[$i]\">$services[$i]\n";
	}
	print "</select>\n";

	print <<p1;
 Service on:  	
<div onclick=\"aSelect(document.myForm.R1,0)\" style="background-color: #EFD6FE; width:100px; height:100px" id="calendar-container"></div><br>

<script type="text/javascript">
  function dateChanged(calendar) {
    // Beware that this function is called even if the end-user only
    // changed the month/year.  In order to determine if a date was
    // clicked you can use the dateClicked property of the calendar:
//    if (calendar.dateClicked) {
      var y = calendar.date.getFullYear();
      var m = calendar.date.getMonth()+1;     // integer, 0..11
      var d = calendar.date.getDate();      // integer, 1..31
      var input_field = document.getElementById("date");
      input_field.value = y + "-" + m + "-" + d;
//    }
  };

  Calendar.setup(
    {
      weekNumbers  : false,
      flatCallback : dateChanged,          // our callback function
      flat         : "calendar-container" // ID of the parent element
    }
  );
</script>
      </td>
      <td>&nbsp;</td>
      <td rowspan="3" style="text-align: right">
p1
  if ($priv > 0)
  {
  	print "<br>Preview Only? <INPUT TYPE=RADIO NAME=\"readonly\" VALUE=\"1\">Yes <INPUT TYPE=RADIO NAME=\"readonly\" VALUE=\"2\" CHECKED>No";
  }
  print "<p><INPUT TYPE=SUBMIT VALUE=\"EDIT Plan\"></td></tr>\n";  
  print "<tr><td><input type=\"radio\" name=\"R1\" value=\"2\">Edit the Existing Plan for ";
  print "<select onclick=\"aSelect(document.myForm.R1,1)\" name=\"old_date\">\n";
  my $dbcursor=$dbh->prepare("SELECT DISTINCT ServiceDate, Service FROM ServiceLines WHERE ServiceDate != '0000-00-00' ORDER BY ServiceDate DESC");
  $dbcursor->execute();
  while (my $dbrow=$dbcursor->fetchrow_hashref)
  {
  	my $ServiceDate = $dbrow->{'ServiceDate'};
  	my $Service = $dbrow->{'Service'};
  	print "<option value=\"$ServiceDate.$Service\">$ServiceDate - $Service\n";
  }
  print "</select><br>&nbsp;</td>\n";
  print "<td><p align=\"left\">&nbsp;</p></td></tr><tr><td>";
  
  print "<input type=\"radio\" name=\"R1\" value=\"3\">Edit the Default Plan for ";
	print "<select onclick=\"aSelect(document.myForm.R1,2)\" name=\"defservice\">\n";
	for ($i=0; $i<(scalar @services); $i++)
	{
		print "<option value=\"$services[$i]\">$services[$i]\n";
	}
	print "</select> Services</td><td>&nbsp;</td></tr></table>\n";
	
  print "</CENTER>\n";
  print "</FORM>\n";

# Preview exisiting services for a given day
  print "<hr>";
	print "<form action=\"previewx.cgi\" method=\"POST\">\n" if (!$noframes);
	print "<form action=\"previewx.cgi?noframes\" method=\"POST\">\n" if ($noframes);
	print "<b>View Plans for:</b> ";
  print "<select name=\"view_date\">\n";
  my $dbcursor=$dbh->prepare("SELECT DISTINCT ServiceDate FROM ServiceLines WHERE ServiceDate != '0000-00-00' ORDER BY ServiceDate DESC");
  $dbcursor->execute();
  while (my $dbrow=$dbcursor->fetchrow_hashref)
  {
  	my $ServiceDate = $dbrow->{'ServiceDate'};
  	print "<option value=\"$ServiceDate\">$ServiceDate\n";
  }
  print "</select> \n";
  print "<INPUT TYPE=SUBMIT VALUE=\"VIEW Existing Plans\">\n";
  print "</FORM>\n";
    
# Delete an old service
  print "<hr>";
	print "<form action=\"servdel.cgi\" method=\"POST\">\n" if (!$noframes);
	print "<form action=\"servdel.cgi?noframes\" method=\"POST\">\n" if ($noframes);
	print "<b>Delete the Plan for:</b> ";	
  print "<select name=\"del_date\">\n";
  my $dbcursor=$dbh->prepare("SELECT DISTINCT ServiceDate, Service FROM ServiceLines WHERE ServiceDate != '0000-00-00' ORDER BY ServiceDate DESC");
  $dbcursor->execute();
  while (my $dbrow=$dbcursor->fetchrow_hashref)
  {
  	my $ServiceDate = $dbrow->{'ServiceDate'};
  	my $Service = $dbrow->{'Service'};
  	print "<option value=\"$ServiceDate.$Service\">$ServiceDate - $Service\n";
  }
  print "</select> \n";
  print "<INPUT TYPE=SUBMIT VALUE=\"DELETE an Existing Plan\">\n";
  print "</FORM>\n";

	print "</body>\n";
