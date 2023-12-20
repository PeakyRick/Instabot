This repo contains a module that logs into Instagram accounts and automatically likes
posts in specified hashtags as well as posts in the discovery page. This module is 
created in Oct 2022 and uses the package Selenium. Minor bugs are expected due to 
Instagram and/or Selenium updates.

Along with the "insta_auto_likes" module, a separated "insta_credentials" python file
needs to be created, which contains login info of the users. In the format of :<br>
  user1_cred = {"USERNAME": "some_user_name", "PASSWORD": "your_password"}
