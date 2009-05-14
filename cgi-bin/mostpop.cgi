#!/usr/bin/perl

use config;
use common;
use DBI;
use CGI header,param;

my $dbcursor=$dbh->prepare("SELECT MIN(ServiceDate) FROM ServiceLines WHERE ServiceDate != '0000-00-00'");
$dbcursor->execute;
my @dbrows=$dbcursor->fetchrow_array();
$_=$dbrows[0];
split /-/;
my $lowyear=$_[0];
my $lowmonth=$_[1];
my $lowday=$_[2];
$_=`date +\"%Y-%m-%d\"`;
split /-/;
my $thisyear=$_[0];
my $thismonth=$_[1];
my $thisday=$_[2];
my $fromdate=$lowday."/".$lowmonth."/".$lowyear;
my $todate=$thisday."/".$thismonth."/".$thisyear;
print header();
print "<html>\n";
print $myheader;
print "<head><title>Most Popular Songs</title></head>\n";
print "<body>\n";
if ($noframes) { TopTable("stats"); }
print "</body>\n";
print "<form action=\"mostpop1.cgi";
print "?noframes" if ($noframes);
print "\" method=\"POST\">\n";
print "<p>Most Popular Songs over a given Period.\n";
print "<p>Select the start of your date range (earliest date possible is $lowday/$lowmonth/$lowyear)<br>\n";

print "<select name=\"from_day\" onchange=\"if(self.gfPop)gfPop.updateHidden(this)\">\n";
my $i;
print "<option value=\"\"></option>\n"; 
for ($i=1;$i<=31;$i++)
{
	print "<option value=\"$i\"";
  print " selected" if ($i == $lowday);
	print ">$i</option>\n";
}
print "</select>\n";
print "<select name=\"from_month\" onchange=\"if(self.gfPop)gfPop.updateHidden(this)\">\n";
print "<option value=\"\"></option>\n"; 
for ($i=1;$i<=12;$i++)
{
	print "<option value=\"$i\"";
	print " selected" if ($i == $lowmonth);
	print ">$months[$i-1]</option>\n";
}
print "</select>\n";
print "<select name=\"from_year\" onchange=\"if(self.gfPop)gfPop.updateHidden(this)\">\n";
for ($i=$lowyear;$i<=($thisyear+1);$i++)
{
	print "<option value=\"$i\"";
	print " selected" if ($i == $lowyear);
	print ">$i</option>\n";
}
print "</select>\n";

print <<p1;
<INPUT name="popcal" onclick="var fm=this.form;if(self.gfPop)gfPop.fStartPop(fm.from,fm.to,this);" type="button" value="...">
<input name="from" type="hidden" value=$fromdate>
p1

print "<p>Select the end of your date range.<br>\n";
print "<select name=\"to_day\" onchange=\"if(self.gfPop)gfPop.updateHidden(this)\">\n";
print "<option value=\"\"></option>\n"; 
for ($i=1;$i<=31;$i++)
{
	print "<option value=\"$i\"";
	print " selected" if ($i == $thisday);
	print ">$i</option>\n";
}
print "</select>\n";
print "<select name=\"to_month\" onchange=\"if(self.gfPop)gfPop.updateHidden(this)\">\n";
print "<option value=\"\"></option>\n"; 
for ($i=1;$i<=12;$i++)
{
	print "<option value=\"$i\"";
	print " selected" if ($i == $thismonth);
	print ">$months[$i-1]</option>\n";
}
print "</select>\n";
print "<select name=\"to_year\" onchange=\"if(self.gfPop)gfPop.updateHidden(this)\">\n";
for ($i=$lowyear;$i<=($thisyear+1);$i++)
{
	print "<option value=\"$i\"";
	print " selected" if ($i == $thisyear);
	print ">$i</option>\n";
}
print "</select>\n";
print <<p1;
<INPUT name="popcal" onclick="var fm=this.form;if(self.gfPop)gfPop.fEndPop(fm.from,fm.to,this);" type="button" value="...">
<input name="to" type="hidden" value=$todate>
p1

print "<p>Which service are you interested in?<br>\n";
for($i=0;$i<(scalar @services);$i++)
{
	print "<input type=\"checkbox\" name=\"service\" value=\"$services[$i]\"";
	print " CHECKED" if ($services[$i] ne "Other");
	print ">$services[$i]<br>\n";
}
print "<p>How many songs do you want retrieved?<br>\n";
print "<input type=text name=\"numsongs\" size=5 maxlength=5 value=\"20\">\n";

print "<CENTER>\n";
print "<INPUT TYPE=SUBMIT VALUE=\"Get Stats\">\n";
print "</CENTER>\n";
print "</FORM>\n";
print $myfooter;
