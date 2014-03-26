#!/bin/sh
#FROM: curl 'https://raw.githubusercontent.com/eacousineau/util/master/git-new-workdir.sh' > .git-new-workdir.sh
#(fork of official git/git/contrib/workdir/git-new-workdir)

# update-head - How to update to a detached head?

bin_path=$0
bin=$(basename $bin_path)
# See `git-repack`
OPTIONS_SPEC="\
git-new-workdir [options] <repository> <new_workdir> [<commit>]
git-new-workdir --show-orig <repository>
--
bare                 checkout as a bare git repository
link-head            link 'HEAD' file as well (useful for tracking stuff as submodules)
no-checkout          don't checkout the files (useful for submodules)

 Management
show-orig            print original repo's directory
update-config        replace workdir's config with original's config
update-head          replace workdir's HEAD with original's HEAD (since it can be made a symlink).\
 Note that this does not update the repo's index nor tree. Use 'git reset HEAD' or 'git checkout -f HEAD' to resolve that.

 Submodules
always-link-config   link 'config' file, even if using on a submodule.\
 Otherwise, a copy of the config is made.
c,constrain          use git-config scm.focusGroup (submodule-ext) to checkout selected submodules
ignore-submodules    do not try to checkout submodules
use-gitdir-modules   link submodules to \$GIT_DIR/modules/\$path, and rely on submodule mechanisms to checkout working copy.
"
# How to get this to show up in basic help? It seems to be either option spec or long usage....
LONG_USAGE='Checkout a branch / commit of an existing Git repository to a new location,
linking to the original object database, refs, config (if not a supermodule), etc., so
that the git database is the same between the original Git repository and the new
working directory.'
NONGIT_OK=1

export PATH=$PATH:$(git --exec-path) # Put git libexec on path

. git-sh-setup

always_link_config=
bare=
ignore_submodules=
use_gitdir_modules=
constrain=
link_head=
show_orig=
update_config=
update_head=
no_checkout=

recurse_flags=

while test $# -gt 0
do
	case "$1" in
	--always-link-config)
		always_link_config=1
		recurse_flags="$recurse_flags --always-link-config";;
	--bare)
		bare=1;;
	--ignore-submodules)
		ignore_submodules=1;;
	--use-gitdir-modules)
		use_gitdir_modules=1;;
	-c|--constrain)
		constrain=1;;
	--link-head)
		link_head=1;;
	--show-orig)
		show_orig=1;;
	--update-config)
		update_config=1;;
	--update-head)
		update_head=1;;
	--no-checkout)
		no_checkout=1;;
	--) shift; break;;
	*) usage;;
	esac
	shift
done

if test -n "$show_orig"
then
    if test $# -ne 1
    then
        usage
    fi
else
    if test $# -lt 2 || test $# -gt 3
    then
        usage
    fi
fi


get_git_dir()
{
	( cd $1 && git rev-parse --git-dir ) 2>/dev/null 
}

get_orig_gitdir()
{
	# want to make sure that what is pointed to has a .git directory ...
	orig_gitdir=$(get_git_dir "$orig_workdir") || die "Not a git repository: \"$orig_workdir\""
	# make sure the links use full paths
	case "$orig_gitdir" in
	.git)
		orig_gitdir="$orig_workdir/.git"
		;;
	.)
		orig_gitdir=$orig_workdir
		;;
	esac
	orig_gitdir=$(readlink -f $orig_gitdir)
}

get_new_gitdir()
{
	if test -z "$bare"
	then
		new_gitdir="$new_workdir/.git"
	else
		new_gitdir="$new_workdir"
	fi
}

git_dir_check_hack()
{
	( cd $1 && test -e HEAD -a -e config -a -d refs )
}

copy_config()
{
	x=config
	orig_config="$orig_gitdir/$x"
	new_config="$new_gitdir/$x"
	# Allow submodules to be checked out
	if test -z "$always_link_config" && git config -f "$orig_config" core.worktree > /dev/null
	then
		echo "\t[ Note ] Copying .git/config and unsetting core.worktree"
		cp "$orig_gitdir/$x" "$new_config"
		git config -f "$new_config" --unset core.worktree
	else
		ln -s "$orig_config" "$new_config"
	fi
}

# TODO Make first argument just 'workdir', and later assign it to orig workdir?
orig_workdir=$1
get_orig_gitdir

if test -n "$show_orig"
then
	cd $orig_gitdir
	test -h "$orig_gitdir/refs" || die "'$orig_workdir' is not a new workdir (just a Git repo?)"
	if test -e orig_workdir
	then
		cat orig_workdir
	else
		real_gitdir=$(dirname $(readlink -f $orig_gitdir/refs))
		cd $real_gitdir
		workdir=$(git rev-parse --show-toplevel)
		if test -z "$workdir"
		then
			# Just try to go up a directory
			echo "WARNING: Could not get --show-toplevel to work. Just going to guess it's up a directory." >&2
			cd .. && workdir="$PWD"
		fi
		echo "$workdir"
	fi
	return 0
fi

resolve_orig_gitdir()
{
	# Crappy function names, bad names...
	new_workdir="$orig_workdir"
	get_new_gitdir
	orig_workdir="$(git-new-workdir --show-orig $orig_workdir)" || exit $?
	get_orig_gitdir
}

