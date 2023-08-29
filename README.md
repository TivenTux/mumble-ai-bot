## Mumble AI Bot
Mumble bot with speech synthesizer that uses openAI or self hosted LLM

Docker image is available for download on
**[Dockerhub](https://hub.docker.com/repository/docker/tiventux/mumble-ai-bot)**.

## Environmental Variables

| Environment Variable             | Description                                                                         |
|----------------------------------|-------------------------------------------------------------------------------------|
| `openaikey`                      | Your openAI api key (https://platform.openai.com/account/api-keys)                  |
| `mumble_host`                    | Mumble server host address.                                                         |
| `portnumber`                     | Mumble server port number.                                                          |
| `bot_nickname`                   | Set the bot's name.                                                                 |
| `mumble_passwd`                  | Mumble server password. Do not set if none.                                         |
| `bot_keyword`                    | Keyword which the bot will respond to. Usually same as with bot's name.             |
| `default_channel_name`           | If set, bot will join this channel after connecting.                                |
| `words_per_min`                  |  Speech synth speed, words per minute. Default `185`.                               |
| `word_gap_ms`                    | Speech synth gap between words. Default `5`ms.                                      |
| `mumble_use_cert`                | Option to use certificate. Set 1 to enable, 0 to disable. Default `disabled`.       

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
