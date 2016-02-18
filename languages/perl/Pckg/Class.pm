package Pckg::Class;

use strict;

use parent qw(Exporter); # Inheritance

#Symbol export (has been ?)
our @EXPORT = qw(&shared &hello);
our @EXPORT_OK = qw(&shared_on_demand &shared_by_tags);
our %EXPORT_TAGS = (TAG_A => [qw(&shared_by_tags)]);

our $shared = 'toto';
our $shared_on_demand = 'titi';
our $shared_by_tags = 'tata';

my $invisible = 'tutu'; # local to package

sub hello {
    my ($surname) = @_;
    print "Hello $surname\n";
}

sub new {
    my ($class,$param1,$param2) = @_; 
    $class = ref($class) || $class; # In case constructor is called on Object, not with Class->
    my $self = {};  # or $class->SUPER::new() if inheritance
    bless($self, $class); 
    $self->{PARAM1} = $param1;
    $self->{_PARAM2} = $param2; # UNDERSCORE => PRIVATE (convention)
    return $self; 
}

sub DESTROY {
  my ($self) = @_;
  # $this->SUPER::DESTROY(); if inheritance
  print "Destroying instance of Pckg::Class\n";
}

BEGIN {
  print "Loading package Pckg::Class\n";
}

END {
  print "End using package Pckg::Class\n";
}

1; # return value when loading package