#!/bin/bash

export PYTHONPATH=$PYTHONPATH:`pwd`/lib:`pwd`/plugin:`pwd`/service:

sourcecode=`find ./ -name "*.py" | tr '\n' ' '`

pylint $@ $sourcecode

true
