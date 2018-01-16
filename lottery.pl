#!/usr/bin/perl -w

use DBI;
use Date::Parse;


$database="DBI:mysql:lottery:localhost";
$user="lottery";
$password="topsecretnottelling";

$filename=$ENV{"HOME"}."/.lottery";

$thisnum=0;
$lastnum=<NUMREAD> if open(NUMREAD,"<$filename");

@drawnums=();

open(LYNX,"lynx -nolist -dump 'http://lottery.merseyworld.com/cgi-bin/lottery?days=2&Machine=Z&Ballset=0&order=1&show=1&year=-1&display=NoTables'|");

while (<LYNX>)
{
	if (length($_)==81)
	{
		$thisnum=substr $_, 0, 4;
		$date=substr $_, 6, 15;
		push @drawnums, substr $_, 23, 2;
		push @drawnums, substr $_, 26, 2;
		push @drawnums, substr $_, 29, 2;
		push @drawnums, substr $_, 32, 2;
		push @drawnums, substr $_, 35, 2;
		push @drawnums, substr $_, 38, 2;
		$bonus=substr $_, 42, 2;

		last;
	}
}

#print "$lastnum, $thisnum '$date' - " . join(" ",@drawnums) . " ($bonus)\n";

if ($thisnum > $lastnum)
{
	#print "Processing new draw\n";

	print NUMWRITE "$thisnum\n" if open(NUMWRITE,">$filename");

	($sec,$min,$hour,$day,$month,$year)=strptime($date);
	$sec=$sec;
	$min=$min;
	$hour=$hour;

	$month+=1;
	$year+=1900;

	$insert="insert into draws values($thisnum,'$year-$month-$day',";
	foreach $drawnum (@drawnums)
	{
		$insert .= $drawnum.",";
	}

	$insert.="$bonus)";

	#print "$insert\n";

	#print "Bonus is $bonus\n";

	$dbh=DBI->connect($database,$user,$password);

	$stinsert=$dbh->prepare($insert);
	$stinsert->execute;

	$sth=$dbh->prepare("select * from tickets");
	$sth->execute;

	while (@row=$sth->fetchrow_array)
	{
		$email=$row[0];

		$matches=0;
		$gotbonus=0;

		@personnums=();

		for ($count=1;$count<=6;$count++)
		{
			push @personnums,$row[$count];
		}

		foreach $personnum (@personnums)
		{
			#print "Matching $personnum with $bonus\n";

			if ($personnum==$bonus)
			{
				#print "Bonus matches\n";
				$gotbonus=1;
			}

			foreach $drawnum (@drawnums)
			{
				#print "Matching $drawnum with $personnum\n";
				if ($drawnum==$personnum)
				{
					#print "Matches\n";
					$matches++;
				}
			}
		}

		$body = "The numbers for draw $thisnum ($date) are:\n\n";
		foreach $drawnum (@drawnums)
		{
			$body .= "$drawnum ";
		}

		$body .= "\nbonus $bonus\n\n";

		$body .= "You matched $matches ";
		if ($gotbonus)
		{
			$body .= " plus the bonus";
		}

		$body .= "\n\n";

		#print "$email matches $matches, bonus $gotbonus\n";

		$datestring=$day."/".$month."/".$year;

		$subject=$datestring.": ";

		foreach (@drawnums)
		{
			$subject.=$_." ";
		}

		$subject.="($bonus) - $matches";

		if ($gotbonus)
		{
			$subject.="+B";
		}

		#print "$email: $subject\n";
		#print "$body\n";

		system("echo \"$body\" | /usr/bin/Mail -s \"$subject\" $email");
	}

	$sth->finish;

	$dbh->disconnect;
}
