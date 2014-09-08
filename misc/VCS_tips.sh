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


#*****#
# Git
#*****#
curl 'https://raw.githubusercontent.com/eacousineau/util/master/git-new-workdir.sh' > .git-new-workdir.sh
curl 'https://raw.githubusercontent.com/git/git/master/contrib/completion/git-completion.bash' > .bashrc_git_completion # buggy with TMUX

# use HTTPS protocol instead of git one (e.g. to bypass a firefall):
git config --global url."https://".insteadOf git://

# Fix commit already pushed - FROM: http://blog.jacius.info/2008/6/22/git-tip-fix-a-mistake-in-a-previous-commit/
git stash
gri HEAD^ # -> 'edit'
git stash apply
git commit --all --ammend
git rebase --continue
git push -f origin master # you DON'T want to do that if others have already pulled you last commit

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

git log --format='%aN %aE' | sort -u # List git commiters

git bisect start
git bisect good GOOD_REVISION_OR_TAG
git bisect bad BAD_REVISION_OR_TAG # or don’t provide a revision to indicate the current revision
git bisect run $cmd
# Bisect will now step through the commits in an automated fashion, marking commits good or bad depending on the exit code of $cmd, until it find the culprit commit.
git bisect reset # to return your repository to the state it started in

git blame -L '/REGEX/',+1 FILE # 'rblame' to get an history of the changes on a line
git log --pickaxe-all --pickaxe-regex -S$regex $file # To get only the additions / deletions (ignore the small changes)
git grep $keyword $(git rev-list $rev1..$rev2) $file # or rev-list --all Also: -function-context

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

### Best-practice: work on feature branches rather than mainline
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


+++++
+ p4
+++++
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
