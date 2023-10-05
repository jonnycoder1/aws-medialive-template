# Purpose
Do you need to livestream simultaneously to YouTube and Facebook?

You can use AWS Elemental MediaLive to create an RTMP endpoint and have it forward your livestream to your 
Facebook and YouTube streams at the same time.

This repo provides a proof of concept for creating a livestream on AWS MediaLive with destinations 
for YouTube and Facebook.

Alternatively, you could use a CloudFormation stack as documented:
https://aws.amazon.com/blogs/publicsector/live-streaming-facebook-youtube-aws-elemental-medialive/


# Usage
Requirements: Python 3.10

Step 1: Edit aws_streaming.py and update the variables in __init__ method.

Step 2: Run the below commands to install dependencies and run the python script.
```
virtualenv venv
source venv/bin/activate
pip install -r requirements.txt
venv/bin/python aws_streaming.py
```
