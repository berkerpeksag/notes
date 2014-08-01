## Root Privileges and Automated Tasks

As a sysadmin, you will likely find yourself in a situation,
where it would be useful to delegate root level privileges to
non-root users. There could be any number of reasons to do this,
lets say that you are working closely with a group of developers,
and they need access to restart httpd each time a code deployment
is pushed out.

Giving the group root access would be overkill since all they
need to do it restart httpd. Luckily this is a well understood
requirement and the sudo command was built with this in mind. The
sudo command allows a permitted user, or group of users, to execute
superuser command as defined by a configuration file. What is so
great about sudo, is that you can define very narrow root access
with the added bonus that there is built in logging.

```sh
# helpdesk ticket #1234
# aid software deployment for dev group
deployment        ALL=(root) NOPASSWD: /etc/init.d/httpd start
deployment        ALL=(root) NOPASSWD: /etc/init.d/httpd stop
deployment        ALL=(root) NOPASSWD: /etc/init.d/httpd restart
```

Depending on your distro, you might have a directory called
`/etc/sudoers.d/` where you can package up your custom `sudoers`
line into nice little files. This can be handy if you have a large
`sudoers` file and want to break it apart into smaller manageable
chunks.

Reference: http://sysadmincasts.com/episodes/23-root-privileges-and-automated-tasks
