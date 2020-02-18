#!/bin/bash

VERSION=$(grep -Eo '[0-9]+\.[0-9]+\.[0-9]+' kosmorrolib/version.py)
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

echo
echo "==== RUNNING E2E TESTS ===="
echo

# Create the package and install it
assertSuccess "$PYTHON_BIN setup.py sdist"
assertSuccess "$PIP_BIN install dist/kosmorro-$VERSION.tar.gz" "CI"

assertSuccess kosmorro
assertSuccess "kosmorro --latitude=50.5876 --longitude=3.0624"
assertSuccess "kosmorro --latitude=50.5876 --longitude=3.0624 -d 27 -m 1 -y 2020"
assertSuccess "kosmorro --latitude=50.5876 --longitude=3.0624 -d 27 -m 1 -y 2020 --timezone=1"
assertSuccess "kosmorro --latitude=50.5876 --longitude=3.0624 -d 27 -m 1 -y 2020 --timezone=-1"
assertSuccess "kosmorro --latitude=50.5876 --longitude=3.0624 -d 27 -m 1 -y 2020 --format=json"
assertFailure "kosmorro --latitude=50.5876 --longitude=3.0624 -d 27 -m 1 -y 2020 --format=pdf"
# Missing dependencies, should fail
assertFailure "kosmorro --latitude=50.5876 --longitude=3.0624 -d 27 -m 1 -y 2020 --format=pdf -o /tmp/document.pdf"

assertSuccess "sudo apt-get install -y texlive" "CI"
assertSuccess "$PIP_BIN install latex" "CI"

# Dependencies installed, should not fail
assertSuccess "kosmorro --latitude=50.5876 --longitude=3.0624 -d 27 -m 1 -y 2020 --format=pdf -o /tmp/document.pdf"

if [ "$failures" != "" ]; then
    echo -e "\n$failures"
    exit 2
fi

echo -e "\n\n==== TESTS RAN SUCCESSFULLY 👍 ===="
