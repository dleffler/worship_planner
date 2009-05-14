package tscommon;

use config;
use common;
use CGI param,header;
use DBI;
use base 'Exporter';
@EXPORT = qw($dbh $team $dbteam ReadInputs SubmitTeam @roles @defaults @sub1s @sub2s @sub3s @sub4s @defaults CheckChanges);

$dbh = DBI->connect("DBI:mysql:database=$database;host=$dbHost",
                       $dbUser, $dbPasswd,
                      {'RaiseError' => 0});

sub ReadInputs
{
	my $i;
	for ($i=1;$i<=$maxfeatures;$i++)
	{
		my $rolepar="role".$i;
		my $defaultpar="default".$i;
		my $sub1par="sub1".$i;
		my $sub2par="sub2".$i;
		my $sub3par="sub3".$i;
		my $sub4par="sub4".$i;
		my $deletepar="delete".$i;

		$roles[$i]=param($rolepar);
		$oldroles[$i]=param("old$rolepar");
		$defaults[$i]=param($defaultpar);
		$olddefaults[$i]=param("old$defaultpar");
		$sub1s[$i]=param($sub1par);
		$oldsub1s[$i]=param("old$sub1par");
		$sub2s[$i]=param($sub2par);
		$oldsub2s[$i]=param("old$sub2par");
		$sub3s[$i]=param($sub3par);
		$oldsub3s[$i]=param("old$sub3par");
		$sub4s[$i]=param($sub4par);
		$oldsub4s[$i]=param("old$sub4par");
		$deletes[$i]=param($deletepar);
	}
}

sub SubmitTeam
{
	$dbh->do("DELETE FROM TeamStruct WHERE Team='$dbteam'");
	my $i;
	for($i=1;$i<(scalar @roles);$i++)
	{
		if(($deletes[$i] != 1) && ($roles[$i] ne ""))
		{
			my $dbrole=$roles[$i];
			$dbrole =~ s/\'/\\\'/g ;
			my $dbdefault=$defaults[$i];
			$dbdefault =~ s/\'/\\\'/g ;
			my $dbsub1=$sub1s[$i];
			$dbsub1 =~ s/\'/\\\'/g ;
			my $dbsub2=$sub2s[$i];
			$dbsub2 =~ s/\'/\\\'/g ;
			my $dbsub3=$sub3s[$i];
			$dbsub3 =~ s/\'/\\\'/g ;
			my $dbsub4=$sub4s[$i];
			$dbsub4 =~ s/\'/\\\'/g ;
			$dbh->do("INSERT INTO TeamStruct VALUES ('$dbteam', '$dbrole', '$dbdefault', '$dbsub1', '$dbsub2', '$dbsub3', '$dbsub4')");
		}
	}
	print "<font size=\"+2\">Team Structure Accepted. Thankyou!</font>\n";
	print "</body></html>\n";
}

