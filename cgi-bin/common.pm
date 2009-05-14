package common;

use lib qw(/home/hhbc/lib/site_perl);

use config;
use CGI header;
use DBI;
use Mail::Sender;
use base 'Exporter';
@EXPORT = qw(CheckPriv GetPriv GetStyles GetCategories GetRoles DaySuffix %styles %categories %roles %approvedSongs GetApprovedSongs $dbh TopTable @months @days ReportError $noframes @privlevels SendEmail);

@months=("January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December");
@days=("Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday");

$noframes= ( $ENV{'QUERY_STRING'} =~ /noframes/ ) ? 1 : 0;

$dbh = DBI->connect("DBI:mysql:database=$database;host=$dbHost",
                       $dbUser, $dbPasswd,
                      {'RaiseError' => 0});

%styles;
%categories;
%roles;
%approvedSongs;

@privlevels = ("member", "leader", "admin");

sub GetStyles
{
	my $dbcursor=$dbh->prepare("SELECT DISTINCT Style FROM Songs");
	$dbcursor->execute();
	while (my $dbrow=$dbcursor->fetchrow_hashref())
	{
		$_ = $dbrow->{'Style'};
		split /,/;
		my $i;
		for ($i=0; $i<(scalar @_); $i++)
		{
			while ((substr $_[$i],0,1) eq " ")
			{
				$_[$i] = (substr $_[$i],1);
			}
			while ((substr $_[$i],(length $_[$i])) eq " ")
			{
				$_[$i] = (substr $_[$i],0,(length $_[$i]));
			}
			$styles{$_[$i]}=$_[$i];
		}
	}
}

sub GetCategories
{
	my $dbcursor=$dbh->prepare("SELECT DISTINCT Categories FROM Songs");
	$dbcursor->execute();
	while (my $dbrow=$dbcursor->fetchrow_hashref())
	{
		$_ = $dbrow->{'Categories'};
		split /,/;
		my $i;
		for ($i=0; $i<(scalar @_); $i++)
		{
			while ((substr $_[$i],0,1) eq " ")
			{
				$_[$i] = (substr $_[$i],1);
			}
			while ((substr $_[$i],(length $_[$i])) eq " ")
			{
				$_[$i] = (substr $_[$i],0,(length $_[$i]));
			}
			$categories{$_[$i]}=$_[$i];
		}
	}
}

sub GetRoles
{
	my $dbcursor=$dbh->prepare("SELECT DISTINCT Roles FROM Team");
	$dbcursor->execute();
	while (my $dbrow=$dbcursor->fetchrow_hashref())
	{
		$_ = $dbrow->{'Roles'};
		split /,/;
		my $i;
		for ($i=0; $i<(scalar @_); $i++)
		{
			while ((substr $_[$i],0,1) eq " ")
			{
				$_[$i] = (substr $_[$i],1);
			}
			while ((substr $_[$i],(length $_[$i])) eq " ")
			{
				$_[$i] = (substr $_[$i],0,(length $_[$i]));
			}
			$roles{$_[$i]}=$_[$i];
		}
	}
}

sub TopTable
{
	my $caller=shift;
	print "<center>\n";
	print "<font size=\"+2\">Worship Service Planning and Archiving System - Version 0.5</font><br>\n";
#	print "Written By <a href=\"http://www.netouerkz.co.uk\">Netouerkz Computer Services</a>\n";
	print "<table border=\"0\" width=\"100\%\">\n";
	print "<tr>\n";
	print "<td align=\"center\" valign=\"top\"><a href=\"$url/$htmldir/$caller.html\">Frames Version</a></td>\n";
	print "<td align=\"center\" valign=\"top\"><a href=\"mydet.cgi?+noframes\">My Details</a></td>\n";
	print "<td align=\"center\" valign=\"top\"><a href=\"team.cgi?+noframes\">Team Manager</a></td>\n";
	print "<td align=\"center\" valign=\"top\"><a href=\"rota.cgi?+noframes\">Rota Manager</a></td>\n";
	print "<td align=\"center\" valign=\"top\"><a href=\"dataman.cgi?+noframes\">Song Manager</a></td>\n";
	print "<td align=\"center\" valign=\"top\"><a href=\"servicepick.cgi?+noframes\">Service Planner</a></td>\n";
	print "<td align=\"center\" valign=\"top\"><a href=\"stats.cgi?+noframes\">Statistics</a></td>\n";
	print "<td align=\"center\" valign=\"top\"><a href=\"$url/$htmldir/help.html\" target=\"_blank\">Documentation</a></td>\n";
	print "</tr>\n";
	print "</table>\n";
	print "</center>\n";
	print "<br><br>\n";
}

sub GetPriv
{
	my $user = $ENV{'REMOTE_USER'};
	$user =~ s/\'/\\\'/g ;
	my $dbcursor=$dbh->prepare("SELECT Privilege FROM Team WHERE Username='$user'");
	$dbcursor->execute();
	my $dbrow = $dbcursor->fetchrow_hashref();
	$dbcursor->finish();
	if ($dbrow == NULL) { return "member"; }
	my $privilege = $dbrow->{'Privilege'};
	return $privilege;
}

sub CheckPriv
{
	my $title=shift;
	my $manager=shift;
	my $authlevel=shift;
	my $priv = GetPriv();
	
	if($priv < $authlevel)
	{
		print header();
		print "<html>\n";
    print $myheader;
		print "<head><title>$title</title></head>\n";
		print "<body>\n";
		if ($noframes) { TopTable($manager); }
		print "<p>$title is not available since you only have $privlevels[$priv] privileges.\n";
		print "</body>\n";
		print "</html>\n";
		exit;
	}
}

sub GetApprovedSongs
{
	my $dbcursor=$dbh->prepare("SELECT SongName, Book, Number FROM Songs ORDER BY SongName;");
	$dbcursor->execute();
	while (my $dbrow=$dbcursor->fetchrow_hashref())
	{
		$approvedSongs{$dbrow->{'SongName'}}=$dbrow->{'Book'}." ".$dbrow->{'Number'};
		$songNo++;
	}
	$dbcursor->finish();
}

sub ReportError
{
	my $errmess = shift;
	my $manager = shift;
	
	print header();
    print $myheader;
	print "<html>\n";
	print "<head><title>Error</title></head>\n";
	print "<body>\n";
	if ($noframes) { TopTable($manager); }
	print "<p>Sorry, I am unable to take that entry. $errmess\n";
	print "</body></html>\n";
}

sub SendEmail
{
	my ($maillist, $mailtext, $subject)=@_;
	my $message=new Mail::Sender {smtp => $mailserver, from => $email};
	$message->Open({ to => $maillist, subject => $subject });
	$message->SendLineEnc("This is an automated message from the Worship Service Planning and Archiving system at $url.");
	$message->SendLineEnc($mailtext);
	$message->Close();
}

sub DaySuffix
{
	my $day=shift;
	$day =~ s/\s+$//;
     if (($day == 1) || ($day == 21) || ($day == 31)) { return $day . 'st'; }
        elsif (($day == 2) || ($day == 22))           { return $day . 'nd'; } 
        elsif (($day == 3) || ($day == 23))           { return $day . 'rd'; }
        else                                          { return $day . 'th'; }
}

1;
