#!/usr/bin/perl -w

# Install modules
cpan Modern::Perl

# http://lhullier.developpez.com/tutoriels/perl/intro/

$\="\n"; $,=" "; # User-friendly separators

my $this_file = ($0 =~ m~^.*[/\\](.*)$~)[0];
print $this_file;

##############################################
print "\n** Tests & tricks before 'strict' **";

$u = $u;
if (defined($u)) { exit 1 } # no need for ';' in block end : eeerck !
my $u = undef;
if (defined($u)) { exit 1 }
$u = 1;
my $u;
if (defined($u)) { exit 1 }
print '$x undefined';

$v = 42;
print "\$v = $v";
my $name_v = "v";
$$name_v++; # work only with globals
print "\$V = $v";

use strict;
#use diagnostics;
#use warnings;

##############################
print "\n** Expressions **";

my $x = "6" + 6 ** 2;
print "\$x = $x";
print($x = $x*3);
$x = "$x"x3;
print chop($x).$x; # respect call order
print reverse($x);
print index($x, 26, 2)."=".rindex($x, 26);
substr($x, 2, 1) = '#';
print $x;

##############################
print "\n** Tests logic **";

print "Multiple FALSE values" if (!undef  && !() && !$u && !0 && !"" && !"0");

# Loops advanced: block LABELs, continue, next, last, redo

########################
print "\n** Lists **";

my @l = ((1..10,"BOOM"),'a'..'z');

print "@l";

print $l[-1];

if (! exists( $l[42] ) ) { print "No element at index 42"; }

my ($x, $y) = @l;
print $x." ".$y;


my @t = @l;
print "\$l size : ".@t;
($x, @l, $y) = @t;
print "\$y emptied : $y";

my $concat = 0;
foreach my $v ( @l ) { $concat .= "$v"; }
print "\$concat=$concat";

# NOTE: 'foreach' is equivalent to 'for', with the lone exception to per default give local scope to loop variables declared without 'my'

print "shifting: ".shift(@l)."...@l";
unshift(@l,1,2);
push(@l,('A'..'Z'));
@t = reverse(@l);
print "@t";

@t = qw/ attention 'aux erreurs' betes /;
print "$t[1]";

@l = sort( {length($b) <=> length($a) or $a cmp $b} @l );
print "@l";

@t = (-5..5);
@t = grep { $_ > 0 } @t;
@t = map { -$_*2 } @t;
print "@t";

################################
print "\n** Functions **";

sub foo {
    my $p1 = shift;
    my ($p2, $p3) = @_;
    return ($p1, $p2, $p3);
}

@t = foo @l;
print "foo: @t";

################################
print "\n** Hash tables **";

my %h = ( "Bob" => 42.666, Sam => "23579");
$h{Tom} = "-<>/\\";
if( reverse($h{"Bob"}) eq "666.24" ) {
    print "test OK";
}

$\=""; $,=""; # Restauring default separators
foreach my $k (keys(%h)) {
  print " K=$k|V=$h{$k}";
}
print "\n";

$h{Sam} = undef; # ! not removed from %h !

foreach my $v (values(%h)) {
  print " V=$v";
}
print "\n";

delete($h{Sam});
%h = reverse(%h);

while( my ($k,$v) = each(%h) ) {
  print " K=$k|V=$v";
}
print "\n";
$\="\n"; $,=" "; # User-friendly separators

print "%h as scalar: ".scalar(%h); # equivalent to ~~
print "%h size: ".keys(%h);

print $ENV{HOME};

################################
print "\n** Slices & files **";

my ($mtime,$ctime) = ( stat($0) )[9,10];
print "file: $0, mtime: $mtime, ctime: $ctime, writable ? ".(-w $0).", size: ".(-s $0);

@t = qw(hello toto hello vous);
%h = ();
@h{@t} = ();
@t = keys %h;
print "Unique values: @t";

# Open perl test file directory
if ( $0 =~ m/^(.*)\\.*/ ) {
    chdir($1) or die("$!");
}

