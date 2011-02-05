#!/bin/bash

echo Connecting to $1
ssh john-2.local tail -f -c +0 /Users/anne/education/bodytrack/zeologger/raw-data/$1 > $1
