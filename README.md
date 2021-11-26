# Wikipedia Quiz Bot
This is a source code of a [Wikipedia Quiz Bot](TODO: add a URL here).

## Description
This bot automatically generates a fill-in-the-blank quiz from a randomly selected Wikipedia page, and posts it on Twitter once a day.

For instance, the Wikipedia page about Twitter starts the description like this:

> Twitter (initially called Twttr) is an American microblogging and social networking service on which users post and interact with messages known as "tweets".

The bot converts this to a question in this way:

> ( ) is an American microblogging and social networking service on which users post and interact with messages known as "tweets".

Then the bot posts this quiz with a poll containing four options. 

After a day, it stops the polling and posts the answer (in this case, "Twitter") as a reply to the question tweet.

