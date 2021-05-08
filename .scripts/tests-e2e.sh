#!/bin/bash

VERSION=$(grep -Eo '[0-9]+\.[0-9]+\.[0-9]+' _kosmorro/__version__.py)
PYTHON_BIN=$(command -v python)
PIP_BIN=$(command -v pip)

if python3 --version > /dev/null; then
    PYTHON_BIN=$(command -v python3)
    PIP_BIN=$(command -v pip3)
fi

failures=''

function fail() {
    failures="$failures\n\n - $1\n\n$2"
}

function run() {
    eval "$1" &> /tmp/output.txt
    return $?
}

function canRun() {
    if [[ "$1" != "" && "$1" != "$ENVIRONMENT" ]]; then
        return 1
    fi

    return 0
}

# Asserts that command $1 has finished with sucess
# $1: the command to run
function assertSuccess() {
    if ! canRun "$2"; then
        echo -n 'I'
        return
    fi

    run "$1"
    returned=$?

    if [ $returned -ne 0 ]; then
      fail "Failed asserting that command '$1' finishes with success, returned status $returned." "$(cat /tmp/output.txt)"
      echo -n 'F'
      return
    fi

    echo -n '.'
}

# Asserts that command $1 has finished with sucess
# $1: the command to run
function assertFailure() {
    if ! canRun "$2"; then
        echo -n 'I'
        return
    fi

    run "$1"
    returned=$?

    if [ $returned -eq 0 ]; then
      fail "Failed asserting that command '$1' finishes with failure." "$(cat /tmp/output.txt)"
      echo -n 'F'
      return
    fi

    echo -n '.'
}

mkdir -p $HOME/kosmorro/export

echo
echo "==== RUNNING E2E TESTS ===="
echo

# Create the package and install it
assertSuccess "make build"
assertSuccess "$PIP_BIN install dist/kosmorro-$VERSION.tar.gz" "CI"

KOSMORRO_COMMAND="kosmorro --debug"

assertSuccess "$KOSMORRO_COMMAND"
assertSuccess "$KOSMORRO_COMMAND -h"
assertSuccess "$KOSMORRO_COMMAND -d 2020-01-27"
assertFailure "$KOSMORRO_COMMAND -d yolo-yo-lo"
assertFailure "$KOSMORRO_COMMAND -d 2020-13-32"
assertFailure "$KOSMORRO_COMMAND --date=1789-05-05"
assertFailure "$KOSMORRO_COMMAND --date=3000-01-01"
assertSuccess "$KOSMORRO_COMMAND --date='+3y 5m3d'"
assertSuccess "$KOSMORRO_COMMAND --date='-1y3d'"
assertFailure "$KOSMORRO_COMMAND --date='+3d4m"
assertFailure "$KOSMORRO_COMMAND -date='3y'"
assertSuccess "$KOSMORRO_COMMAND --latitude=50.5876 --longitude=3.0624"
assertSuccess "$KOSMORRO_COMMAND --latitude=50.5876 --longitude=3.0624 -d 2020-01-27"
assertSuccess "$KOSMORRO_COMMAND --latitude=50.5876 --longitude=3.0624 -d 2020-01-27 --timezone=1"
assertSuccess "$KOSMORRO_COMMAND --latitude=50.5876 --longitude=3.0624 -d 2020-01-27 --timezone=-1"
assertSuccess "$KOSMORRO_COMMAND --latitude=50.5876 --longitude=3.0624 -d 2020-01-27 --format=json"
assertFailure "$KOSMORRO_COMMAND --latitude=50.5876 --longitude=3.0624 -d 2020-01-27 --format=pdf"

# Environment variables
assertSuccess "LATITUDE=50.5876 LONGITUDE=3.0624 TIMEZONE=1 kosmorro -d 2020-01-27"
assertSuccess "LATITUDE=50.5876 LONGITUDE=3.0624 TIMEZONE=-1 kosmorro -d 2020-01-27"

# Missing dependencies, should fail
assertFailure "$KOSMORRO_COMMAND --latitude=50.5876 --longitude=3.0624 -d 2020-01-27 --format=pdf -o $HOME/kosmorro/export/document.pdf"
assertFailure "ls $HOME/kosmorro/export/document.pdf"

assertSuccess "sudo apt-get install -y texlive texlive-latex-extra" "CI"

# Dependencies installed, should not fail
assertSuccess "$KOSMORRO_COMMAND --latitude=50.5876 --longitude=3.0624 -d 2020-01-27 --format=pdf -o $HOME/kosmorro/export/document.pdf"
assertSuccess "ls $HOME/kosmorro/export/document.pdf"

assertSuccess "$KOSMORRO_COMMAND --latitude=50.5876 --longitude=3.0624 -d 2020-01-27 --format=pdf -o $HOME/kosmorro/export/document-no-graph.pdf --no-graph"
assertSuccess "ls $HOME/kosmorro/export/document-no-graph.pdf"

# man page
assertSuccess "man --pager=cat kosmorro"

if [ "$failures" != "" ]; then
    echo -e "\n$failures"
    exit 2
fi

echo -e "\n\n==== TESTS RAN SUCCESSFULLY 👍 ===="
