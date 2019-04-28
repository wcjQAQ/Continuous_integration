#!/usr/bin/env bash
# get_tag.sh

git_url=$1
[[ ! $git_url == git* ]] && echo "please enter git url" && exit 1
Tags=$(git ls-remote --tags -h $git_url)

TagChoise=$(awk -vFS='/' 'BEGIN{printf "请选择上线的版本号,"}/tags/&&/[0-9][0-9]$/{a[++m]=$NF}END{for(i=m;i>=1;i--)printf a[i]","}' <<< "$Tags")

echo $TagChoise
