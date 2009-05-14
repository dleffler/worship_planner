package config;

use custom;
use base 'Exporter';
our @EXPORT = qw($dbUser $dbPasswd $dbHost $database @services %servicedays $maxfeatures %basefeatures $htpwfile $docroot $cgidir $htmldir $imagedir $url $mailserver $tempdir $myheader $myfooter);

our $dbHost="harrisonhills.org";
our $database="harrisonhills_org";
our $dbUser="hhbc";
our $dbPasswd="38YFxv5u";
our $mailserver="mail.harrisonhills.org";
our $tempdir="/tmp";

our $htpwfile="/home/hhbc/stuff/.htpasswd";
our $docroot="/home/hhbc/www/worship";
our $htmldir="worship";
our $cgidir="cgi-bin\/worship";
our $imagedir="images";
our $url="http:\/\/www.harrisonhills.org";

our @services=("Morning", "Evening", "Students");

our %servicedays=(
	'Morning', "Sunday",
	'Evening', "Sunday",
	'Students', "Wednesday",
	'Other', "All");

our %basefeatures=(
	'Greeting', "Greeting",
	'Reading', "Reading",
	'Prayer', "Prayer",	
	'Welcome', "Welcome",
  'Announcements', "Announcements",		
  'Hymn', "Hymn",
	'Song', "Song",
	'Choir', "Choir",
	'Testimony', "Testimony",
	'Offering', "Offering",
	'Special Music', "Special Music",
  'Message', "Message",
  'Lords Supper', "Lords Supper",
  'Baptism', "Baptism",
  'Drama', "Drama");
our $maxfeatures=15;

1;
