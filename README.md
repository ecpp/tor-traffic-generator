# What is this?
- This python script creates traffic with tor ip addresses. I use it with random-chain proxychains so every traffic looks like it comes from different IP.
- It has also ability to bruteforce but since it uses tor it will be so slow, I do not recommend it.

# Why I created this?
It is for my graduation project. To create unique traffics to my honeypots.

# Is it working?
Yes, but for now only some protocols are working. More yet to be implemented.

# Prerequisites
- You must have TOR and proxychains configured.
- I recommend to use proxychains with random-chain.

# Usage
- python3 tor-traffic-generator.py
- Select desired protocol to create traffic.
- Enter IP, port, username (if ssh or ftp), password list (if ssh or ftp)

# Educational Purposes Only
