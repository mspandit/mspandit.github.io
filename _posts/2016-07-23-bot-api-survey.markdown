---
layout: post
title: "A Survey of Bot APIs"
excerpt: "A survey of Bot APIs and potential business models around them."
date:   2016-07-23 13:14:00
---

Several [recent articles][twitter-now-interactive] have promoted
conversational, text-based UIs as a forthcoming innovation. These UIs promise
to provide a natural, comfortable way to access information and services in the
enterprise and at home, integrating as necessary with voice interfaces.

Slack, Facebook, and Microsoft have opened up APIs in the hopes that developers
will add value to their respective messaging platforms.

# Slack API

The [Slack API][slack-api] lets you build [bot users][bot-users] that "enable
teams to conversationally interact with external services or your custom
code..." The bot user can

* be invited to participate in channels,
* monitor and participate in conversations with other users in channels 

[Botkit][botkit] from [Howdy.ai][howdy] is a recommended (open-source) platform
for building bot-users. It uses simple [keyword
pattern-matching][botkit-matching] to trigger responses.

# Facebook Messenger Platform 

The [Facebook Messenger Platform][facebook-platform] lets you build bots that
interact with users across "all platforms where Messenger exists."  Facebook
seems to recognize that Messenger bots will be marketing tools, and specifically
mentions support for brand and calls to action.

Furthermore, 

> The wit.ai Bot Engine effectively turns natural language into structured data 
> as a simple way to manage context and drive conversations based on your 
> business or app's goals.

As mentioned in a [prior post][prior-post], wit.ai lets a developer classify
natural language statements into a set of known intents. For an e-commerce site
trying to market using Facebook Messenger Platform, "intents" may be things like

* Ask if an item is in inventory
* Inquire about the price of an item
* Purchase an item listed in inventory
* Return an item

By allowing numerous natural ways of doing the above, by enabling customization
to a particular e-commerce site's inventory, and by providing a dashboard for
continuous improvement of the bot, Facebook hopes Messenger will become a
channel for marketing and e-commerce.

# Microsoft Skype Bots

The [Microsoft Bot Framework][microsoft-bot-framework] lets you "build and
connect intelligent bots to interact with your users naturally wherever they
are". Bots are built on top of an open-source [Bot Builder
SDK][bot-builder-sdk].

While Facebook Messenger Platform uses wit.ai to classify natural language
statements into known intents, the Microsoft Bot Framework uses the 
[Language Understanding Intelligent Service][luis] for the same purpose.

# Google

Google has announced an intelligent bot running inside its new messaging app,
[Allo][allo-bot]. However, this seems to be a closed bot, providing information
from the knowledge graph Google has already built.

# Business Models

The business model considered in the previous [post][prior-post] seems to
remain valid: Organizations that are already using one of the above messaging
platforms might be willing to pay for a bot that provides information and
services highly relevant to the enterprise---information and services that
would otherwise require costly human mediation or time-consuming search. One
example is [Wade & Wendy](http://wadeandwendy.ai/), a conversational recruiting
bot. NextIT has been in this space for some time, and
[butter.ai](http://butter.ai/) is providing enterprise file search through a
conversational interface. Competitive advantage in such a model will arise from

* selling capabilities beyond those of the IT departments of organizations, 
* speed and efficiency (cost) of implementation, 
* levels of automation, eliminating human labor,
* customization to the specific needs of the organization.

This model would also apply to companies that provide a conversational UI to
existing complex applications. For example, [sudo.ai](https://www.sudo.ai/) and
[Birdly](https://salesforce.getbirdly.com/), which provide a conversational UI
to Salesforce.com.

Facebook seems to be enabling brand engagement via the Messenger Platform, and
the business model here is obviously very marketing oriented. Marketing and IT
departments at large companies are likely to project their brands via such a 
platform, but there will be opportunities for agencies that can build engaging
chatbots---much like the opportunities for agencies that can build engaging
web sites and mobile applications. Competitive advantage in such a model will
arise from

* selling capabilities beyond those of the IT departments of organizations, 
* quantifiable engagement and sales closure
* creativity of brand expression

There may be a horizontal technology (for example intent classification from
natural language inputs) that becomes competitive to wit.ai and LUIS. However,
these are currently free services---their cost is borne by Facebook and
Microsoft (respectively) in the interests of promoting adoption of their social
media and cloud (respectively) platforms. It will be difficult to monetize a
horizontal technology. However, a company that builds one could hope to be
acquired by someone whose platform it helps.

[allo-bot]: http://www.theverge.com/2016/5/18/11699122/google-allo-messaging-app-announced-io-2016
[bot-builder-sdk]: https://github.com/Microsoft/BotBuilder
[bot-users]: https://api.slack.com/bot-users
[botkit]: https://howdy.ai/botkit/
[botkit-matching]: https://github.com/howdyai/botkit/blob/master/readme.md#matching-patterns-and-keywords-with-hears
[facebook-platform]: https://developers.facebook.com/blog/post/2016/04/12/bots-for-messenger/
[howdy]: https://howdy.ai/
[luis]: https://www.luis.ai/
[microsoft-bot-framework]: https://developer.microsoft.com/en-us/skype/bots
[prior-post]: http://blog.now-interactive.net/2016/07/09/facebook-m-wit-ai.html
[slack-api]: https://api.slack.com/
[twitter-now-interactive]: https://twitter.com/search?q=from%3Anwntrctv%20since%3A2016-01-31%20until%3A2016-07-23&src=typd&lang=en
