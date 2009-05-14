#!/usr/bin/perl

use CGI::Carp qw(fatalsToBrowser);
use config;
use DBI;
use CGI param,header;
use common;

CheckPriv("Edit Team Member","team",1);

my $memname=param("memname");
$memname =~ s/</&lt;/g ;
$memname =~ s/>/&gt;/g ;
my $telnum=param("telnum");
$telnum =~ s/</&lt;/g ;
$telnum =~ s/>/&gt;/g ;
my $email=param("email");
$email =~ s/</&lt;/g ;
$email =~ s/>/&gt;/g ;
my $username=param("username");
$username =~ s/</&lt;/g ;
$username =~ s/>/&gt;/g ;
my $pass1=param("pass1");
my $pass2=param("pass2");
my $priv=param("priv");
my $roles=param("roles");
$roles =~ s/</&lt;/g ;
$roles =~ s/>/&gt;/g ;
my $oldname=param("oldname");
$oldname =~ s/</&lt;/g ;
$oldname =~ s/>/&gt;/g ;
my $error;

my $mypriv = GetPriv();
if ($mypriv < $priv)
{
	$error = "Your privilege level of $privlevels[$mypriv] does not have authority to give other users $privlevels[$priv] privileges.";
	ReportError($error,"team");
	exit;
}

my $dbmemname=$memname;
$dbmemname =~ s/\'/\\\'/g ;
my $dboldname=$oldname;
$dboldname =~ s/\'/\\\'/g ;
my $dbtelnum=$telnum;
$dbtelnum =~ s/\'/\\\'/g ;
my $dbemail=$email;
$dbemail =~ s/\'/\\\'/g ;
my $dbusername=$username;
$dbusername =~ s/\'/\\\'/g ;
my $dbpriv=$priv;
$dbpriv =~ s/\'/\\\'/g ;
my $dbroles=$roles;
$dbroles =~ s/\'/\\\'/g ;

my $numBooks=0;

if($memname eq "")
{
	$error = "Name field is mandatory. Please go back and fill it in.";
	ReportError($error,"team");
	exit;
}

if($memname ne $oldname)
{
	my $dbcursor=$dbh->prepare("SELECT Name FROM Team WHERE Name='$dbmemname'");
	$dbcursor->execute();
	my $dbrow=$dbcursor->fetchrow_hashref();
	if ($dbrow != NULL)
	{
		if(($dbrow->{'Name'} eq $memname) && ($memname ne $oldname))
		{
			$error="$memname already exists in the database.";
			$dbcursor->finish();
			ReportError($error,"team");
			exit;
		}
	}
	$dbcursor->finish();
}

$dbh->do("UPDATE Team SET Name='$dbmemname', Roles='$dbroles', Telephone='$dbtelnum', Email='$dbemail' WHERE Name='$dboldname'");
$dbh->do("UPDATE Rota SET Leader='$dbmemname' WHERE Leader='$dboldname'");
if($memname ne $oldname)
{
	$dbh->do("UPDATE TeamStruct SET Main='$dbmemname' WHERE Main='$dboldname'");
	$dbh->do("UPDATE TeamStruct SET Sub1='$dbmemname' WHERE Sub1='$dboldname'");
	$dbh->do("UPDATE TeamStruct SET Sub2='$dbmemname' WHERE Sub2='$dboldname'");
	$dbh->do("UPDATE TeamStruct SET Sub3='$dbmemname' WHERE Sub3='$dboldname'");
	$dbh->do("UPDATE TeamStruct SET Sub4='$dbmemname' WHERE Sub4='$dboldname'");
}

my $user = $ENV{'REMOTE_USER'};
my $date=`date +\"%Y-%m-%d %H:%M:%S\"`;
$dbh->do("INSERT INTO Activity VALUES ('$date', '$user', 'Editted Team Member; $dboldname, $dbtelnum, $dbemail, $dbroles')");

print header();
print "<html>\n";
print $myheader;
print "<head><title>Team Manager</title></head>\n";
print "<body>\n";
if ($noframes) { TopTable("team"); }
print "<p>New Details Accepted.\n";
my $warned = 0;
$dbcursor=$dbh->prepare("SELECT Team, Role FROM TeamStruct WHERE Main='$dbmemname' OR Sub1='$dbmemname' OR Sub2='$dbmemname' OR Sub3='$dbmemname' OR Sub4='$dbmemname'");
$dbcursor->execute();
while ($dbrow=$dbcursor->fetchrow_hashref())
{
	my $rolefound=$dbrow->{'Role'};
	my $teamfound=$dbrow->{'Team'};
	if ($roles !~ /$rolefound/)
	{
		if ($warned == 0)
		{
			print "<p><b>Warning:</b> your changes have compromised data integrity.\n";
			$warned = 1;
		}
		print "<p>$memname is in $teamfound with the role of $rolefound. This role is no longer listed as one of $memname\'s roles.\n";
	}
}
$dbcursor->finish();
if ($warned) { print "<p>Please either re-edit this person's details, or update the team structure to fix this.\n"; }
print "<p><a href=\"teamed.cgi";
print "?noframes" if ($noframes);
print "\">Click here</a> to edit another member.\n";
print "</body></html>\n";
