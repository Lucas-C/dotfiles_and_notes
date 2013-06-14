#-----#
# SVN #
#-----#

# Svn ignore
svn propedit svn:ignore DIR # then specify PATTERNS

# Get all svn props
svn propget -R svn:ignore .

# Rm added then removed files
svn status | grep '!M' | awk '{print $2}' | xargs svn rm #--force

# Display even ignored files
svn status --no-ignore

# List modifcations /commit
svn diff --summarize -c <nb>

# Checkout file
svn up -r <rev> <file>


#*****#
# Git
#*****#
# http://blog.jacius.info/2008/6/22/git-tip-fix-a-mistake-in-a-previous-commit/

# Git 'un-commit', as 'don't-change-any-files-but-cancel-last-commit'
git reset HEAD^

# Git show changes currently 'added' (ready to be commited)
git diff --cached HEAD

# Stash with a name, then either pop or apply + drop
git stash save "stash-name"

# Reflog
git reflog # To list all actions done on the git repo ( not only the commits, but all commands that were run, including rebases )
git reset --hard HEAD@{3} # To rewind the repo back to the state of HEAD@{3} in the reflog lists.

# List versioned files
git ls-tree --name-only HEAD

# Git bisect
git bisect start
git bisect good GOOD_REVISION_OR_TAG
git bisect bad BAD_REVISION_OR_TAG # or don’t provide a revision to indicate the current revision
git bisect run <cmd>
# Bisect will now step through the commits in an automated fashion, marking commits good or bad depending on the exit code of <cmd>, until it find the culprit commit.
git bisect reset # to return your repository to the state it started in

# Rollback last pushed commit
git revert HEAD

# List git commiters
git log --format='%aN %aE' | sort -u

# Git log blame a regex
git blame -L '/<regex>/',+1 <file>

# Grep
git grep <keyword> $(git rev-list <rev1>..<rev2>) [–function-context]

# Commit only part of a file
git add -p <file>


+++++
+ p4
+++++
# status
find . -type f -print0 | xargs -0 p4 fstat -T clientFile,action

