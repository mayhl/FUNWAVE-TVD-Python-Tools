#!/bin/bash
#

CMD="bokeh serve --show"

PIDS=$(ps aux | grep "$CMD" | grep -v grep | awk '{print $2}' | xargs)
kill -9 $PIDS


python $1

if [ $? -eq 0 ]; then
	$CMD $1
fi
