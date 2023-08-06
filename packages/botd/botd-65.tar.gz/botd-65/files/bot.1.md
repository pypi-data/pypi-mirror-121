% BOT(1) BOTD version 65
% Bart Thate 
% Oct 2021

# NAME

**bot** - IRC bot

# SYNOPSIS

 bot \<cmd\> \[key=value\] \[key==value\] 
    
# DESCRIPTION

**bot** is an attempt to achieve OS level integration of bot technology 
directly into the operating system. A solid, non hackable bot, that stores
it's data as JSON files on disk, every object is timestamped, readonly of
which the latest is served to the user layer. This bot is intended to be
programmable in a static, only code, no popen, no importing from directories,
way that makes it suitable for embedding.

# IRC

IRC configuration is done with the use of the cfg command.

> $ bot cfg server=\<server\> channel=\<channel\> nick=\<nick\> 

default channel/server is #botd on localhost.

# SASL

some irc channels require SASL authorisation (freenode,libera,etc.) and
a nickserv user and password needs to be formed into a password. You can use
the pwd command for this.

> $ bot pwd \<nickservnick\> \<nickservpass\>

after creating you sasl password add it to you configuration.

> $ bot cfg password=\<outputfrompwd\>

# USERS

if you want to restrict access to the bot (default is disabled), enable
users in the configuration and add userhosts of users to the database.

> $ bot cfg users=True

> $ bot met \<userhost\>

# RSS

if you want rss feeds in your channel install feedparser.

> $ sudo apt install python3-feedparser

add a url to the bot and the feed fetcher will poll it every 5 minutes.

> $ bot rss <url>

# FILES

| bin/bot
| man/man1/bot.1.gz

# COPYRIGHT

**bot** is placed in the Public Domain, no Copyright, no LICENSE.

# SEE ALSO

| https://pypi.org/project/botd
