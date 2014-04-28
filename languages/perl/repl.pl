#!/usr/bin/env perl5.8
# Read–eval–print loop for Perl
# Can benefit being called with http://utopia.knoware.nl/~hlub/uck/rlwrap/
 
use Devel::REPL;
 
my $repl = Devel::REPL->new;
$repl->load_plugin($_) for qw(History);
$repl->run;
