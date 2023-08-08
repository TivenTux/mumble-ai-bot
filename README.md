# Phoenix - Mumble AI Bot
Mumble bot with speech synthesizer that uses openAI or self hosted LLM


If you have issues with the speech synthesizer voice, please check your conf files under /etc/speech-dispatcher
Some discord functions are planned for the future so please create a discord app, and get the bot's token here: https://discord.com/developers/applications It's needed for configuration.

Get chatGPT api key here: https://platform.openai.com/account/api-keys

Edit conf settings from line 12 to 40. If you use openAI's chatgpt, you do not need to edit anything on locally hosted LLM settings.

```
If the LLM is self hosted there is small performance drop on GGML (CPU) models with passthrough_username enabled. No performance drop on openAI.
```

### pip packages

```
pymumble, discord, openai

```

### os deps

```
espeak, ffmpeg

```
