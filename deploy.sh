#!/usr/bin/env bash
set -e

BRANCH=master
TARGET_REPO=wiseturtles/wiseturtles.github.io
PELICAN_OUTPUT_FOLDER=output

function show()
{
    echo -e "\033[32;1m==========================\033[0m"
    echo -e "\033[34;1m[INFO]$1\033[0m"
    echo -e "\033[32;1m==========================\033[0m"
}

if [ "$TRAVIS_PULL_REQUEST" == "false" ]; then
    show "Starting to deploy to Github Pages"
    if [ "$TRAVIS" == "true" ]; then
        git config --global user.email "lianglin999@gmail.com"
        git config --global user.name "crazygit"
    fi
    # using token to clone repo
    git clone --quiet --branch=$BRANCH --recursive https://${GH_TOKEN}@github.com/$TARGET_REPO blog-html > /dev/null
    # go into directory and copy data we're interested in to that directory
    cd blog-html
    rsync -avq --delete --exclude=.git --exclude="theme/.webassets-cache/" ../$PELICAN_OUTPUT_FOLDER/ .
    #add, commit and push files
    git add -Af .
    git commit -m "Travis build $TRAVIS_BUILD_NUMBER pushed to Github Pages"
    git push -fq origin $BRANCH > /dev/null
    show "Deploy completed"
fi
