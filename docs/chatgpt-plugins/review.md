## Plugin review process

We are in the early stages of building the plugin store, this page outlines the basic overview of how we are thinking about the plugin review process, and what the plugin review process will look like.

The plugin review process will change significantly over time. We are open to feedback about how to improve the process for those building plugins.

## What make a great plugin

The purpose of the review process is to ensure that plugins on ChatGPT are safe, provide useful functionality, and provide a high-quality user experience. Long-term, we expect it to be routine to go through the review process as we formalize it.

In the immediate term, we expect that plugins which deliver new, magical experiences for users, which would not have been possible without the unique capabilities of large language models, will deliver the most value.

So far, some categories of plugins that have been the most magical are:

- Retrieval over user-specific or otherwise hard-to-search knowledge sources (searching over Slack, searching a user’s docs or another proprietary database).
- Plugins that synergize well with other plugins (asking the model to plan a weekend for you, and having the model blend usage of flight/hotel search with dinner reservation search).
- Plugins that give the model computational abilities (Wolfram, OpenAI Code Interpreter, etc).
- Plugins that introduce new ways of using ChatGPT, like games.
- Plugin states
- When developing a plugin, the plugin can be in one of several statuses, indicating where it is along the review process and who can use it. Right now, there are only a couple of plugin statuses. We expect this to change as the plugins system evolves.

| Status     | Description                                                                                               | Developer access | Users access |
|------------|-----------------------------------------------------------------------------------------------------------|------------------|--------------|
| Unverified | The default status that a plugin starts out in.                                                           | 15               | 0            |
| Approved   | OpenAI has reviewed the plugin, and has determined that the plugin is approved for use by a general audience of users. | Unlimited        | Unlimited    |
| Banned     | OpenAI has reviewed the plugin, and has determined that the plugin should be banned.                       | 0                | 0            |

Note that if you submit a plugin and it is rejected because it fails to meet the requirements, it would still be in the "Unverified" state.

## Types of users
Right now there are three categories of users that we talk about when it comes to plugins access.

| User type | Description |
| --- | --- |
| ChatGPT Plus users | ChatGPT Plus users who have been given access to plugins that have gone through our review process and have been approved for general use. |
| Plugin developers | ChatGPT Plus users who have been given the ability to develop, use, and test plugins that are in development. |
| Normal ChatGPT users | Right now, normal ChatGPT users without plug don’t have plugin access. |

## Plugin store

In order to have your plugin available in the plugin store, it needs to be reviewed by OpenAI. Before submitting your plugin for review, make sure your plugin fits the criteria below:

- Adheres to our content policy
- Complies with our brand guidelines
- Functions as described in your submission
- Provides informative error messages
- Features descriptive operation names
- Offers a simple and concise manifest file
- Uses correct grammar and ends the plugin description with punctuation
- States geographical or functional limitations clearly in the plugin description to avoid user confusion
- Does not use words like plugin, ChatGPT, or OpenAI in the plugin name or description
- Plugin enforces user confirmation before taking an action (see Zapier for an example of this)
- If the plugin takes actions in the world, it needs to use OAuth

If any one of these criteria are missing, we will reject the plugin and you can submit it again once it is updated.

## Submit a plugin for review

You can expect to hear back about a plugin you submit for review ~7 days after you submit the plugin.
We are currently reviewing new plugins on a rolling basis. You can submit a plugin for review using the plugin submission bot. To see the bot, you need to be signed in.

To view the status of your plugin submission, make sure you are logged in and select "Help" in the top right corner of this page. Under "Messages", you will be able to see your plugin submission. We will notify you as the status of your plugin changes during the review process.