print for <*>, <.*>; # equivalent to glob('*')

my $timeout = 1; #seconds
eval {
    local $SIG{ALRM} = sub { die "ALRM: $!" };
    alarm $timeout;
    sleep 5; #seconds
    alarm 0;
};
if ($@) {
    if ( $@ =~ /^ALRM/ ) {
        print "Time out";
    } else {
        print "Unexpected error";
    }
} else {
    print "Normal behaviour";
}
# Various failure modes: die, carp, cluck, croak, confess - http://www.tutorialspoint.com/perl/perl_error_handeling.htm

my $fail_file = ".not_readable.txt";
eval {
    print "$fail_file is ".(-r $fail_file ? '' : 'un')."readable: ";
    # Better use 3-args 'open' form to avoid any strange filename impact
    # + use a reference counted filehandle
    open($fic,'<',$fail_file) or die("OPEN $!");
    print("OPEN OK");
    close($fic);
};
print "Died $@" if ($@ =~ /^OPEN/ );

open($fic,'<',"$this_file") or die("OPEN $!");
open($fic_pipe,'|-',"7z a -si $this_file.7z > /dev/null");
while( <$fic> ) {
  chomp $_;
  print "$. : $_" if ($. % 100 == 1);
  print $fic_pipe if m/^#.*/;
}
close($fic_pipe);
close($fic);

open($fic,'<',"ipconfig|");
while( <$fic> ) {
    print $1 if m/(\d\d\d\.\d\d\d\.\d\d\d\.\d)/;
}
close($fic);

############################
print "\n** DBM files **";

%h = ();
dbmopen(%h,"data",0644) or die($!);
$h{'prenom'} = 'Larry';
dbmclose(%h) or die($!);

%h = ();
dbmopen(%h,"data",0644) or die($!);
print "$h{'prenom'}";
dbmclose(%h) or die($!);

#########################################
print "\n** Expressions regulieres **";

my @adn = ("TATATATA" =~ m/(GC|TA)(GC|TA)(GC|TA){2}/);
print "@adn";

# Options:
# i - case insensitive
# g - multiple substitutions
# e - right member is considered perl expression
# o - opimization if often used regular expression

# Anchors:
# \G - indicates the position of the end of the previous match
# \b - indicates end or start of a word
#EXAMPLE: while(/\G(\b\w*\b)/g) { print "$1\n"; }


#+ non-greedy quantifiers

my $msg = 'aBcDe$^@[]()\/~';
$msg = quotemeta($msg);
print $msg;

($msg = "hello world !") =~ tr/a-z/za-y/;
print $msg;

#############################
print "\n** References **";

$x = 42;
my $refx = \$x;
print $refx;
print $$refx;
print ref($refx);

my $refN = \34; #Constant, cannot be modified
my $refS = \"er"; #Constant, cannot be modified
print "$$refN $$refS\n";

my $r;
$r = { a => \$r, b => { 0 => 'valid', 1 => 'invalid' }, c => [ 0..9 ]};
use Data::Dumper;
print Dumper($r);

open($fic,'<',"$this_file") or die("OPEN $!");
print \*$fic;
close($fic);

# With functions
print "\\&foo: ".\&foo;
print "ref(\\&foo): ".ref(\&foo);
sub foo { 42 }; # Redefinition + if no 'return' keyword : last expression evaluated returned
print foo;
print "\\&foo: ".\&foo; # Same address !

print foo + 1; # WARNING ! print 42
print foo() + 1;

# Anonymous functions
my $baz = sub { my $x = shift; $x * $x }; #squaring
print $baz->(-1);
print "\$baz: ".$baz;
print "ref(\$baz): ".ref($baz);
$baz = sub { my $sum = 0; $sum += $_ for @_; $sum }; #Redefinition, sum

# Currying
sub curry {
    my ($func, @args) = @_;
    return sub {
        &$func(@args, @_); 
    }
}
my $curried = curry $baz, 5, 7, 9;
print $curried->(1,2,3);
# To improve : http://www.perlmonks.org/?node_id=380421, http://www.perlmonks.org/?node_id=408304

