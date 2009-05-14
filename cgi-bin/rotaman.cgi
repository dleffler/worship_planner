#!/usr/bin/perl

use config;
use common;
use DBI;
use CGI header,param;

CheckPriv("Rota Manager", "rota",2);

$_=`date +\"%Y-%m-%d\"`;
split /-/;
my $thisyear=$_[0];
my $thismonth=$_[1];
my $thisday=$_[2];

my $lastyear,$lastmonth,$lastday;
if ($thismonth == 1)
{
	$lastyear = $thisyear - 1;
	$lastmonth = 12;
}
else
{
	$lastyear = $thisyear;
	$lastmonth = $thismonth - 1;
}
$lastday = 1;
my $lastdate=$lastday."/".$lastmonth."/".$lastyear;

my $nextyear,$nextmonth,$nextday;
if ($thismonth == 12)
{
	$nextyear = $thisyear + 1;
	$nextmonth = 1;
}
else
{
	$nextyear = $thisyear;
	$nextmonth = $thismonth + 1;
}
$nextday = 31;
$nextday = ((($nextmonth == 4) || ($nextmonth == 6) 
             || ($nextmonth == 9) || ($nextmonth == 11))
             && ($nextday == 31)) ? 30 : $nextday ;

$nextday = (($nextmonth == 2) && ($nextday >= 29)) ? 
              ((($nextyear % 4) == 0) ? 29 : 28 )
              : $nextday ;
my $nextdate=$nextday."/".$nextmonth."/".$nextyear;
		 
print header();
print "<html>\n";
print $myheader;
print "<head><title>Rota Manager</title></head>\n";
print "<body>\n";
if ($noframes) { TopTable("rota"); }
print "</body>\n";
print "<form action=\"rotaman1.cgi";
print "?noframes" if ($noframes);
print "\" method=\"POST\">\n";
print "<table border=\"0\" cellpadding=\"10\">\n";
print "<tr>\n";
print "<td>\n";
print "<p>Select the start of your date range<br>\n";
print "<select name=\"from_day\" onchange=\"if(self.gfPop)gfPop.updateHidden(this)\">\n";
print "<option value=\"\"></option>";
my $i;
for ($i=1;$i<=31;$i++)
{
	print "<option value=\"$i\"";
	print " selected" if ($i == $lastday);
	print ">$i\n";
}
print "</select>\n";
print "<select name=\"from_month\" onchange=\"if(self.gfPop)gfPop.updateHidden(this)\">\n";
print "<option value=\"\"></option>";
for ($i=1;$i<=12;$i++)
{
	print "<option value=\"$i\"";
	print " selected" if ($i == $lastmonth);
	print ">$months[$i-1]\n";
}
print "</select>\n";
print "<select name=\"from_year\" onchange=\"if(self.gfPop)gfPop.updateHidden(this)\">\n";
for ($i=($lastyear-10);$i<=($thisyear+10);$i++)
{
	print "<option value=\"$i\"";
	print " selected" if ($i == $lastyear);
	print ">$i\n";
}
print "</select>\n";

print <<p1;
<INPUT name="popcal" onclick="var fm=this.form;if(self.gfPop)gfPop.fStartPop(fm.from,fm.to);" type="button" value="...">
<input name="from" type="hidden" value=$lastdate>
p1

print "<p>Select the end of your date range.<br>\n";
print "<select name=\"to_day\" onchange=\"if(self.gfPop)gfPop.updateHidden(this)\">\n";
print "<option value=\"\"></option>";
for ($i=1;$i<=31;$i++)
{
	print "<option value=\"$i\"";
	print " selected" if ($i == $nextday);
	print ">$i\n";
}
print "</select>\n";
print "<select name=\"to_month\" onchange=\"if(self.gfPop)gfPop.updateHidden(this)\">\n";
print "<option value=\"\"></option>";
for ($i=1;$i<=12;$i++)
{
	print "<option value=\"$i\"";
	print " selected" if ($i == $nextmonth);
	print ">$months[$i-1]\n";
}
print "</select>\n";
print "<select name=\"to_year\" onchange=\"if(self.gfPop)gfPop.updateHidden(this)\">\n";
for ($i=($lastyear-10);$i<=($nextyear+10);$i++)
{
	print "<option value=\"$i\"";
	print " selected" if ($i == $nextyear);
	print ">$i\n";
}
print "</select>\n";
print <<p1;
<INPUT name="popcal" onclick="var fm=this.form;if(self.gfPop)gfPop.fEndPop(fm.from,fm.to);" type="button" value="...">
<input name="to" type="hidden" value=$nextdate>
p1

print "</td><td>\n";
print "<p>Select which services you wish to manage?<br>\n";
for($i=0;$i<(scalar @services);$i++)
{
	print "<input type=\"checkbox\" name=\"service\" value=\"$services[$i]\"";
	print " CHECKED" if ($services[$i] ne "Other");
	print ">$services[$i]<br>\n";
}
print "</td></tr>\n";
print "</table>\n";
print "<CENTER>\n";
print "<INPUT TYPE=SUBMIT VALUE=\"Show Rota\">\n";
print "</CENTER>\n";
print "</FORM>\n";
print $myfooter;
