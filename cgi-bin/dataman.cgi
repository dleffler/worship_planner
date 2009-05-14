#!/usr/bin/perl

use config;
use CGI header;
use common;

my $priv=GetPriv();

print header();
print "<html>\n";
print $myheader;
print "<head><title>Song Manager</title></head>\n";
print "<body>\n";
if ($noframes) { TopTable("dataman"); }
print "<h1>Song Manager</h1>\n";
print "<p>Current features of the data manager are:<br>\n";
print "<table cellspacing=10 border=\"0\">\n";
print "<tr>\n";
print "<td align=\"left\" valign=\"top\">\n";
if ($priv > 0)
{
	print "<a href=\"bookman.cgi?noframes\">" if ($noframes);
	print "<a href=\"bookman.cgi\" target=\"Work\">" if (!$noframes);
	print "Add a New Book</a><br>\n";
	print "<a href=\"songman.cgi?noframes\">" if ($noframes);
	print "<a href=\"songman.cgi\" target=\"Work\">" if (!$noframes);
	print "Add a New Song</a><br>\n";
}
print "<a href=\"songpick.cgi?noframes\">" if ($noframes);
print "<a href=\"songpick.cgi\" target=\"Work\">" if (!$noframes);
print "Song Picker</a><br>\n";
if ($priv > 0)
{
	print "</td>\n";
	print "<td align=\"left\" valign=\"top\">\n";
	print "<a href=\"booked.cgi?noframes\">" if ($noframes);
	print "<a href=\"booked.cgi\" target=\"Work\">" if (!$noframes);
	print "Edit a Book</a><br>\n";
	print "<a href=\"songed.cgi?noframes\">" if ($noframes);
	print "<a href=\"songed.cgi\" target=\"Work\">" if (!$noframes);
	print "Edit a Song</a><br>\n";
	print "<a href=\"songmerge.cgi?noframes\">" if ($noframes);
	print "<a href=\"songmerge.cgi\" target=\"Work\">" if (!$noframes);
	print "Merge Songs </a><br>\n";

	print "</td>\n";
	print "<td valign=top>\n";
	print "<a href=\"bookdel.cgi?noframes\">" if ($noframes);
	print "<a href=\"bookdel.cgi\" target=\"Work\">" if (!$noframes);
	print "Delete a Book</a><br>\n";
	print "<a href=\"songdel.cgi?noframes\">" if ($noframes);
	print "<a href=\"songdel.cgi\" target=\"Work\">" if (!$noframes);
	print "Delete a Song</a><br>\n";
}
print "</td>\n";
print "</tr>\n";
print "</table>\n";
print "</body></html>\n";
