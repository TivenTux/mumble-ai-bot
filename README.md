## Mumble AI Bot
Mumble bot with speech synthesizer that uses openAI or self hosted LLM

Docker image is available for download on
**[Dockerhub](https://hub.docker.com/repository/docker/tiventux/mumble-ai-bot)**.

## Environmental Variables

**openaikey** - your chatGPT api(https://platform.openai.com/account/api-keys) <br>
**mumble_host** - Mumble server host address <br>
**portnumber** - Mumble server port number <br> 
**bot_nickname** - Set the bot's name.<br>
**mumble_passwd** - Mumble server password. Do not set if none.<br>
**bot_keyword** - Keyword which the bot will respond to. Usually same as with bot's name.<br>
**default_channel_name** - After connecting, bot will join this channel.<br>
**words_per_min** - Speech synth speed, words per minute. Default 185<br>
**word_gap_ms** - Speech synth gap between words. Default 5ms<br>

You can specify these environment variables when starting the container using the `-e` command-line option as documented
[here](https://docs.docker.com/engine/reference/run/#env-environment-variables):
```bash
docker run -e "openaikey=yy"
```

## Running the pre-built docker image

If you just want to run the pre-built docker image, you can run
```bash
docker run --name=mumble-ai-bot -d -e "openaikey=yyy" -e "mumble_host=yyy" -e "portnumber=yyy" -e "bot_nickname=yyy" -e "bot_keyword=yyy" tiventux/mumble-ai-bot:latest

```


## Building the container

After having cloned this repository, you can run
```bash
docker build -t mumble-ai-bot .
```

## Running the container

```bash
docker run -d -e "openaikey=yyy" -e "mumble_host=yyy" -e "portnumber=yyy" -e "bot_nickname=yyy" -e "bot_keyword=yyy" mumble-ai-bot

```
