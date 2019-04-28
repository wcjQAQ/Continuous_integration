#!/usr/bin/env bash
# names : branch.sh

git_url=$1

branch=$(git ls-remote -h $git_url|awk -vFS='[/]+' '{a=a?a","$NF:$NF}END{print a}')

echo $branch
