#-----#
# SVN #
#-----#

svn propedit svn:ignore DIR # then specify PATTERNS # svn ignore

svn propget -R svn:ignore . # Get all svn props

svn status | grep '!M' | awk '{print $2}' | xargs svn rm #--force # Rm added then removed files

svn add $(svn status | grep "^\?" | awk '{print $2}') # Add all newly files

svn status --no-ignore # Display even ignored files

svn diff --summarize -c <nb> # List modifcations /commit

svn up -r <rev> <file> # Checkout file

svn diff | diffstat # sum-up a diff


#*****#
# Git
#*****#
# http://blog.jacius.info/2008/6/22/git-tip-fix-a-mistake-in-a-previous-commit/

# Git 'uncommit', as 'don't-change-any-files-but-cancel-last-commit'
git reset HEAD^

# Rollback last pushed commit
git revert HEAD

# Git show changes currently 'added' (ready to be commited)
git diff --cached HEAD
# Git diff with same format as 'git status'
git diff --stat

# Stash with a name, then either pop or apply + drop
git stash save "stash-name"

# Commit only part of a file
git add -p <file>

# Reflog
git reflog # To list all actions done on the git repo ( not only the commits, but all commands that were run, including rebases )
git reset --hard HEAD@{3} # To rewind the repo back to the state of HEAD@{3} in the reflog lists.

# List versioned files
git ls-tree -r --name-only HEAD

# List git commiters
git log --format='%aN %aE' | sort -u

# Git bisect
git bisect start
git bisect good GOOD_REVISION_OR_TAG
git bisect bad BAD_REVISION_OR_TAG # or don’t provide a revision to indicate the current revision
git bisect run <cmd>
# Bisect will now step through the commits in an automated fashion, marking commits good or bad depending on the exit code of <cmd>, until it find the culprit commit.
git bisect reset # to return your repository to the state it started in

# Git log blame a REGEX
git blame -L '/REGEX/',+1 FILE
# To get an history of the changes on a line, use the 'rblame' alias
# To get only the additions / deletions (ignore the small changes) :
git log --pickaxe-all --pickaxe-regex -S'REGEX' -- FILE

# Grep
git grep <keyword> $(git rev-list <rev1>..<rev2>) [–function-context]

# Incorporate a repo in another repo
git submodule add URL DIRNAME # http://git-scm.com/book/en/Git-Tools-Submodules

# Adding vX.Y tags to commits
# - can be signed with GPG with -s
# - must be manually pushed or 'git push --tags'
git tag

# Branch infos
git branch -av
git remote show origin
# Set remote branch to track
git branch -u origin/master
# Delete branch
git branch -d $branch_name

### Best-practice: work on feature branches rather than mainline
# Create a new feature branch:
git branch <branch name> --track origin/mainline
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
