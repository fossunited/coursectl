#! /bin/bash
#
# Script to run all the tests.
#

exec py.test --flakes "$@"
