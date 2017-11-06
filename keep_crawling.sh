#!/bin/bash
while true
do
    echo "Press CTRL+C to stop the script execution"
    scrapy crawl crashreport
    sleep 20s
done
