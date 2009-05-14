#!/usr/bin/perl

use CGI::Carp qw(fatalsToBrowser);
use config;
use DBI;
use CGI param,header;
use common;
use Apache::Htpasswd;

CheckPriv("Delete Team Member","team",2);

my $name=param("name");
$name =~ s/</&lt;/g ;
$name =~ s/>/&gt;/g ;
my $username=param("username");
$username =~ s/</&lt;/g ;
$username =~ s/>/&gt;/g ;

my $dbname=$name;
$dbname =~ s/\'/\\\'/g ;

$dbh->do("DELETE FROM Team WHERE Name='$name'");
$pwfile = new Apache::Htpasswd($htpwfile);
if($username ne "") { my $result=$pwfile->htDelete($username); }
#if($username ne "") { my $result=`/usr/sbin/htpasswd -b $htpwfile $username notNom0re`; }

my $dbcursor=$dbh->prepare("SELECT * FROM TeamStruct WHERE Main='$dbname' OR Sub1='$dbname' OR Sub2='$dbname' OR Sub3='$dbname' OR Sub4='$dbname'");
$dbcursor->execute();
while (my $dbrow=$dbcursor->fetchrow_hashref())
{
	my $updatestring;
	if($dbrow->{'Main'} eq $name)
	{
		$updatestring="UPDATE TeamStruct SET Main='".$dbrow->{'Sub1'}."', Sub1='".$dbrow->{'Sub2'}."', Sub2='".$dbrow->{'Sub3'}."', Sub3='".$dbrow->{'Sub4'}."', Sub4='' WHERE Role='".$dbrow->{'Role'}."' AND Main='$name' AND Sub1='".$dbrow->{'Sub1'}."' AND Sub2='".$dbrow->{'Sub2'}."' AND Sub3='".$dbrow->{'Sub3'}."' AND Sub4='".$dbrow->{'Sub4'}."'";
		$dbh->do($updatestring);
	}
	if($dbrow->{'Sub1'} eq $name)
	{
		$updatestring="UPDATE TeamStruct SET Sub1='".$dbrow->{'Sub2'}."', Sub2='".$dbrow->{'Sub3'}."', Sub3='".$dbrow->{'Sub4'}."', Sub4='' WHERE Role='".$dbrow->{'Role'}."' AND Main='".$dbrow->{'Main'}."' AND Sub1='$name' AND Sub2='".$dbrow->{'Sub2'}."' AND Sub3='".$dbrow->{'Sub3'}."' AND Sub4='".$dbrow->{'Sub4'}."'";
		$dbh->do($updatestring);
	}
	if($dbrow->{'Sub2'} eq $name)
	{
		$updatestring="UPDATE TeamStruct SET Sub2='".$dbrow->{'Sub3'}."', Sub3='".$dbrow->{'Sub4'}."', Sub4='' WHERE Role='".$dbrow->{'Role'}."' AND Main='".$dbrow->{'Main'}."' AND Sub1='".$dbrow->{'Sub1'}."' AND Sub2='$name' AND Sub3='".$dbrow->{'Sub3'}."' AND Sub4='".$dbrow->{'Sub4'}."'";
		$dbh->do($updatestring);
	}
	if($dbrow->{'Sub3'} eq $name)
	{
		$updatestring="UPDATE TeamStruct SET Sub3='".$dbrow->{'Sub4'}."', Sub4='' WHERE Role='".$dbrow->{'Role'}."' AND Main='".$dbrow->{'Main'}."' AND Sub1='".$dbrow->{'Sub1'}."' AND Sub2='".$dbrow->{'Sub2'}."' AND Sub3='$name' AND Sub4='".$dbrow->{'Sub4'}."'";
		$dbh->do($updatestring);
	}
	if($dbrow->{'Sub4'} eq $name)
	{
		$updatestring="UPDATE TeamStruct SET Sub4='' WHERE Role='".$dbrow->{'Role'}."' AND Main='".$dbrow->{'Main'}."' AND Sub1='".$dbrow->{'Sub1'}."' AND Sub2='".$dbrow->{'Sub2'}."' AND Sub3='".$dbrow->{'Sub3'}."' AND Sub4='$name'";
		$dbh->do($updatestring);
	}
}
$dbcursor->finish();

my $user = $ENV{'REMOTE_USER'};
my $date=`date +\"%Y-%m-%d %H:%M:%S\"`;
$dbh->do("INSERT INTO Activity VALUES ('$date', '$user', 'Deleted Team Member; $dbname')");

print header();
print "<html>\n";
print $myheader;
print "<head><title>Team Manager</title></head>\n";
print "<body>\n";
if ($noframes) { TopTable("team"); }
print "<p><font size=\"+2\"$name has been deleted.</font>\n";
print "</body></html>\n";
