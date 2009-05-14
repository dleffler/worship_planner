#!/usr/bin/perl
# Worship Service Planning and Archiving System installer.

print "Welcome to the Worship Service Planning and Archiving System Install program.\n";
print "You should be logged in as root, or at least have write access to your Apache\n";
print "configuration files and document root.\n";
print "Before going any further you should ensure that you have a working web server\n";
print "(only Apache is supported by this installation program) and MySQL database.\n";
print "You should also have created a database user that this system will connect as.\n";
print "This user should have the right to create databases, select, delete and insert.\n";
print "First some questions regarding the database:\n";
my $dbHost = getinput("Enter the hostname of the database server","localhost");
my $database = getinput ("Enter the name of the database","Services");
my $dbUser = getinput ("Enter the Database user","");
my $dbPasswd = getinput ("Enter the Database user's password","");
print "Next some details about you as the first user and administrator of the system.\n";
my $fullname = getinput ("Enter your full name","");
my $username = getinput ("Enter your prefered username","");
my $password = getinput ("Enter your prefered password","");
print "Next a couple of questions regarding emails:\n";
my $mailserver = getinput("Enter the hostname of your mailserver","localhost");
my $tempdir = getinput("Enter the location of your temporary directory","/tmp");
print "Next some webserver information:\n";
my $docroot = getinput("Enter the full path to the directory that is the top of your website tree","/var/www/html");
my $htmldir = getinput("Enter the RELATIVE path to the directory where the html files will be stored. Leave this blank if your html files are to go at the top of your website tree.","");
my $cgiroot = getinput("Enter the full path to the directory where the cgi files will be stored","/var/www/cgi-bin");
my $imagedir = getinput("Enter the RELATIVE path from your website root to the directory where the graphics files will be stored","images");
my $url = getinput("Enter the BASE URL of this system (excluding path to html files)","http://foo.bar.com");
my $cgipath = getinput("Enter the RELATIVE path from the BASE url that browsers should use to access your cgi-directory","cgi-bin");
my $serverUser = getinput("Enter the username that Apache runs with","apache");
my $htpwfile = getinput("Enter the full pathname of your htpasswords file","");
print "Which services will this system be used to plan?\n";
print "Enter a list of service names, one after the other, hitting Enter after each.\n";
print "Names should either be the time that the service starts, or some other easy\n";
print "identifier. Please note that the order in which you enter them here is the\n";
print "order in which they will be listed on the system. Enter a blank value to finish.\n";
my @services = getlist("Enter Service Name","N");
print "For each service listed please list the days of the week on which they occur,\n";
print "one after another hitting Enter after each.\n";
print "Enter All if the service can occur on any day. Enter a blank value to finish.\n";
my %servicedays;
foreach $service (@services)
{
	my @daylist = getlist("Enter a day on which the $service service will occur","Y");
	$servicedays{$service} = join ',',@daylist;
}
my %basefeatures=(
	'Cong. Song', "Cong. Song",
	'Perf. Song', "Perf. Song",
	'Reading', "Reading",
	'Prayer', "Prayer",
	'Sermon', "Sermon",
	'Communion', "Communion",
	'Drama', "Drama",
	'Dance', "Dance",
	'Testimony', "Testimony",
	'Baptism', "Baptism",
	'Offering', "Offering",
	'Announcements', "Announcements",
	'Ministry', "Ministry");
print "What kind of activities occur during your services? Here's a suggested list.\n";
my $featurecount=0;
while (($key,$value) = each %basefeatures)
{
	if ($featurecount == 1) { print ", "; }
	$featurecount = 1;
	print "$key";
}
print "\nHit enter to accept this suggested list, or enter your own list, one after\nanother hitting Enter between entries with a blank line to finish.\n";
print "Enter an activity, or hit Enter to accept the suggested list: ";
my $input = <STDIN>;
chomp $input;
my @features;
if ($input ne "")
{
	%basefeatures=();
	@features = getlist("Enter an activity, or hit Enter to finish","N");
	unshift @features, $input;
}
foreach $feature (@features)
{
	$basefeatures{$feature} = $feature;
}

