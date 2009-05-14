#!/usr/bin/perl

use CGI::Carp qw(fatalsToBrowser);
use config;
use DBI;
use CGI param,header;
use common;
use Apache::Htpasswd;

my $username = $ENV{'REMOTE_USER'};

my $memname=param("memname");
$memname =~ s/</&lt;/g ;
$memname =~ s/>/&gt;/g ;
my $telnum=param("telnum");
$telnum =~ s/</&lt;/g ;
$telnum =~ s/>/&gt;/g ;
my $email=param("email");
$email =~ s/</&lt;/g ;
$email =~ s/>/&gt;/g ;
my $roles=param("roles");
$roles =~ s/</&lt;/g ;
$roles =~ s/>/&gt;/g ;
my $oldname=param("oldname");
$oldname =~ s/</&lt;/g ;
$oldname =~ s/>/&gt;/g ;
my $pass1=param("pass1");
my $pass2=param("pass2");
my $error;

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

if($pass1 ne $pass2)
{
	$error = "The two passwords did not match. Please go back and re-enter them both.\n";
	ReportError($error,"team");
	exit;
}

if($pass1 ne "")
{
	$pwfile = new Apache::Htpasswd($htpwfile);
	my $result=$pwfile->htpasswd($username, $pass1, 1);
	#my $result=`/usr/sbin/htpasswd -b $htpwfile $username $pass1`;
	if($result != 1)
	{
		$error = "Problem updating user password. Please try again later.";
		ReportError($error,"team");
		exit;
	}
}

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
print "<p>Since you changed your password you will probably be asked to login again if you click any links. Simply enter your username and new password to continue.\n";
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
		print "<p>You are in $teamfound with the role of $rolefound. This role is no longer listed as one of your roles.\n";
	}
}
$dbcursor->finish();
if ($warned)
{
	my $priv = GetPriv();
	print "<p>Please either re-edit your details, or update the team structure to fix this.\n" if ($priv > 0);
	if ($priv == 0)
	{
		print "<p>Please either re-edit your details, or email one of the following leaders and ask them to amend the team structures.<br>\n";
		$dbcursor=$dbh>prepare("SELECT Name, Email FROM Team WHERE Privilege>0 AND Email<>''");
		$dbcursor->execute();
		while ($dbrow=$dbcursor->fetchrow_hashref())
		{
			print "<a href=\"mailto:".$dbrow->{'Email'}."\">".$dbrow->{'Name'}."</a> ";
		}
	}
}
if ($noframes) { print "<p><a href=\"mydet.cgi?noframes\">Click here</a> to return Your Details manager\n"; }
if (!$noframes) { print "<p><a href=\"mydet.cgi\" target=\"Manager\">Click here</a> to refresh your details above.\n"; }
print "</body></html>\n";
