  #!/bin/bash

# Set the `errexit` option to make sure that
# if one command fails, all the script execution
# will also fail (see `man bash` for more 
# information on the options that you can set).
set -o errexit

# This is the main routine of our bash program.
# It makes sure that we've supplied the necessary
# arguments, then it prints a CSV header and then
# keeps making requests and printing their responses.
#
# Note.: because we're calling `curl` each time in
#        the loop, a new `curl` process is created for 
#        each request. 
#       
#        This means that a new connection will be made 
#        each time.
#       
#        Such property might be useful when you're testing
#        if a given load-balancer in the middle might be
#        messing up with some requests.
main () {
  local url=$1

  if [[ -z "$url" ]]; then
    echo "ERROR:
  An URL must be provided.

  Usage: check-res <url>

Aborting.
    "
    exit 1
  fi

#  print_header
  for i in `seq 1 10`; do
    make_request $url
  done
}

# This method does nothing more that just print a CSV
# header to STDOUT so we can consume that later when
# looking at the results.
print_header () {
  echo "code,time_total,time_connect,time_appconnect,time_starttransfer"
}

# Make request performs the actual request using `curl`. 
# It specifies those parameters that we've defined before,
# taking a given `url` as its parameter.
make_request () {
  local url=$1

  curl \
    --write-out "%{http_code},%{time_total}\n" \
    --silent \
    --output /dev/null \
    -H 'Content-Type: application/json' \
    -H 'Postman-Token: 82eea0cc-7db3-4698-b826-3acd88df44c0' \
    -H 'cache-control: no-cache' \
    -d '     { "size" : 1000, 
     	"sort": [
        {
          "@timestamp": {
            "order": "desc"
          }
        }
      ],
        "query" : {
            "bool" : {
                "must_not" : [{"match" : {"SourceLocation.keyword": "10.0.0.0-10.255.255.255"}}]
            }
        }
    }' \
    -X GET \
    "$url"
}

main "$@"
  
  
  
