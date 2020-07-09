#!/bin/bash

# Generates a YYYY-MM-DD tag for every day where a commit was made

# USAGE: git_tags_from_date.sh $starting_ref

set -o pipefail -o errexit -o nounset

git rev-list $1..HEAD | tac | while read ref; do
    tag=$(git show -s --format="%ci" $ref | cut -d' ' -f1)
    if git rev-parse $tag >/dev/null 2>&1; then
        git tag -d $tag
    fi
    git tag $tag $ref
done
