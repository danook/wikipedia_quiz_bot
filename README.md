# Wikipedia Quiz Bot
This is a source code of a [Wikipedia Quiz Bot](https://twitter.com/wikiqbot).

## Description
This bot automatically generates a fill-in-the-blank quiz from a randomly selected Wikipedia page and posts it on Twitter once a day.

For instance, the Wikipedia page about Twitter starts the description like this:

> Twitter (initially called Twttr) is an American microblogging and social networking service on which users post and interact with messages known as "tweets".

The bot converts this to a question in this way:

> ( ) is an American microblogging and social networking service on which users post and interact with messages known as "tweets".

Then the bot posts this quiz with a poll containing four options. Options are randomly picked up from the pages mutually linked from the page.

After a day, it stops the polling and posts the answer (in this case, "Twitter") as a reply to the question tweet.

> Answer: Twitter

## Languages & Technologies
* Python3
* [Tweepy](https://www.tweepy.org/) (Python library for using Twitter API)
* [Mediawiki API](https://www.mediawiki.org/wiki/API:Main_page) (API for Wikipedia)
* [Heroku](https://www.heroku.com/)
* [Google Drive API](https://developers.google.com/drive/api/)
