#!/bin/bash
cat $HOME/NorsePi/XML/LastHourReadable.json | grep time | sed -n '1p;$p'
