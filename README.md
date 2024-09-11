# Clara S. Traversal's Classroom
**This is supposed to be a black box challenge no source code review is necessary.**

**If you have any questions or want to get acces to hints you can join this server : https://discord.gg/G5sHRuWJ**

The Clara S. Traversal's Classroom web security challenge is a challenge where you'll need to exploit a couple of web vulnerabilities in order to make Vincent's final grade over 90%.

- Objective : Gain access to the class and find a way to change the user Vincent's final grade to be over 90%

- Requirements : Python installed nothing else.

- Additional info: The teacher denies access to users every minute. Also I recommend not logging in to the teacher's account and logging out it will cause problems with the teacher.py script and is not needed for the challenge.

Warning: This is an intentionally vulnerable website. This code contains an RCE so make sure the website is not publicly accessible.

### Startup 

```
git clone https://github.com/vin-hacks/ClaraClassroom
cd ClaraClassroom
python3 server.py
```

In another shell
```
cd ClaraClassroom
python3 teacher.py
```

Then you should be able to access http://localhost:8081/ in your browser and begin hacking!

Note that this challenge was made so that no code review or enumeration is necessary.

Hints will be put on here soon and 
