package servcommon;

use config;
use common;
use CGI param,header;
use DBI;
use Date::Pcalc qw(Date_to_Days Add_Delta_Days Day_of_Week);
use base 'Exporter';
use Socket;
use POSIX;

@EXPORT = qw($dbh Printable PrintTxt ShowHidden genMime SmtpSendMail $servstring $service $date);

$dbh = DBI->connect("DBI:mysql:database=$database;host=$dbHost",
                       $dbUser, $dbPasswd,
                      {'RaiseError' => 0});

$servstring="";
$date="";
$service="";

#==============================================================================
# These headers are for sending out email reminders or vcalendars 
%m = (
  'textheader' => qq{Content-Type: text/plain; charset=iso-8859-1\015\012Content-Transfer-Encoding: 8bit},
  'htmlheader' => qq{Content-Type: text/html; charset=iso-8859-1\015\012Content-Transfer-Encoding: 8bit},
	 );
				  
sub Printable
{
	my $i=1;
	my $message="";	
	my $seqpar="seq".$service.$i;
	my $seq=param($seqpar);
	if ($seq ne "") {
	  	$message .= "<center>\n";
	  	$message .= "<h3>";
	  	#$message .= "<a href=\"servicepick.cgi?+noframes\">" if ($noframes);
	  	$message .= "$servstring Service";
	  	#$message .= "</a>" if ($noframes);
	  	$message .= "</h3></center>\n";
	  	$message .= "<table border=\"1\" style=\"border-collapse: collapse\" width=\"100%\">\n";	
	}
	while ($seq ne "")
	{
		my $ftypepar="ftype".$service.$i;
		my $ftype=param($ftypepar);
		$ftype =~ s/</&lt;/g ;
		$ftype =~ s/>/&gt;/g ;
		my $featurepar="feature".$service.$i;
		my $feature=param($featurepar);
		$feature =~ s/</&lt;/g ;
		$feature =~ s/>/&gt;/g ;
		my $notespar="notes".$service.$i;
		my $notes=param($notespar);
		$notes =~ s/</&lt;/g ;
		$notes =~ s/>/&gt;/g ;
		my $songnumpar="songnum".$service.$i;
		my $songnum=param($songnumpar);
		$songnum =~ s/</&lt;/g ;
		$songnum =~ s/>/&gt;/g ;

		my $dbftype=$ftype;
		$dbftype =~ s/\'/\\\'/g ;
		my $dbfeature=$feature;
		$dbfeature =~ s/\'/\\\'/g ;
		my $dbnotes=$notes;
		$dbnotes =~ s/\'/\\\'/g ;

		$message .= "<tr>\n";
		$message .= "<td align=\"left\" valign=\"top\">$ftype&nbsp;<br></td>\n";
		$message .= "<td align=\"left\" valign=\"top\">$feature&nbsp;<br>$notes<br></td>\n";
		$message .= "<td align=\"right\" valign=\"top\">$songnum&nbsp;<br></td>\n";
		$message .= "</tr>\n";
		
		$i++;
		$seqpar="seq".$service.$i;
		$seq=param($seqpar);
	}
	if ($i ne 1) {
	  	$message .= "</table>\n";
	}
	return $message
}
				  
sub PrintTxt
{
	my $i=1; 
	my $message="";
	my $seqpar="seq".$service.$i;
	my $seq=param($seqpar);
	$message = "$servstring Service\n\n" if ($seq ne "");
	while ($seq ne "")
	{
		my $ftypepar="ftype".$service.$i;
		my $ftype=param($ftypepar);
		$ftype =~ s/</&lt;/g ;
		$ftype =~ s/>/&gt;/g ;
		my $featurepar="feature".$service.$i;
		my $feature=param($featurepar);
		$feature =~ s/</&lt;/g ;
		$feature =~ s/>/&gt;/g ;
		my $notespar="notes".$service.$i;
		my $notes=param($notespar);
		$notes =~ s/</&lt;/g ;
		$notes =~ s/>/&gt;/g ;
		my $songnumpar="songnum".$service.$i;
		my $songnum=param($songnumpar);
		$songnum =~ s/</&lt;/g ;
		$songnum =~ s/>/&gt;/g ;

		my $dbftype=$ftype;
		$dbftype =~ s/\'/\\\'/g ;
		my $dbfeature=$feature;
		$dbfeature =~ s/\'/\\\'/g ;
		my $dbnotes=$notes;
		$dbnotes =~ s/\'/\\\'/g ;

		$message .= "- $ftype\t$feature\t$songnum\n";
		
		$i++;
		$seqpar="seq".$service.$i;
		$seq=param($seqpar);
	}
  $message .= "\n";
  return $message;
}

