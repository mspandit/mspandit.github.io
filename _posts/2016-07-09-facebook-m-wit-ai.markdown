---
layout: post
title: "Facebook M and Wit.ai"
summary: "Business considerations of Facebook M, its acquisition of Wit.ai and some of Wit.ai's competitors."
date:   2016-07-09 17:48:00
---

Since their inception, intelligent agents like Siri, Google Now, and Cortana
have reverted to internet searches when they could not understand the meaning
of a user request. A few years ago, I envisioned an intelligent agent that
would seamlessly route the query to a human being if it could not understand it
or fulfill it. Backed by a cadre of humans, such an agent could deliver a leap
in service performance.

A colleague, formerly of [Tellme Networks][tellme], which was acquired by
Microsoft, assured me that such a model could not possibly work, because of the
cost of employing the human beings. I pointed out that those costs would
decline as fast as the intelligent agent's performance (on its own) improved,
and that ongoing improvement of its models and algorithms could be built in to
the overall operation, but he insisted that this had all been analyzed
previously and deemed infeasible.

![Facebook M][facebook-m]

It turns out that I was right. The _Wired_ [article][article1] entitled
_Facebook's Human-Powered Assistant May Just Supercharge AI_ describes just
such an agent. A number of things could have rendered this feasible for
Facebook:

* Facebook started with sufficient investment to make the venture profitable in
  the long run.

* Facebook M is a text messaging agent, while my colleague and I were
  considering speech recognition systems, that are vulnerable to unintelligible
  audio.
  
* Facebook simply hasn't realized yet that it is infeasible!

The article was doubly interesting because it mentioned that
[Wit.ai](https://wit.ai/) was acquired to help build Facebook M. Wit.ai
provides an attractive platform for crowdsourced _intent classification._ In
other words, a developer can specify a limited set of "intents" to be
recognized from various natural language statements. The system will generalize
from this. When given a new natural language statement, it will generate a
probability distribution across the intents. The system is not perfect, but it
provides a dashboard for the developer to correct its mistakes. It will
approach perfection over time. If a sufficient number and diversity of
developers participated, then the system could recognize a corresponding number
and diversity of intents, and become generally very useful.

It is not clear why Wit.ai was ultimately sold to Facebook. Shortly before
their acquisition, they open-sourced their [Duckling parser][duckling]. I do
know that one of its competitors, [Ask Ziggy][askziggy] apparently [ran out of
money][askziggy-closed]. Another competitor, [Speaktoit][speaktoit] recently
re-branded itself as mobile application [Assistant.ai](http://assistant.ai),
backed by [api.ai](http://api.ai).

Wit.ai currently offers its service for [free][wit-free], which is likely to
make things difficult for [api.ai][speaktoit-cost]. In any case, the platform
business is bound to be difficult unless there is an end-to-end application
that is sufficiently compelling and also promotes competition.

[article1]: http://www.wired.com/2015/08/how-facebook-m-works/
[askziggy]: http://thenextweb.com/dd/2013/03/11/ask-ziggys-new-api-allows-any-app-to-have-its-own-built-in-siri/
[speaktoit]: https://en.wikipedia.org/wiki/Speaktoit
[tellme]: https://en.wikipedia.org/wiki/Tellme_Networks 
[facebook-m]: http://www.wired.com/wp-content/uploads/2015/09/Facebook-M-logo-1200x630.jpg
[duckling]: https://duckling.wit.ai/
[askziggy-closed]: https://www.crunchbase.com/organization/ask-ziggy#/entity
[wit-free]: https://wit.ai/faq
[speaktoit-cost]: https://api.ai/pricing/