#############################################
print "\n** Modules (cf. www.cpan.org) **";

use Pckg::Class qw(:DEFAULT &shared_on_demand :TAG_A); # DEFAULT is if there is a "qw" param to load auto shared variables ; '&' seems facultative before variables
hello( "Bob" );

my $class_name = 'Pckg::Class'; #small trick, doesn't work when calling 'use'
my $obj = $class_name->new(42, "string");
$obj = new $class_name(42, "string"); # Stricly equivalent
print $obj;
print ref($obj); # In case of inheritance : use UNIVERSAL qw(isa); if( isa( $obj, "MotherClass" ) ) { ... }
print Dumper($obj);

# For documentation on the following : http://perldoc.perl.org/UNIVERSAL.html
print '? CAN new:'.$class_name->can('new');
print '? CAN hello:'.$class_name->can('hello');
print '? CAN foo:'.$class_name->can('foo');

############################
print "\n** HTML parser **";
# FROM: http://perltuts.com/tutorials/web-scraping-with-lwp/scraping

use HTML::TreeBuilder::XPath;
use HTML::Selector::XPath;

=pod
use LWP::UserAgent;
my $ua =
  LWP::UserAgent->new(agent => 'MyWebScaper/0.1 <http://perltuts.com>');

my $response = $ua->get('http://127.0.0.1/');

my $html;
if ($response->is_success) {
    $html = $response->decoded_content;
} else {
    die $response->status_line;
}
=cut

my $html = <<'EOF';
<html>
    <head>
        <title>A sample webpage!</title>
    </head>
    <body>
        <h1>Perltuts.com rocks!</h1>
        <a href="http://perltuts.com">perltuts.com</a>
    </body>
</html>
EOF

my $tree = HTML::TreeBuilder::XPath->new;
$tree->ignore_unknown(0);
$tree->parse($html);
$tree->eof;

my @nodes = $tree->findnodes('//title');
print $nodes[0]->as_text;

my $xpath = HTML::Selector::XPath::selector_to_xpath('h1');
@nodes = $tree->findnodes($xpath);
print $nodes[0]->as_text;

$xpath = HTML::Selector::XPath::selector_to_xpath('a');
@nodes = $tree->findnodes($xpath);
my @attrs = $nodes[0]->getAttributes();
print $attrs[0]->getValue();

# SEE ALSO: http://search.cpan.org/~miyagawa/Web-Scraper-0.36/lib/Web/Scraper.pm & http://search.cpan.org/~jesse/WWW-Mechanize-1.72/lib/WWW/Mechanize.pm

#######################
print "\n** Tricks **";

my $a = 'a'; print ++$a;
my $z = 'z'; print ++$z;

my $n1; my $n2; my $n3 = 0;
my $n_def = $n1 // $n2 // $n3 // 1;
print "\$n_def = $n_def";
my $n_true = $n1 || $n2 || $n3 || 1;
print "\$n_true = $n_true";

# Turn warnings into errors : local $SIG{__WARN__} = sub { die @_ };

# Optimize tail call (not impressive)
use Benchmark;
sub normal {
    return 0 unless $_[0];
    @_ = ($_[0] - 1);
    return normal(@_);
}
sub tail {
    return 0 unless $_[0];
    @_ = ($_[0] - 1);
    goto &tail;
}
=pod
timethese( 10, {
        "normal" => sub { normal(500000) },
        "tail"   => sub {   tail(500000) },
    }
);
=cut

END {
    print("Execution END : instructions A"); # Could be nested in other block -> same behaviour
}
END {
    print("Execution END : instructions B"); # Could be nested in other block -> same behaviour
}
# Also : UNITCHECK , CHECK and INIT (see: http://perldoc.perl.org/perlmod.html#BEGIN%2C-UNITCHECK%2C-CHECK%2C-INIT-and-END)