if test -n "$update_config"
then
	resolve_orig_gitdir
	if test -h "$new_gitdir/config"
	then
		echo "config is already a symlink, no need to update"
	else
		rm -f "$new_gitdir/config"
		# Need to move HEAD so that Git doesn't complain about worktree stuff???
		mv "$new_gitdir/HEAD" "$new_gitdir/HEAD_"
		copy_config
		mv "$new_gitdir/HEAD_" "$new_gitdir/HEAD"
	fi
	return 0
fi

if test -n "$update_head"
then
	resolve_orig_gitdir
	# Meh, ignore staging
	echo "Updating head"
	cp "$orig_gitdir/HEAD" "$new_gitdir/HEAD"
	return 0
fi

# See if it's a workdir, resolve orig_workdir to that working directory
if test -h "$orig_gitdir/refs"
then
	echo "This is a workdir."
	old_workdir="$orig_workdir"
	orig_workdir=$(git-new-workdir --show-orig "$orig_workdir") || die "\tCould not resolve original directory"
	echo "\tResolving to original workdir: $orig_workdir"
	get_orig_gitdir
fi

new_workdir=$2
branch=$3

# don't recreate a workdir over an existing repository
orig_workdir_abs="$(cd $orig_workdir && pwd)"
death_hint=""
if test "$new_workdir" != "${new_workdir%/}"
then
	# Trailing slash, try to add
	basedir="$new_workdir"
	new_workdir="$new_workdir$(basename $orig_workdir_abs)"
	test -e "$basedir" || die "Intermediate directory '$basedir' does not exist, cannot create '$new_workdir'. (The trailing slash means that the basename of orig workdir will be appended)".
else
	death_hint=" (did you forget the trailing '/' ?)"
fi

test -e "$new_workdir" && die "New workdir '$new_workdir' already exists$death_hint"

get_new_gitdir

# don't link to a configured bare repository
isbare=$(git --git-dir="$orig_gitdir" config --bool --get core.bare)
if test ztrue = z$isbare -a -z "$bare"
then
	die "\"$orig_gitdir\" has core.bare set to true," \
		" remove from \"$orig_gitdir/config\" to use $0"
fi

# create the gitdir
mkdir -p "$new_gitdir" || die "unable to create \"$new_gitdir\"!"

new_workdir_abs="$(cd $new_workdir && pwd)"
echo "[ Old -> New ]\n\t$orig_workdir_abs\n\t$new_workdir_abs"


# create the links to the original repo.  explicitly exclude index, HEAD and
# logs/HEAD from the list since they are purely related to the current working
# directory, and should not be shared.
for x in refs logs/refs objects info hooks packed-refs remotes rr-cache svn
do
	case $x in
	*/*)
		mkdir -p "$(dirname "$new_gitdir/$x")"
		;;
	esac
	ln -s "$orig_gitdir/$x" "$new_gitdir/$x"
done

# Add in quick file that points to original work dir
echo "$orig_workdir_abs" > "$new_gitdir/orig_workdir"

copy_config

is_supermodule=
# Still checkout submodules if bare? Yes, that way we can see the log
if test -z "$ignore_submodules"
then
	set -e -u
	x=modules
	orig_modules="$orig_gitdir/$x"
	new_modules="$new_gitdir/$x"
	if test -n "$use_gitdir_modules" -a -d "$orig_modules"
	then
		echo "[ Supermodule ] Applying $bin --bare to .git/modules/\*"
		is_supermodule=1
		# Checkout bare directories
		recurse_flags="$recurse_flags --bare"

		modulate()
		{
			orig_path=$1
			new_path=$2
			modules=$(dir $orig_path)
			for module in $modules
			do
				orig_module=$orig_path/$module
				new_module=$new_path/$module
				# If it's not a git module itself, then it might be a directory containing them. GO MONKEY GO!
				if git_dir_check_hack $orig_module
				then
					# Teh recursion
					echo "[ Submodule \"$module\" ]"
					$bin_path $recurse_flags $orig_module $new_module
				else
					# Recurse directory
					( modulate $orig_module $new_module )
				fi
				# See if it's a git module
			done
		}

		modulate $orig_modules $new_modules
	elif test -e "$orig_workdir/.gitmodules" -a -z "$bare"
	then
		is_supermodule=1
		echo "[ Supermodule ] Applying $bin to submodules for $orig_workdir"
		# Checkout new working directories
		list_flags=""
		if test -n "$constrain"
		then
			list_flags="--constrain"
		fi

		(
			cd $orig_workdir
			git submodule-ext foreach $list_flags -- "$bin $recurse_flags . $new_workdir_abs/\$path"
		)
	fi
fi

# copy the HEAD from the original repository as a default branch
if test -z "$link_head"
then
	cp "$orig_gitdir/HEAD" $new_gitdir/HEAD
else
	# Link it if so desired
	echo "WARNING: This does not seem to work." >&2
	ln "$orig_gitdir/HEAD" $new_gitdir/HEAD
fi

if test -z "$bare" -a -z "$no_checkout"
then
	# now setup the workdir
	cd "$new_workdir"
	# checkout the branch (either the same as HEAD from the original repository, or
	# the one that was asked for)
	git checkout -f $branch > /dev/null

	# Update submodules - TODO Use `git sube` to allow --constrain option to be recursive	?
	if test -n "$is_supermodule"
	then
		echo "Updating / initializing submodules"
		if test -n "$constrain"
		then
			modules=$(git config scm.focusGroup)
		else
			modules=
		fi
		git submodule update --init --recursive --checkout -- $modules
	fi
fi
