---
title: Why do we keep giving LLMs rules we know they can't follow?
date: 2026-03-22
published: true
---

We've all seen the news reports nowadays. [The Meta AI exec who almost let an AI assistant delete
their entire email inbox][1]. [The agent that wiped out someone's hard drive][2]. [The LLM that
ignored "no" when asking whether to implement a plan][3]. You've probably had it happen to you
directly. Especially when you include the more common case of LLMs and agents ignoring general
instructions that are provided to them. Agent prompts regularly include things like "RETURN ONLY
JSON" nowadays, and yet you _still_ have to verify that the response you got is actually that.

I got me to thinking: **why do we keep giving LLMs rules we know they can't follow?**

### What do I mean by this?

It's widely accepted at this point that LLMs do not understand language. They're effectively word
predictors - they predict the probability of a word given the surrounding context. This means that
they don't understand the rules they're provided. Those rules just add additional weight to certain
probabilities, making them more likely outcomes.

This means that the LLM is incapable of 100% following any instruction or rule it's given. Those
things influence the probabilities in the network to make an outcome that _does_ follow the
instructions extremely likely. But at the end of the day, you as the user don't have final say. If,
somehow, the word predictions lead to a state where the LLM thinks it should do something
catastrophic, you don't really have a way to stop it from doing that.

This of course has led to the rise of sandboxing in AI usage, where you run your agents on a
separate machine or in a container. I personally don't believe this to be a sufficient level of
security. Within whatever sandbox you're using, the LLM is still king - it can effectively do
whatever it wants. The sandbox just allows you to create a situation where you can recover from
that.

### Rules don't make sense in this context

At the end of the day, in a context where the LLM/agent doesn't actually _understand_ the language
behind the rules, I don't think providing rules makes sense. Even for something like Claude's
defensive modes vs the `--dangerously-skip-permissions` flag, you're effectively always in
"dangerously skip permissions" mode. There are rules and prompts attempting to stop it from running
whatever commands without your permission; but as we've seen, those permissions can be ignored.

As a software developer, it feels nuts to me that we allow AI agents/LLMs in the wild with this
current permissions structure. Computer science is almost exclusively concerned with worst case
performance and outcomes, and yet we let Claude masquerade like it has safety checks when it cannot
stop the agent from doing whatever it wants.

### We need an indirection layer

I think the long term solution for LLM permissions is going to be some kind of hardware-level I/O
indirection layer between the LLM and the disk/network. You cannot have a solution that relies on
the LLM choosing to call your framework or exist within the sandbox because it can always break
those rules. Therefore, you need something that sits outside the agent framework and intercepts
commands at the layer where they can do damage: when they're written to I/O, whether that's the disk
or network.

I don't know what this looks like in practice - this level of hardware/driver engineering is beyond
my level of expertise. But I think until something like this exists, there's no way to ever use LLMs
or agents in real-world critical situations. At the end of the day, you can't stop it from doing
whatever it wants. We need to come up with an answer that puts the user back in charge.

[1]:
  https://www.fastcompany.com/91497841/meta-superintelligence-lab-ai-safety-alignment-director-lost-control-of-agent-deleted-her-emails
[2]: https://www.newsweek.com/google-ai-accidentally-deletes-hard-drive-data-antigravity-11169711
[3]: https://gist.github.com/bretonium/291f4388e2de89a43b25c135b44e41f0
