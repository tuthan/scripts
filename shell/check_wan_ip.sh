#!/bin/bash
#https://wiki.archlinux.org/title/msmtp - to setup the email account (gmail)
ip_file="/home/hvo/wan_ip.txt"
SMTPTO="Email_recived@domain.com"

SUBJECT="Public IP address has changed"

if [ ! -f "$ip_file" ] ; then
   touch "$ip_file"
fi

WAN_IP=`curl -s ifconfig.me/ip`

echo "Public IP address is: $WAN_IP"

while read line
do
   if [ "$line" = "$WAN_IP" ]
   then
      echo "Public IP did not change."
   else
      echo "Public IP has changed. Writing new value..."
      echo "$WAN_IP" > "$ip_file"
      echo "Mailing the admin..."
      MESSAGE="Network configuration change warning! The IP address is now $WAN_IP."
      printf "Subject: $SUBJECT\n$MESSAGE" | msmtp $SMTPTO
   fi

done < "$ip_file"