print "OK, that's all the questions over.\nHere's a quick recap before everything is installed.\n";
print "Regarding the database, on host $dbHost I'll create a $database database using\nusername $dbUser and password $dbPasswd to login to the database.\nI'll then install all the tables into this database.\n";
print "I'll create a new user for the system for $fullname with\nusername $username and password $password.\nThis user will have admin privileges and should be editted via the\n\"My Details\" section to add extra user detail.\n";
print "The system will be configured to use $mailserver as its mailserver\nand will use $tempdir to store temp files prior to emailing.\n";
print "Regarding your webserver, user passwords will be stored in $htpwfile,\n";
print "the html files will be installed in $docroot/$htmldir, images installed in\n";
print "$imagedir and cgi files in $cgiroot. and will be accessed via the\n";
print "internet on $url,\n and Apache runs with the username of $serverUser.\n";
print "You will have to manually make sure that your webserver is capable of running\ncgi programs from $cgiroot.\n";
print "These are the services you have entered and the days on which they occur:\n";
foreach $service (@services)
{
	print "$service: $servicedays{$service}\n";
}
print "Finally you have selected the following as your base list of activities. Remember that users can add to this list.\n";
$featurecount=0;
while (($key, $value) = each %basefeatures)
{
	if ($featurecount == 1) { print ", "; }
	$featurecount = 1;
	print "$key";
}
print "\n\nPlease hit Enter to install with these settings.\n";
my $input = <STDIN>;
Install();
WriteConfig();
BuildDB();

sub getinput
{
	my $message = shift;
	my $default = shift;
	print "$message [$default]: ";
	my $input = <STDIN>;
	chomp $input;
	if ($input eq "")
	{
		if ($default eq "")
		{
			print "There is no default value here. You must enter a value.\n";
			print "$message [$default]: ";
			my $input = <STDIN>;
			chomp $input;
		}
		else
		{
			$input = $default;
		}
	}
	return $input;
}

sub getlist
{
	my $message = shift;
	my $validate = shift;
	my @list;
	print "$message : ";
	my $input = <STDIN>;
	chomp $input;
	while ($input ne "")
	{
		if ($validate eq "Y") { $input = Validate($input); }
		if ($input ne "invalid") { push @list, $input; }
		print "$message : ";
		$input = <STDIN>;
		chomp $input;
	}
	return @list;
}

sub Validate
{
	my $input = shift;
	$input =~ s/[Ss][Uu][Nn][Dd][Aa][Yy]/Sunday/g ;
	$input =~ s/[Mm][Oo][Nn][Dd][Aa][Yy]/Monday/g ;
	$input =~ s/[Tt][Uu][Ee][Ss][Dd][Aa][Yy]/Tuesday/g ;
	$input =~ s/[Ww][Ee][Dd][Nn][Ee][Ss][Dd][Aa][Yy]/Wednesday/g ;
	$input =~ s/[Th][Hh][Uu][Rr][Ss][Dd][Aa][Yy]/Thursday/g ;
	$input =~ s/[Ff][Rr][Ii][Dd][Aa][Yy]/Friday/g ;
	$input =~ s/[Ss][Aa][Tt][Uu][Rr][Dd][Aa][Yy]/Saturday/g ;
	$input =~ s/[Aa][Ll][Ll]/All/g;

	if ( "Sunday,Monday,Tuesday,Wednesday,Thursday,Friday,Saturday,All" !~ /$input/)
	{
		print "$input is not a valid day of the week. Please enter another.\n";
		$input = "invalid";
	}
	return $input;
}

