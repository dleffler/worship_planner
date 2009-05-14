#!/usr/bin/perl

use CGI::Carp qw(fatalsToBrowser);
use config;
use DBI;
use CGI param,header;
use common;
use Apache::Htpasswd;

CheckPriv("Add Team Member","team",1);

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

if(($memname eq "") || ($username eq "") || ($pass1 eq "") || ($pass2 eq ""))
{
	$error = "Name, username, and the password fields are mandatory. Please go back and fill them in.";
	ReportError($error,"team");
	exit;
}

if($pass1 ne $pass2)
{
	$error = "The two passwords did not match. Please go back and re-enter them both.\n";
	ReportError($error,"team");
	exit;
}

my $dbcursor=$dbh->prepare("SELECT Name, Username FROM Team WHERE Name='$dbmemname' OR Username='$dbusername'");
$dbcursor->execute();
my $dbrow=$dbcursor->fetchrow_hashref();
if ($dbrow != NULL)
{
	if($dbrow->{'Name'} eq $memname) { $error = "$dbmemname already exists in the database."; }
	if($dbrow->{'Username'} eq $username) { $error = "$dbusername already exists in the database."; }
	$dbcursor->finish();
	ReportError($error,"team");
	exit;
}
$dbcursor->finish();

$pwfile = new Apache::Htpasswd($htpwfile);
my $result = $pwfile->htpasswd($username,$pass1);
#my $result=`/usr/sbin/htpasswd -b $htpwfile $username $pass1`;
if($result != 1)
{
	$error = "Problem creating user password. Please try again later.";
	ReportError($error,"team");
	exit;
}
$result=`echo \"\nRequire user $username\" >> $docroot/.htaccess`;
if($result != 0)
{
	$error = "Problem creating user password. Please try again later.";
	ReportError($error,"team");
	exit;
}

$dbh->do("INSERT INTO Team VALUES ('$dbmemname', '$dbroles', '$dbtelnum', '$dbemail', '$dbusername', '$dbpriv')");
my $user = $ENV{'REMOTE_USER'};
my $date=`date +\"%Y-%m-%d %H:%M:%S\"`;
$dbh->do("INSERT INTO Activity VALUES ('$date', '$user', 'Added New Team Member; $dbmemname, $dbtelnum, $dbemail, $dbroles')");

print header();
print "<html>\n";
print $myheader;
print "<head><title>Team Manager</title></head>\n";
print "<body>\n";
if ($noframes) { TopTable("team"); }
print "<p>New Team Member Accepted.\n";
print "<p><a href=\"teamadd.cgi";
print "?noframes" if ($noframes);
print "\">Click here</a> to add another member.\n";
print "</body></html>\n";
