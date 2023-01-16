#  Change Merit to set the primary NIC for Windows PC with multiple NICs


 http://superuser.com/questions/364978/windows-7-set-default-network-connection refers to http://support.microsoft.com/kb/299540
http://levynewsnetwork.wordpress.com/2011/12/01/windows-7-default-internet-connection-choice/ didn’t try this.

Before change the Merit, trace to google.com goes through 192.168.2.11
```
C:\>route print
IPv4 Route Table
===========================================================================
Active Routes:
Network Destination        Netmask          Gateway       Interface  Metric
          0.0.0.0          0.0.0.0     172.16.184.1   172.16.184.149     25
          0.0.0.0          0.0.0.0      192.168.2.1     192.168.2.11     20
        127.0.0.0        255.0.0.0         On-link         127.0.0.1    306
…..

C:\ >tracert www.google.com

Tracing route to www.google.com [74.125.226.18]
over a maximum of 30 hops:

  1     4 ms     3 ms     3 ms  192.168.2.1
. . . . . .
  8   109 ms   121 ms   105 ms  yyz06s05-in-f18.1e100.net [74.125.226.18]
```
 After change the Merit, trace to google.com goes through 172.16.184.149 

IPv4 Route Table
```
Active Routes:
Network Destination        Netmask          Gateway       Interface  Metric
          0.0.0.0          0.0.0.0     172.16.184.1   172.16.184.149     25
          0.0.0.0          0.0.0.0      192.168.2.1     192.168.2.11     50
        127.0.0.0        255.0.0.0         On-link         127.0.0.1    306
        127.0.0.1  255.255.255.255         On-link         127.0.0.1    306
  127.255.255.255  255.255.255.255         On-link         127.0.0.1    306
…..

C:\ >tracert www.google.com

Tracing route to www.google.com [74.125.226.18]
over a maximum of 30 hops:

  1     5 ms    11 ms     5 ms  172.16.184.252
. . . . . .
10     7 ms     8 ms     7 ms  yyz06s05-in-f18.1e100.net [74.125.226.18]

Trace complete.
```
