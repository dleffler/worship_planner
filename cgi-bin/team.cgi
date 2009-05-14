#!/usr/bin/perl

use CGI::Carp qw (fatalsToBrowser);
use config;
use CGI header;
use common;

my $priv = GetPriv();

print header();
print "<html>\n";
print $myheader;
print "<head><title>Team Manager</title></head>\n";
print "<body>\n";
if ($noframes) { TopTable("team"); }
print "<h1>Team Manager</h1>\n";
print "<p>Current features of the Team Manager are:<br>\n";
print "<table cellspacing=10 border=\"0\">\n";
print "<tr>\n";
print "<td align=\"left\" valign=\"top\">\n";
print "<a href=\"teamsum.cgi?noframes\">" if ($noframes);
print "<a href=\"teamsum.cgi\" target=\"Work\">" if (!$noframes);
print "Team Summary</a><br>\n";
if ($priv > 0)
{
	print "<a href=\"teamadd.cgi?noframes\">" if ($noframes);
	print "<a href=\"teamadd.cgi\" target=\"Work\">" if (!$noframes);
	print "Add a team member</a><br>\n";
}
if ($priv > 1)
{
	print "<a href=\"teamdel.cgi?noframes\">" if ($noframes);
	print "<a href=\"teamdel.cgi\" target=\"Work\">" if (!$noframes);
	print "Delete a team member</a><br>\n";
}
print "</td>\n";

print "<td align=\"left\" valign=\"top\">\n";
if ($priv > 0)
{
	print "<a href=\"teamed.cgi?noframes\">" if ($noframes);
	print "<a href=\"teamed.cgi\" target=\"Work\">" if (!$noframes);
	print "Edit a team member</a><br>\n";
	
print "<a href=\"teammail.cgi?noframes\">" if ($noframes);
print "<a href=\"teammail.cgi\" target=\"Work\">" if (!$noframes);
print "Email Team</a><br>\n";
}

if ($priv > 0)
{
	print "<a href=\"teamstruct.cgi?noframes\">" if ($noframes);
	print "<a href=\"teamstruct.cgi\" target=\"Work\">" if (!$noframes);
	print "Manage Team Structures</a><br>\n";
}
print "</td>\n";
print "<td>\n";
print "<a href=\"teamservpick.cgi?noframes\">" if ($noframes);
print "<a href=\"teamservpick.cgi\" target=\"Work\">" if (!$noframes);
print "View Team Expected at a Service</a><br>\n";
print "</td>\n";
print "</tr>\n";
print "</table>\n";
print "</body></html>\n";
