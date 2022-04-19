# scripts
Collection of script I use

- ps -ef | grep 'nginx' | grep -v grep | awk '{print $2}' | xargs -r kill -9