bar("This call should crash !");
sub AUTOLOAD {
    print "Magic handling undefined subroutine call ^^";
}
# See: http://etutorials.org/Programming/perl+bioinformatics/Part+I+Object-Oriented+Programming+in+Perl/Chapter+3.+Object-Oriented+Programming+in+Perl/3.9+How+AUTOLOAD+Works/

# Creating pseudo block operations to expand the language : http://stackoverflow.com/questions/161872/hidden-features-of-perl#162601

# Perl Archiver to bundle dependancies : http://perltraining.com.au/tips/2008-05-23.html

Devel:NYTProf # per-function, per-line, per-block  & per-opcode profiler with call-graph visualiation provided by nytprofcg
Perl DTrace # real-time stats on function entry & exit

# Switch (given and when) 

# http://www.perl.com/pub/2007/06/07/better-code-through-destruction.html

# One-liners tuto : http://articles.mongueurs.net/magazines/linuxmag50.html
# - Imprime les lignes communes aux deux fichiers (posté par Randal Schwartz sur perlmonks) :
#        perl -ne 'print if ($seen{$_} .= @ARGV) =~ /10$/' fichier1 fichier2
# - Détecte les fichiers texte (un fichier est considéré comme un fichier texte par l'opérateur -T s'il contient plus de 30% de caractères "bizarres" ou un caractère nul (\0) dans le premier bloc) :
#        perl -le 'for(@ARGV) {print if -f && -T _}' *
# - Modifie des dates d'accès et de modification du fichier, pour affirmer qu'ils datent d'un mois dans le futur.
#        perl -e '$X=24*60*60; utime(time(),time() + 30 * $X,@ARGV)' fichier
# - Extrait, trie et imprime les mots d'un fichier
#        perl -0nal012e '@a{@F}++; print for sort keys %a' fichier
# - Génère un mot de passe aléatoire :
#        perl -e 'print chr(32 + rand 95) for 1..8'
# - Affiche les lignes du fichier fichier (ou du flux reçu sur l'entrée standard) par ordre croissant d'occurrence :
#        perl -ne '$c{$_}++;END{print sort { $c{$a}<=>$c{$b} } keys%c}' fichier

$ perl -MCPAN -e 'install Mon::Module' # To install modules - Sometimes the `cpan` command works better, eg: perl -MCPAN -e 'install YAML' Can't locate object method "install" via package "YAML" at -e line 1.
# Updating all outdated Perl modules (FROM: https://www.nu42.com/2012/05/updating-all-outdated-perl-modules.html)
$ cpanm --self-upgrade
$ cpan-outdated |cpanm

# Advanced : Attributes
# -> http://perldoc.perl.org/attributes.html
# -> http://perldoc.perl.org/Attribute/Handlers.html

#Files cleaning
unlink "$this_file.7z", "data.dir", "data.pag";

=pod
    FROM: http://articles.mongueurs.net/magazines/linuxmag52.html
# Dont un joli one-liner : LC_ALL=french perl -e '$! = $_, print 0 + $!, " $!\n" for 1 .. 128'

    use English qw(-no_match_vars);

    $_       $ARG
    @ARGV
    @_
    $/       $INPUT_RECORD_SEPARATOR    $RS
    $.       $INPUT_LINE_NUMBER         $NR
    $\       $OUTPUT_RECORD_SEPARATOR   $ORS
    $,       $OUTPUT_FIELD_SEPARATOR    $OFS
    $"       $LIST_SEPARATOR
    $|       $OUTPUT_AUTOFLUSH
    $@       $EVAL_ERROR
    $!       $OS_ERROR                  $ERRNO
    $?       $CHILD_ERROR
    $^E      $EXTENDED_OS_ERROR
    $0       $PROGRAM_NAME
    $$       $PROCESS_ID                $PID
    %ENV
    @INC
    $^O      $OSNAME
    $^X      $EXECUTABLE_NAME
    $^W      $WARNING
    %SIG
=cut

# integrated DATA block
my @lines = <DATA>;
for (@lines) {
    print if /bad/;
}

__DATA__
some good data
some bad data
more good data 
more good data