sub ShowHidden
{
	my $i=1;
	my $seqpar="seq".$service.$i;
	my $seq=param($seqpar);
	while ($seq ne "")
	{
		my $ftypepar="ftype".$service.$i;
		my $ftype=param($ftypepar);
		$ftype =~ s/</&lt;/g ;
		$ftype =~ s/>/&gt;/g ;
		my $featurepar="feature".$service.$i;
		my $feature=param($featurepar);
		$feature =~ s/</&lt;/g ;
		$feature =~ s/>/&gt;/g ;
		my $notespar="notes".$service.$i;
		my $notes=param($notespar);
		$notes =~ s/</&lt;/g ;
		$notes =~ s/>/&gt;/g ;
		my $songnumpar="songnum".$service.$i;
		my $songnum=param($songnumpar);
		$songnum =~ s/</&lt;/g ;
		$songnum =~ s/>/&gt;/g ;

		my $dbftype=$ftype;
		$dbftype =~ s/\'/\\\'/g ;
		my $dbfeature=$feature;
		$dbfeature =~ s/\'/\\\'/g ;
		my $dbnotes=$notes;
		$dbnotes =~ s/\'/\\\'/g ;

		print "<input type=hidden name=\"seq$service$i\" value=\"$seq\">\n";
		print "<input type=hidden name=\"ftype$service$i\" value=\"$ftype\">\n";
		print "<input type=hidden name=\"feature$service$i\" value=\"$feature\">\n";
		print "<input type=hidden name=\"notes$service$i\" value=\"$notes\">\n";
		print "<input type=hidden name=\"songnum$service$i\" value=\"$songnum\">\n";
		
		$i++;
		$seqpar="seq".$service.$i;
		$seq=param($seqpar);
	}
}

#=====================================================================================================
sub genMime {  # generate an appropriate MIME message based on what's to be included in e-mail
    my($tmsg, $hmsg) = (@_);
	$tmsg =~ s/\r?\n/\015\012/g; $tmsg=&html_escape($tmsg, 0);
	$hmsg =~ s/\r?\n/\015\012/g; 
    my $theTime = &formatdatetime;
    my $mixbdy = "=-mix-wcal-AR479212096304";
    my $mixhdr = "Content-Type: multipart/mixed; boundary=\"$mixbdy\"";
    my $relbdy = "=-rel-wcal-AR479212096304";
    my $relhdr = "Content-Type: multipart/related; boundary=\"$relbdy\"";
    my $altbdy = "=-alt-wcal-AR479212096304";
    my $althdr = "Content-Type: multipart/alternative; boundary=\"$altbdy\"";

    if($tmsg) {
		$tmsg = "$m{'textheader'}\015\012\015\012$tmsg";
    }
    if($hmsg) {
		$hmsg="$m{'htmlheader'}\015\012\015\012$hmsg";
    }

    my $msg = "MIME-Version: 1.0\015\012Date: $theTime\015\012";
	$msg .= "$althdr\015\012";
	$msg .= "\015\012This is a multi-part message in MIME format.\015\012\015\012";	
	$msg .= "\015\012--$altbdy\015\012$tmsg\015\012\015\012--$altbdy\015\012$hmsg\015\012\015\012--$altbdy--\015\012";
	
	return $msg;
}
#--------------------------------------------------------------------------------
sub SmtpSendMail {
    my ($fromuser, $fromsmtp, $touser, $tosmtp, $subject, $messagebody) = (@_);
    my ($ipaddress, $fullipaddress, $packconnectip);
    my ($packthishostip);
    my ($AF_INET, $SOCK_STREAM);
    my ($PROTOCOL, $SMTP_PORT);
    my ($buf);

    my $datetime=&formatdatetime;
    my $message = "Subject: $subject\015\012";
	$message .= "To: $touser\015\012";
    $message .= "Date: $datetime\015\012";
	$message .= "X-Mailer: Worship Planner\015\012";
	$message .= $messagebody ;
    
    $AF_INET = AF_INET;
    $SOCK_STREAM = SOCK_STREAM;

    $PROTOCOL = (getprotobyname('tcp'))[2];
    $SMTP_PORT = (getservbyname('smtp','tcp'))[2];

    $SMTP_PORT = 25 unless ($SMTP_PORT =~ /^\d+$/);
    $PROTOCOL = 6 unless ($PROTOCOL =~ /^\d+$/);

    $fullipaddress = inet_aton($tosmtp);
    $packconnectip = sockaddr_in($SMTP_PORT, $fullipaddress);

    if(! socket (S, $AF_INET, $SOCK_STREAM, $PROTOCOL) ) { return (-1, "Can not make socket:$!\n");}
    if(! connect(S, $packconnectip)) {return (-3, "Can't connect socket:$!\n");}
    
    select(S);
    $| = 1;
    select (STDOUT);

    $buf = read_sock(S, 6);

    print S "HELO $fromsmtp\015\012";

    $buf = read_sock(S, 6);

    print S "MAIL From:<$fromuser>\015\012";
    $buf = read_sock(S, 6);

    my ($addr, @recipents);
    @recipents = split(/[, ]+/, $touser);
    for $addr (@recipents) { print S "RCPT To:<$addr>\015\012";  $buf = read_sock(S, 6); }

    print S "DATA\015\012";
    $buf = read_sock(S, 6);

    print S $message . "\015\012.\015\012";

    $buf = read_sock(S, 6);

    print S "QUIT\015\012";

    shutdown(S,2);

    return (0, "");
}
#--------------------------------------------------------------------------------

