
#!/bin/bash

if [ "$2" != "" ]; then
    cat $1 | python3 -m json.tool | tee $2 
else
    cat $1 | python3 -m json.tool | tee $1-readable.json 
fi
