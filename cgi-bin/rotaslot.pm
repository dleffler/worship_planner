package rotaslot;

use strict;

sub new
{
	my $self = { 'servicedate' => "",
	             'service' => "",
				 'team' => "",
				 'role' => "",
	             'main' => "",
				 'substitute' => "",
				 };

	bless $self;
	return $self;
}

sub copy
{
	my ( $self ) = @_;
	my ( $new );

	%{ $new } = %{ $self };

	bless $new, 'rotaslot';
	return $new;
}

sub servicedate
{
	my $self = shift;
	$self->{'servicedate'} = shift;
	bless $self;
	return $self;
}

sub service
{
	my $self = shift;
	$self->{'service'} = shift;
	bless $self;
	return $self;
}

sub team
{
	my $self = shift;
	$self->{'team'} = shift;
	bless $self;
	return $self;
}

sub role
{
	my $self = shift;
	$self->{'role'} = shift;
	bless $self;
	return $self;
}

sub main
{
	my $self = shift;
	$self->{'main'} = shift;
	bless $self;
	return $self;
}

sub substitute
{
	my $self = shift;
	$self->{'substitute'} = shift;
	bless $self;
	return $self;
}

sub getservicedate
{
	my $self = shift;
	return $self->{'servicedate'};
}

sub getservice
{
	my $self = shift;
	return $self->{'service'};
}

sub getteam
{
	my $self = shift;
	return $self->{'team'};
}

sub getrole
{
	my $self = shift;
	return $self->{'role'};
}

sub getmain
{
	my $self = shift;
	return $self->{'main'};
}

sub getsubstitute
{
	my $self = shift;
	return $self->{'substitute'};
}

1;