sub CheckChanges
{
	my $date = `date +\"%Y-%m%d\"`;
	my $par;
	for ($par=1;$par<(scalar @roles);$par++)
	{
		if($deletes[$i] != 1)
		{
			#Check changes to see if they would mess anything up.
			# FIXME
			if((($roles[$par] ne $oldroles[$par]) && ($oldroles[$par] ne ""))
			|| (($defaults[$par] ne $olddefaults[$par]) && ($olddefaults[$par] ne ""))
			|| (($sub1s[$par] ne $oldsub1s[$par]) && ($oldsub1s[$par] ne ""))
			|| (($sub2s[$par] ne $oldsub2s[$par]) && ($oldsub2s[$par] ne ""))
			|| (($sub3s[$par] ne $oldsub3s[$par]) && ($oldsub3s[$par] ne ""))
			|| (($sub4s[$par] ne $oldsub4s[$par]) && ($oldsub4s[$par] ne "")))
			{
				#Get names and attempt the emailing.
				my %namelist;
				#Inserting the names into a hash removes duplicates
				for $name ($defaults[$par],$oldDefaults[$par],$sub1s[$par],$oldsub1s[$par],$sub2s[$par],$oldsub2s[$par],$sub3s[$par],$oldsub3s[$par],$sub4s[$par],$oldsub4s[$par])
				{
					$namelist{$name}=$name;
				}
				while (($name, $value) = each %namelist)
				{
					my $dbname=$name;
					$dbname =~ s/\'/\\\'/g ;
					my $dbcursor=$dbh->prepare("SELECT Email, Telephone FROM Team WHERE Name='$dbname'");
					$dbcursor->execute();
					my $dbrow=$dbcursor->fetchrow_hashref();
					my $email=$dbrow->{'Email'};
					my $telephone=$dbrow->{'Telephone'};
					$dbcursor->finish();
					if ($email ne "")
					{
						# Send them an email about it
						print "<BR>$name has been emailed regarding the change.\n";
						my $subject="Worship Team Structure Update";
						my $message="The structure of $dbteam has changed. The role where:\nRole = $oldroles[$par], Main Member = $olddefaults[$par], Sub1 = $oldsub1s[$par], Sub2 = $oldsub2s[$par], Sub3 = $oldsub3s[$par], Sub4 = $oldsub4s[$par]\nhas been changed to:\nRole = $roles[$par], Main Member = $defaults[$par], Sub1 = $sub1s[$par], Sub2 = $sub2s[$par], Sub3 = $sub3s[$par], Sub4 = $sub4s[$par].\nThis may mean that any indicated absences may have been deleted.\nPlease visit $url/mydet.cgi to check your updated responsibilities.\n";
						SendEmail($email,$message,$subject);
					}
					else
					{
						if($telephone ne "")
						{
							print "<BR>$name\'s email address is not on the system.";
							print "Please telephone $telephone to advise of this change.\n";
						}
						else
						{
							print "<BR>Neither $name\'s email address nor telephone number are stored on this system. Please get in touch to advise of this change and perhaps give an encouragement to visit $url/mydets.cgi and fill in the relevant details.\n";
						}
					}
				}
				if((($roles[$par] ne $oldroles[$par]) && ($oldroles[$par] ne ""))
				|| (($defaults[$par] ne $olddefaults[$par]) && ($olddefaults[$par] ne "")))
				{
					#You changed either the role or the main member.
					#Delete any RotaSubs and email all those affected.
					$dbh->do("DELETE FROM RotaSub WHERE Team='$dbteam' AND Role='$oldroles[$par]' AND Main='$olddefaults[$par]' AND ServiceDate>='$date'");
					print "<BR>You changed $roles[$par] in $dbteam from:<br>\n";
					print "Role - $oldroles[$par], Main Member - $olddefaults[$par], Sub1 - $oldsub1s[$par], Sub2 - $oldsub2s[$par], Sub3 - $oldsub3s[$par], Sub4 - $oldsub4s[$par]<br>To:<br>\n";
					print "Role - $roles[$par], Main Member - $defaults[$par], Sub1 - $sub1s[$par], Sub2 - $sub2s[$par], Sub3 - $sub3s[$par], Sub4 - $sub4s[$par]<br>\n";
					print "Since this can mess up the rota any affected substitutions that occur from today onwards have been deleted and the following team members should be made aware of this change.<br>\n";

				}
				else
				{
					#Check Rotasub. If the change only affects subs who have yet to be
					#made responsible for any services in this role then do nothing.
					#Otherwise delete the affected RotaSub lines and email the people.
					my $dbcursor=$dbh->prepare("SELECT * FROM RotaSub WHERE Team='$dbteam' AND Role='$oldroles[$par]' AND Main='$olddefaults[$par]' AND ServiceDate>='$date'");
					$dbcursor->execute();
					my @delLines;
					while (my $dbrow=$dbcursor->fetchrow_hashref())
					{
						my $delString="$oldroles[$par];$olddefaults[$par];".$dbrow->{'ServiceDate'}.";".$dbrow->{'Service'};
						my $sub=$dbrow->{'Sub'};
						if($sub eq "Sub5")
						{
							push @delLines, $delString;
						}
						elsif(($sub eq "Sub4") && 
							  (($sub4s[$par] ne $oldsub4s[$par]) ||
							   ($sub3s[$par] ne $oldsub3s[$par]) ||
							   ($sub2s[$par] ne $oldsub2s[$par]) ||
							   ($sub1s[$par] ne $oldsub1s[$par])
						      ))
						{
							push @delLines, $delString;
						}
						elsif(($sub eq "Sub3") && 
							  (($sub3s[$par] ne $oldsub3s[$par]) ||
							   ($sub2s[$par] ne $oldsub2s[$par]) ||
							   ($sub1s[$par] ne $oldsub1s[$par])
						      ))
						{
							push @delLines, $delString;
						}
						elsif(($sub eq "Sub2") && 
							  (($sub2s[$par] ne $oldsub2s[$par]) ||
							   ($sub1s[$par] ne $oldsub1s[$par])
						      ))
						{
							push @delLines, $delString;
						}
						elsif(($sub eq "Sub1") && 
							  ($sub1s[$par] ne $oldsub1s[$par]))
						{
							push @delLines, $delString;
						}
					}
					foreach $_ (@delLines)
					{
						#Delete the line.
						split /;/ ;
						$dbh->do("DELETE FROM RotaSub WHERE Role='$_[0]' AND Main='$_[1]' AND ServiceDate='$_[2]' AND Service='$_[3]'");
					}
				}
			}
		}
		else
		{
			#Delete any RotaSub lines and email those affected.
			print "<BR>You deleted $roles[$par] from $dbteam.\n";
			$dbh->do("DELETE FROM RotaSub WHERE Team='$dbteam' AND Role='$oldroles[$par]' AND Main='$olddefaults[$par]' AND ServiceDate>='$date'");
			foreach $name ($defaults[$par],$sub1s[$par],$sub2s[$par],$sub3s[$par],$sub4s[$par])
			{
				my $dbname=$name;
				$dbname =~ s/\'/\\\'/g ;
				my $dbcursor=$dbh->prepare("SELECT Email, Telephone FROM Team WHERE Name='$dbname'");
				$dbcursor->execute();
				my $dbrow=$dbcursor->fetchrow_hashref();
				my $email=$dbrow->{'Email'};
				my $telephone=$dbrow->{'Telephone'};
				$dbcursor->finish();
				if ($email ne "")
				{
					# Send them an email about it
					print "<BR>$name has been emailed regarding this deletion.\n";
					my $subject="Worship Team Structure Update";
					my $message="The role of $roles[$par] has been deleted from $dbteam. Please visit $url/mydet.cgi to check your updated responsibilities.\n";
					SendEmail($email,$message,$subject);
				}
				else
				{
					if($telephone ne "")
					{
						print "<BR>$name\'s email address is not on the system.";
						print "Please telephone $telephone to advise of this change.\n";
					}
					else
					{
						print "<BR>Neither $name\'s email address nor telephone number are stored on this system. Please get in touch to advise of this change and perhaps give an encouragement to visit $url/mydets.cgi and fill in the relevant details.\n";
					}
				}
			}
		}
	}
}

1;
