#!/bin/bash
# Shared there: https://chezsoi.org/shaarli/shaare/a--SwQ
set -o pipefail -o errexit -o nounset

# Install required extension: gh extension install twelvelabs/gh-repo-config
# -> it's a set of Bash scripts: https://github.com/twelvelabs/gh-repo-config/blob/main/gh-repo-config

config_dir=.github/config/branch-protection
cp $config_dir/main.json .
yq -iP -o json .required_pull_request_reviews=null $config_dir/main.json
yq -iP -o json .required_status_checks.checks=[]   $config_dir/main.json
gh repo-config apply
git push
mv main.json $config_dir/
gh repo-config apply

# API v3 doc to understand fields in .github/config/branch-protection/: https://docs.github.com/en/rest/branches/branch-protection#update-branch-protection--parameters

exit 0

# GraphQL doc on BranchProtectionRule: https://docs.github.com/en/graphql/reference/objects#branchprotectionrule
# List all BranchProtectionRule for py-pdf/pdfly:
gh api graphql -f query='{
  repository(owner: "py-pdf", name: "pdfly") {
    branchProtectionRules(first: 10) {
      edges {
        node {
          allowsDeletions
          allowsForcePushes
          blocksCreations
          dismissesStaleReviews
          isAdminEnforced
          lockAllowsFetchAndMerge
          lockBranch
          pattern
          requireLastPushApproval
          requiredApprovingReviewCount
          requiredDeploymentEnvironments
          requiresApprovingReviews
          requiresCodeOwnerReviews
          requiresCommitSignatures
          requiresConversationResolution
          requiresDeployments
          requiresLinearHistory
          requiresStatusChecks
          requiresStrictStatusChecks
          restrictsPushes
          restrictsReviewDismissals
        }
      }
    }
  }
}'
