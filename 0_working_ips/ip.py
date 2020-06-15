"""
-------------------------------
    I N T R O D U C T I O N
-------------------------------
Author:         Fuad Al Abir
Date:           December 6, 2018
File name:      ip.py
Objective:      is to find the working ips in range and write them in a text file 'working_ip.txt'
Algorithms:     Brute force
Problem Source: Wish to find ip servers of Ahsan.wifi

-------------------------------------
    I M P O R T E D   M O D U L E
-------------------------------------
Header: webbrowser
Reason: to open a url in browser
Header: requests
Reason: to process url's status

---------------------------------
    S A M P L E   O U T P U T
---------------------------------
for start = 0
    end = 1
    working_ip.txt:
        http://1.0.0.1
        http://1.1.1.1
"""

import webbrowser
import requests

start = 0   # Starting combination with start.start.start.start
i = start
j = start
k = start
l = start
end = 1     # Ending with end.end.end.end

f = open("working_ip.txt", "w")
while i <= end:
    while j <= end:
        while k <= end:
            while l <= end:
                url = 'http://' + str(i) + '.' + str(j) + '.' + str(k) + '.' + str(l)
                print url
                
                try:
                    r = requests.get(url,timeout=3)
                    #print r.raise_for_status()
                    print r.status_code
                    if r.status_code == 200:
                        # to open in browser
                        # webbrowser.open(url)
                        # working url is written in te text file
                        f.write(url + '\n')
                except requests.exceptions.HTTPError as errh:
                    #print ("Http Error:",errh)
                    print 'ERROR 0'
                except requests.exceptions.ConnectionError as errc:
                    #print ("Error Connecting:",errc)
                    print 'ERROR 1'
                except requests.exceptions.Timeout as errt:
                    #print ("Timeout Error:",errt)
                    print 'ERROR 2'
                except requests.exceptions.RequestException as err:
                    #print ("OOps: Something Else",err)
                    print 'ERROR 3'
                l += 1
            l = start
            k += 1
        k = start
        j += 1
    j = start
    i += 1
f.close()
