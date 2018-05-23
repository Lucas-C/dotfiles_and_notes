- [5 Useful Tips For A Better Commit Message](https://robots.thoughtbot.com/5-useful-tips-for-a-better-commit-message)
- adopt a convention in the shortname, like a prefix: [$issue_number] - DEV|BUGFIX - ...
- [Semantic Commit Messages](https://seesparkbox.com/foundry/semantic_commit_messages)

#-----#
# SVN #
#-----#

svn propedit svn:ignore DIR # then specify PATTERNS # svn ignore

svn propget -R svn:ignore . # Get all svn props

svn status | grep '!M' | awk '{print $2}' | xargs svn rm #--force # Rm added then removed files

svn add $(svn status | grep "^\?" | awk '{print $2}') # Add all newly files

svn status --no-ignore # Display even ignored files

svn diff --summarize -c $nb # List modifcations /commit

svn up -r $rev $file # Checkout file

svn diff | diffstat # sum-up a diff


~°~°~°~°~°~
 Mercurial
~°~°~°~°~°~
hg init / clone $url
hg pull -u # Alt: hg fetch - requires this in .hgrc : [extensions] hgext.fetch=
hg log / summary / status
hg add $file / commit
hg push -r .


::=::=::
 Bazaar
::=::=::
bzr init / branch $url
bzr pull
bzr log / diff # status
bzr mv / rm
bzr add $file / commit $files -m $msg


*******
= Git =
*******
Next/previous commits: $commit^ (first parent) & $commit~ (first child)

curl 'https://raw.githubusercontent.com/eacousineau/util/master/git-new-workdir.sh' > .git-new-workdir.sh
curl 'https://raw.githubusercontent.com/git/git/master/contrib/completion/git-completion.bash' > .bashrc_git_completion # buggy with TMUX

curl http://git-punish.io/get -o /usr/local/bin/git-punish
chmod +x /usr/local/bin/git-punish
git punish -L135,170 index.js  # generates a URL to a funny page that expires in 24 hours

gitg > gitk # GUI client/viewer

# use HTTPS protocol instead of git one (e.g. to bypass a firefall):
git config --global url."https://".insteadOf git://

git rebase --interactive # squash commits. For initial commit, use: git reset HEAD^ && git commit --all --amend

# Fix commit already pushed - FROM: http://blog.jacius.info/2008/6/22/git-tip-fix-a-mistake-in-a-previous-commit/
git commit --all --amend
gri HEAD^
git push --force-with-lease origin master # --force-with-lease >>> --force : if there are new remote commits, --force-with-lease will fail

git reset HEAD^ # Git 'uncommit', as 'don't-change-any-files-but-cancel-last-commit'

git show HEAD^:$file > $file.old # checkout an old version of a file under a different name

git revert HEAD..HEAD^^ # Rollback last pushed commit

git diff --cached HEAD # Git show changes currently 'added' (ready to be commited)
git diff --stat # Git diff with same format as 'git status'
git fsck --lost-found # list 'dangling commits' SHA1 that can be 'git show'-ed

git stash save "stash-name" # Stash with a name, then either pop or apply + drop
# Checking that all stashes have been commited:
git stash list | awk -F' ' '{for (i = 6; i <= NF; i++) printf "%s ",$i; print ""}' | while read msg; do echo "CHECKING: $msg"; git lg | grep "$msg"; done

git add -p $file # Commit only part of a file

git reflog # To list all actions done on the git repo ( not only the commits, but all commands that were run, including rebases )
git reset --hard HEAD@{3} # To rewind the repo back to the state of HEAD@{3} in the reflog lists.

git ls-files # list versioned files. Alt: git ls-tree -r --name-only HEAD
git update-index --assume-unchanged .gitconfig # ignore changes in tracked file

git log --format='%aN %aE' | sort -u # List git commiters

git bisect start
git bisect good GOOD_REVISION_OR_TAG
git bisect bad BAD_REVISION_OR_TAG # or don’t provide a revision to indicate the current revision
git bisect run $cmd
# Bisect will now step through the commits in an automated fashion, marking commits good or bad depending on the exit code of $cmd, until it find the culprit commit.
git bisect reset # to return your repository to the state it started in

git blame -L '/REGEX/',+1 FILE # 'rblame' to get an history of the changes on a line
git log --pickaxe-all --pickaxe-regex -S$regex $file # To get only the additions / deletions (ignore the small changes)
git grep $keyword $(git rev-list $rev1..$rev2) $file # or rev-list --all Also: -function-context to show the whole function as context that was affected by a change

git submodule update --init # initialize a repo that has .gitmodules
git submodule add URL DIRNAME # Incorporate a repo in another repo - http://git-scm.com/book/en/Git-Tools-Submodules

git tag # Add vX.Y tags to commits
# - can be signed with GPG with -s
# - must be manually pushed or 'git push --tags'

git branch -u origin/master # Set remote branch to track
git branch -d $branch_name # Delete branch
git branch -m old_name new_name # Rename branch
git push ${remote_name:-origin} $branch_name # create remote branch
git remote set-url origin https://github.com/Lucas-C/... # change a remote URL, useful for rebasing on a fork for a Pull reuqest
# Show branch info:
git branch -av
git remote show origin

git fetch upstream && git rebase upstream/master && git push --force-with-lease # Sync a fork

### Work on feature branches rather than mainline : best practice, or not ? -> https://speakerdeck.com/tdpauw/xp2017-feature-branching-is-evil
# Create a new feature branch:
git co -b $branch_name --track origin/mainline # checkout -b <=> create branch && checkout
# Commit feature branch and fast forward changes to mainline
git co featureBranch
git ci
git co mainline
git merge featureBranch
# Then rebase the other feature branches
git co anotherFeatureBranch
git rebase mainline
# Fast forward main to merge other branches in
git co mainline
git merge anotherFeatureBranch
# Push from mainline
git co mainline
gri
git push

.git/hooks/post-receive # any executable, e.g. bash script
pre-commit/pre-commit # great hooks manager + cf. https://github.com/Yelp/venv-update/blob/a5960acab7101a1e70c57945b2038fef9d005aed/.pre-commit-config.yaml#L15-L22

# Only checkout a subdirectory
git config core.sparsecheckout true
echo subdir/path/ >> .git/info/sparse-checkout

git cherry-pick $sha # copy a commit from another branch into the current branch

git update-index --assume-unchanged $file # ignore changes to a file that's already tracked in the repository

git diff --no-color -U999999 --no-prefix HEAD^ | crucible.py $CR_ID --newpatch # https://confluence.atlassian.com/crucible/creating-reviews-from-the-command-line-335479612.html#Creatingreviewsfromthecommandline-InstallingtheReviewCLItool

git-hash-object () { # substitute when the `git` command is not available
    local type=blob
    [ "$1" = "-t" ] && shift && type=$1 && shift
    # depending on eol/autocrlf settings, you may want to substitute CRLFs by LFs
    # by using `perl -pe 's/\r$//g'` instead of `cat` in the next 2 commands
    local size=$(cat $1 | wc -c | sed 's/ .*$//')
    ( echo -en "$type $size\0"; cat "$1" ) | sha1sum | sed 's/ .*$//'
}
# Retrieve a file version (commit) in a git history based on its SHA hash, for example to identify a deployed file
git-identify () { # USAGE: git-identify file hash
    local file=${1?}
    local hash=${2?}
    git log --format="%h %s" $file | while read commit msg; do
        if [ $(git rev-parse $commit:$file) = "$hash" ]; then
            echo $commit $msg - oldest tag including this commit: $(git tag --contains $commit | head -n 1)
            break
        fi
    done
}

# Checkout GitHub pull requests locally: add the following line in corresponding .git/config section - FROM: https://gist.github.com/piscisaureus/3342247
[remote "origin"]
    fetch = +refs/pull/*/head:refs/remotes/origin/pr/*
$ git fetch origin
$ git checkout pr/999
# Does not allow to push. One must follow this process to do so: https://help.github.com/articles/committing-changes-to-a-pull-request-branch-created-from-a-fork/


++++++
+ p4 +
++++++
p4 info | grep 'Client root'
p4 client -o
p4 depots
p4 opened -C $USER # assuming that $USER is a client

# status
find . -type f -print0 | xargs -0 p4 fstat -T clientFile,action

# Display protections in place for a given user/path
p4 protects
# Groups a user belong to
p4 groups -i $USER

# It will shelve (locally save changes) changes with id 7731531
p4 shelve –c 7731531
# to update the changes
p4 shelve –f –c 7731531
#
p4 unshelve -s 7731531
