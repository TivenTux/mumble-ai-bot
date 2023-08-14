## Mumble AI Bot
Mumble bot with speech synthesizer that uses openAI or self hosted LLM


If you have issues with the speech synthesizer voice, please check your conf files under /etc/speech-dispatcher
Some discord functions are planned for the future so please create a discord app, and get the bot's token here: https://discord.com/developers/applications 

Set ENV variables:  

**openaikey** - your chatGPT api(https://platform.openai.com/account/api-keys) <br>
**discordtoken** - your discord bot token(https://discord.com/developers/applications) <br> 
**mumble_host** - Mumble server host address <br>
**portnumber** - Mumble server port number <br> 
**bot_nickname** - Set the bot's name.<br>
**mumble_passwd** - Mumble server password. Do not set if none.<br>
**bot_keyword** - Keyword which the bot will respond to. Usually same as with bot's name.<br>

_If the LLM is self hosted there might be a small performance drop on GGML (CPU) models with passthrough_username enabled. No performance drop on openAI._


### pip packages

```
pymumble, discord, openai

```

### os deps

```
espeak, ffmpeg

```