sub read_sock {
    #
    # $handle:  Handle to an allocated Socket
    # $endtime = amount of time read_sock is allowed to
    #                wait for input before timing out
    #                (measured in seconds)
    #
    #  return buffer containing what was read from the socket
    # 
    my ($handle, $endtime) = (@_);
    my ($localbuf,$buf);
    my ($rin,$rout,$nfound);

    $endtime += time;

    $buf = "";

    $rin = '';
    vec($rin, fileno($handle), 1) = 1;

    $nfound = 0;
#--------------------------------------------------------------------------------
  read_socket: 
    while (($endtime > time) && ($nfound <= 0)) {
	$length = 1024;
	$localbuf = " " x 1025;
	$nfound = 1;
        if( $ !~ m/MSWin|NT/i ) { # NT does not support select for polling to see if there are characters to be received.
	    $nfound = select($rout=$rin, undef, undef,.2);
	}
    }
    # If we found something in the read socket, we should
    # get it using sysread.
    if ($nfound > 0) {
	$length = sysread($handle, $localbuf, 1024);
	if ($length > 0) {
	    $buf .= $localbuf;
	}
    }
    return $buf;
}
#--------------------------------------------------------------------------------
sub formatdatetime {
    my $zone = strftime "%z", localtime;
    my ($sec, $min, $hour, $mday, $mon, $year, $wday, $yday, $isdst) = localtime(time);
    my @mons  = qw(Jan Feb Mar Apr May Jun Jul Aug Sep Oct Nov Dec);
    my @wdays = qw(Sun Mon Tue Wed Thu Fri Sat);
    $mon = $mons[$mon];
    
    #bug fix 2005/06/14 ul, wdays changed to wday	
    $wday = $wdays[$wday];
    $year +=  1900;
    $mday = sprintf("%02d", $mday);
    my $time = sprintf("%02d:%02d:%02d", $hour,$min,$sec);
    return "$wday, $mday $mon $year $time $zone";	
}

#--------------------------------------------------------------------------------
sub html_escape {
    my ($str, $encode) =(@_);
    if($encode){ $str =~ s/&/&amp;/g; $str =~ s/</&lt;/g; $str =~ s/>/&gt;/g; $str =~ s/\"/&quot;/g;}  # encode
    else { $str =~ s/&lt;/</g; $str =~ s/&gt;/>/g; $str =~ s/&quot;/\"/g; $str =~ s/&amp;/&/g;}        # decode
    return $str;
}
1;