sub WriteConfig
{
	open CONFIG, ">$cgiroot/config.pm" or die "Could not create config file";
	select CONFIG;

	print "package config;\n";
	print "\n";
	print "use custom;\n";
	print "use base 'Exporter';\n";
	print "our \@EXPORT = qw(\$dbUser \$dbPasswd \$dbHost \$database \@services \%servicedays \$maxfeatures \%basefeatures \$htpwfile \$docroot \$cgidir \$htmldir \$imagedir \$url \$mailserver \$tempdir);\n";
	print "\n";
	print "our \$dbHost=\"$dbHost\";\n";
	print "our \$database=\"$database\";\n";
	print "our \$dbUser=\"$dbUser\";\n";
	print "our \$dbPasswd=\"$dbPasswd\";\n";
	print "our \$mailserver=\"$mailserver\";\n";
	print "our \$tempdir=\"$tempdir\";\n";
	print "\n";
	print "our \$htpwfile=\"$htpwfile\";\n";
	print "our \$docroot=\"$docroot\";\n";
	print "our \$htmldir=\"$htmldir\";\n";
	print "our \$cgidir=\"$cgipath\";\n";
	print "our \$imagedir=\"$imagedir\";\n";
	print "our \$url=\"$url\";\n";
	print "\n";
	print "our \@services=(";
	my $first=0;
	foreach $service (@services)
	{
		if ($first == 1) { print ", "; }
		print "\"$service\"";
		$first = 1;
	}
	print ");\n";
	print "\n";
	print "our \%servicedays=(\n";
	$first=0;
	while (($service, $days) = each %servicedays)
	{
		if ($first == 1) { print ",\n"; }
		print "	'$service', \"$days\"";
		$first = 1;
	}
	print ",\n	'Other', \"All\");\n";
	print "\n";
	print "our \%basefeatures=(\n";
	$first = 0;
	while (($feature, $featname) = each %basefeatures)
	{
		if ($first == 1) { print ",\n"; }
		print "	'$feature', \"$featname\"";
		$first = 1;
	}
	print ");\n";
	print "our \$maxfeatures=30;\n";
	print "\n";
	print "1;\n";
	select STDOUT;
	close CONFIG;
}

sub BuildDB
{
	my $addDB = `mysql --host=$dbHost --user=$dbUser --password=$dbPasswd mysql --exec=\"CREATE DATABASE $database\"`;
	my $addTables = `mysql --host=$dbHost --user=$dbUser --password=$dbPasswd $database < Services.sql`;
	my $addUser = `mysql --host=$dbHost --user=$dbUser --password=$dbPasswd $database --exec=\"INSERT INTO Team (Name,Username,Privilege) VALUES ('$fullname','$username',2);\"`;
}

sub Install
{
	my $makeDir = `mkdir $docroot`;
	my $makeCgiDir = `mkdir $cgiroot`;
	my $copy = `cp -R cgi-bin/* $cgiroot`;
	if ($htmldir ne "")
	{
		$makeDir = `mkdir $docroot/$htmldir`;
	}
	$copy = `cp -R html/* $docroot/$htmldir`;
	# if ($cgipath ne "cgi-bin")
	# {
		$url =~ s/\//\\\//g ;
		$cgipath =~ s/\//\\\//g ;
		my $htmlfix = "for file in $docroot/$htmldir/*.html ; do sed s/cgi-bin/\"$url\\\/$cgipath\"/g \$file > $docroot/$htmldir/tempout ; mv $docroot/$htmldir/tempout \$file ; done";
		print $htmlfix;
		my $doit = `$htmlfix`;
		# }
	if ($imagedir ne "")
	{
		$makeDir = `mkdir $docroot/$imagedir`;
	}
	$copy = `cp -R images/* $docroot/$imagedir`;
	open HTACCESS, ">$cgiroot/.htaccess" or die "Unable to create htaccess file";
	select HTACCESS;
	print "AuthType Basic\n";
	print "AuthName \"Worship Planner\"\n";
	print "AuthUserFile $htpwfile\n";
	print "Require user $username";
	select STDOUT;
	close HTACCESS;
	my $chown = `chown -R $serverUser.root $docroot/$htmldir/*`;
	my $chown = `chown -R $serverUser.root $docroot/$imagedir/*`;
	my $chown = `chown -R $serverUser.root $cgiroot/*`;
	my $chown = `chmod 755 $cgiroot/*.cgi`;
	my $psMake = `touch $htpwfile; /usr/sbin/htpasswd -b $htpwfile $username $password ; chown $serverUser.root $htpwfile`;
}
