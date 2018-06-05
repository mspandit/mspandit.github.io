---
layout: post
title: "What Would Google Bot?"
summary: "Predictions about Google's chatbot and the business model that might support it."
date:   2016-07-25 09:06:00
---

[Microsoft](https://developer.microsoft.com/en-us/skype/bots),
[Facebook](https://developers.facebook.com/blog/post/2016/04/12/bots-for-messeng
 er/), and [Slack](https://api.slack.com/) have introduced bot APIs. Ray
Kurzweil has
[announced](http://sdtimes.com/author-ray-kurzweil-google-team-create-human-like
-chatbot-danielle/) that Google will also introduce a bot later this year. This 
made me wonder what features a fully-functional Google bot would possess, and
how it might support Google's business model.

# Summary of Predictions

* Google search is presently characterized by two types of responses to keyword queries: ranked web pages and advertisements. Search will expand to include natural language dialogue responses to natural language queries. (There is not a black-and-white distinction between natural language queries and keyword queries. The responses could be a similar blend.) (See [Google Assistant](https://techcrunch.com/2016/05/18/google-unveils-google-assistant-a-big-upgrade-to-google-now/).)

* Google search presently exploits context that is implicit and not volunteered by the user, at least not at the time of query. This has the benefit of "magically" relevant responses, but also has a "creep factor." Natural language dialogue will consume more of a user's time, but have the benefit of explicit, immediate, and voluntary context. This in turn will be rewarded with precise, relevant results.

* Google search dialogue could differ dramatically from human-to-human dialogue if it presents multiple responses, allows the user to choose the course of the dialogue, and improves over time based on these choices.

* Google will continue to promote schemas and standards for authors to explicitly structure content for easy, relevant access. Google will continue to pursue natural language processing algorithms to automatically structure text that remains unstructured.

* The Google search page will continue to use a global knowledge graph for dialogue, but site search will use a knowledge graph that is "local" to a web site. **It will therefore be possible, in a few lines of Javascript code, to embed a site-search-chatbot in your site that is an expert on your content.**

* In the same way that the look and feel of site search can be [customized](https://support.google.com/customsearch/answer/1721914?hl=en&ref_topic=1723767), it will be possible to customize the _personality_ of the dialogue aspects of site search.

* Presently, ranked web page results sometimes overlap with advertisements (sponsored links). Similarly, natural language dialogue responses may direct users to web site destinations that are also advertised. Such directions will have a higher closure rate (revenue per impression) because of explicit, immediate, and voluntary context.

* Google presently allows advertisers to associate keywords with advertisements, and encourages expansions to ensure that all relevant keywords are included. Google will allow advertisers to associate some form of dialogue structure (for example, _intents_) and encourage expansions to ensure that all relevant ones are included. Advertisers will tolerate the additional labor because of the increased revenue per impression.

# Supporting Considerations

## The Importance of Context

> Google’s [mission](https://www.google.com/about/company/) is to organize the
> world’s information and make it universally accessible and useful.

Increasing amounts of "the world's information" are certainly becoming
available online. However, Google recognized early on that accessibility,
usefulness, and even organization were highly dependent on the time, place, and
other aspects of the
[_context_](https://en.wikipedia.org/wiki/Contextual_searching) in which it was
being accessed. By accounting for the time and place of your search, the recent
history of your searches and even _searches by all other users,_ Google is able
to better filter and sort results, frequently ranking the most relevant result
at the top. This is by no means an easy task, and in the beginning it seemed
magical. It is now very much expected by users, who can become frustrated when
the results fail to satisfy their immediate demands. However, use of context
can also trigger the "creep factor"---that unpleasant but common suspicion that
"Google knows everything about you."

Accessibility of information was also frequently degraded when the answer to a
specific question was buried in the text of a web page. Google has made strides
on this front by returning "snippets" at the top of the results page---snippets
that could have been extracted automatically by Google software or
[defined](https://developers.google.com/search/docs/guides/intro-structured-data
 ) by web page authors themselves. Of course, snippets are only helpful if they
correctly address the specifics of a search query and the context in which it
was made.

[Custom search](https://cse.google.com/cse/tools/create_onthefly) could be
thought of as a specific kind of context that filters search results to a 
single web site.

## Dialogue for Context

One way to acquire context is through _question-and-answer dialogue._ This is a
very natural mode by which humans answer questions, and avoids the creep
factor---you, the search user, do not feel the other party "knows everything
about you" because you have supplied information voluntarily and recently
during the course of the dialogue.

A very rudimentary form of dialogue was introduced by Google with the "Did you
mean?" feature. If you use an unusual spelling in your query, you are presented
results as usual, but at the top of the page is a link titled "Did you mean
[expected spelling]?" That link lets you re-do the search with the expected
spelling, in a single click. 

More recently, Google introduced [_anaphora resolution_](http://nlp.stanford.edu/courses/cs224n/2003/fp/iqsayed/project_repo
 rt.pdf) in its voice search. You can (verbally) ask the search engine, "Who is
the President of the United States?" and get the correct result, "Barack
Obama." You can then ask, "How old is he?" Google will correctly interpret "he"
to mean "Barack Obama" and return Obama's age.

Natural language dialogue does consume time compared to fast keyword search. It
will never _replace_ keyword search, but it does provide a useful and natural
extension. This is especially true as Google asserts Android's dominance on
smartphones.
[Forbes](http://www.forbes.com/sites/neilhowe/2015/07/15/why-millennials-are-tex
ting-more-and-talking-less/#79287be45576) recently published the results of a
Gallup Poll: "Text messages now outrank phone calls as the dominant method of
communication among Millennials." It is reasonable to conclude, therefore, that
chatbot dialogue is a natural next step in Google's pursuit of its stated
mission. (See also: [Apple Lays the Groundwork to Kill Online Advertising](https://techcrunch.com/2016/07/24/apple-lays-the-groundwork-to-kill-online-advertising/?ncid=rss&cps=gravity_1730_6590232193807806974))

## Show Me the Money

Not everything Google (or Alphabet) does has a direct impact on the top line,
but search does:

* Advertisers pay Google to present advertisements along with "organic" search
  results when certain keywords are queried

* The more an advertiser bids on a keyword, the more likely the advertisement
  will be presented when that keyword is used in a query.

* An advertisement targeted for one or more keywords may or may not be
  presented (an event called an _impression_) when those keywords are queried.
  The advertiser is only charged when the user clicks on an advertisement (pay
  per click or PPC).

* The advertiser can easily track when the user clicks on an advertisement, and
  even when that _clickthrough_ results in a sale, download, or other action

* Google provides tools for advertisers to construct advertisements, target
  keywords, count impressions, and track clickthroughs.

* Web site owners can earn money from Google by become advertising
  _affiliates._ They reserve space on web pages for advertisements to appear.
  Google runs an automated competition for that space, choosing a relevant
  advertisement based on the content of the page, the advertiser's bids, and
  the visitor's context. The user's visit to the page becomes a kind of
  _implicit query_ whose result is the advertisement that appears in the
  reserved space.

Advertisements could be thought of as a class of search results whose
"relevance" is determined (partially) by money. Sometimes the results overlap,
and the top advertisement links to the very same page as the top "organic"
search result. However, the ideal for all parties is when the advertised
product or service truly meets the need implicit (or explicit) in the user's
query.

What does this mean if keyword search is extended to chatbot-style dialogue,
or if chatbot-style dialogue becomes the dominant mode of search?

## Search as Chat

We can certainly imagine queries being processed in two ways simultaneously:

* as keyword searches, just as they currently are, with results being web
  pages. Of course, multiple web pages may be relevant to a keyword query, and
  they are ranked according to Google's proprietary algorithm. When a user
  clicks on one of the returned links, this choice is used to improve the
  algorithm's ranking in the future.

* as natural language chat statements, with the result being the answer to a
  question, the result of executing a command, or a clarifying question.

The fact is, in response to a natural language chat statement, a _multiplicity_
of responses could be considered. Differing assertions might be present in the
Google knowledge graph and in various web sites. These responses _might_ be
ranked the way web pages are, and the top-ranked response might be chosen for
presentation. This is analogous to what happens in a human dialogue. However,
the search page affords an opportunity to do something different: unlike human
chat, Google chat could return _multiple_ ranked responses. The user could
choose from one, thereby taking the dialogue in a particular direction. This
choice could be used to alter the search system's ranking of responses in the
future. (See [Choose Your Own
Adventure](https://en.wikipedia.org/wiki/Choose_Your_Own_Adventure).)

The number of natural language responses (vs. the number of organic search
results) presented could be higher if the query consisted of a parsable natural
language question or statement.

To the extent a knowledge graph can be extracted from text on a web page,
Google seems to do so automatically, using techniques like [information
extraction](https://github.com/dbpedia/fact-extractor) but a special importance
should be given to knowledge explicitly structured by web page authors. 

When a multiplicity of answers is given to a natural language query, it will be
important to communicate their sources. Popular answer sources could be
considered more trustworthy than unpopular sources.

The chatbot equivalent of site search would converse based on the knowledge
graph in a single web site. The results would provide the "perspective" of that
source on a topic of conversation.

## "Chatvertising"

When a query is processed, a (potentially large) set of advertisements
"compete" to be among the few presented on the results page. The algorithm that
selects an advertisement is proprietary, but considering that advertisers
associate keywords with their advertisements, we can safely assume that if an
advertisement is associated with a query keyword, it is included in the initial
set. (After that, it may get filtered out for various other reasons.)

The risk here is that the search user may, for various reasons, use a keyword
that the advertiser did not anticipate. The user misses seeing a relevant
advertisement, and the advertiser misses a potentially lucrative impression.

Google mitigates this risk on the advertisers' side by suggesting _expansions_
of the keyword list associated with an advertisement. There appears to be some
expansion happening on the user side as well, because the web pages in search
results sometimes contain only synonyms, and not the keywords themselves.

The point is that the match takes place between a _derivative_ of the query
and a derivative of the advertisement. These derivatives may be specified by
the author (as in advertising keyword expansions or structured snippets) or
they may be extracted automatically by Google algorithms (as in query keyword
expansions).

We can certainly imagine treating statements in a dialogue as queries for the
purpose of selecting advertisements, using the same algorithms as for keyword
queries. However, irrelevant advertisements inevitably appear, at least partly
because the context used to select advertisements is not obvious, immediate,
nor in the user's control.

It is more interesting to consider that a properly-structured dialogue---which
is explit, immediate, and within the user's control---could lead to a product
or service that perfectly meets the user's needs. The increased likelihood that
an "impression" leads to satisfactory resolution would compensate for
significant incremental effort on the part of the user (in engaging in
dialogue), the advertiser (in structuring dialogues, analogous to associating
keywords and advertisements to products and services) and Google (in
automatically generating derivatives to close the gap).

