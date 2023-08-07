import discord, time, os, random, requests, json
from discord.ext.commands import Bot
from discord.ext import commands
import asyncio, openai
from time import *
import re, sys
import urllib, datetime
import pymumble_py3
from pymumble_py3.constants import *
import subprocess as sp

############ conf ############
#use number 1 for openAI or 2 for custom api
aiselection = 1
#openAI settings
openaikey = '' #create api at https://platform.openai.com/account/api-keys

#discord bot token
token = '' #create bot and get the token number at https://discord.com/developers/applications

#locally hosted LLM settings - use this if you dont want to use openAI and host your LM elsewhere
aihost = '127.0.0.1:9500'
aiurl = f'http://{aihost}/api/v1/generate'

#mumble settings for bot
server = "127.0.0.1"
portnumber = 64738
nick = "Phoenix" #if you change this, remember to edit the prompt describing the AI assistant's name in msg process function.
passwd = ""
bot_keyword = 'PHOENIX' #needs to be in uppercase
bot_keyword2 = 'PHOENIX,' #needs to be in uppercase
mumble_use_cert = 0 #change to 1 if you want to use certificate. remember to generate it first
certfilemumble = './constants/public.pem'
keyfilemumble = './constants/private.pem'
mumble = pymumble_py3.Mumble(server, nick, port=portnumber, password=passwd, reconnect=True)
if mumble_use_cert == 1:
    mumble = pymumble_py3.Mumble(server, nick, port=portnumber, password=passwd, reconnect=True, certfile=certfilemumble, keyfile=keyfilemumble)




#init some stuff
intents = discord.Intents().all()
intents.members = True
client = discord.Client(prefix='', intents=intents)
aikeynumber = 0
dcerrors = 0
totalaierrors = 0
punishedusers = []
mumbleusercomment = ' '



#mumble users check, not used anymore
async def checkmumble():
    serverstatus = 'unknown'
    try:
        status = mumble.users.count()
        print('users:' + str(status) + '\n')
        if status > 0:
            serverstatus = 'ok'
    except Exception as e:
        print(e)
        serverstatus = 'dc'
    return serverstatus

def onmumbledisconnect():
    mumble.connect()
    print('connection dropped reconnecting..')
    #run_dc_handler = asyncio.run(handledc())
    return

def exit_program():
    global dcerrors
    dcerrors += 1
    print("Exiting the program...")
    quit()

#handle disconnects, not used anymore
async def handledc():
    mumble.connect()
    await asyncio.sleep(4)
    return

#process the message and prompt
async def msgprocess(text, usern):
    finprompt1 = "Below is a conversation between a user named " + usern + " and an AI assistant named Phoenix.\nPhoenix was made by Tiven and provides helpful answers.\n" + usern + ": "
    aifinal_question = finprompt1 + str(text) + "\nPhoenix:"
    try:
      if aiselection == 1:
          ai_response = await aiprocess1(aifinal_question, openaikey)
      else:
          ai_response = await aiprocess2(aifinal_question, str(text))
    except Exception as e:
        print(e)
    await speech_synthesize(ai_response)
    await msgsend(ai_response)
    return

#reply in mumble channel
async def msgsend(ai_response):
    msg = ai_response.encode('utf-8', 'ignore').decode('utf-8')
    mumblechan = mumble.channels[mumble.users.myself['channel_id']]
    mumblechan.send_text_message(msg)
    return

#clean up message, find author and forward
def onmumblemsg(text):
    print('received msg.. passing through')
    print(text)
    rmsg = text.message
    rmsg = rmsg[7:]
    try:
        usern = str(mumble.users[text.actor]['name'])
    except Exception as e:
        print(e)
        usern = 'nan'
    rmsg2 = text.message.upper()

    if text.actor == 0 or text.session:
    # Some server will send a welcome message to the bot once connected.
    # It doesn't have a valid "actor". Simply ignore it here.
        print('ignoring pm: ' + rmsg2)
        return
    if rmsg2.startswith(bot_keyword) or rmsg2.startswith(bot_keyword2):
        start_this_now = asyncio.run(msgprocess(rmsg, usern))
    else:
        print('ignoring pm: ' + rmsg2)
    return

#when discord bot is ready, connect to mumble
@client.event
async def on_ready():
    print('Logged in as', client.user.name)
    print('--ready--')
    mumble.start()
    await asyncio.sleep(5)
    #serverstatus = await checkmumble()
    #print(serverstatus)
    await background_loop()

#openAI
async def aiprocess1(aifinal_question, aiapikey):
    try:
        openai.api_key = aiapikey
        response = openai.Completion.create(
            model="text-davinci-003",
            prompt=aifinal_question,
            temperature=0.5,
            max_tokens=485,
            top_p=0.4,
            frequency_penalty=0.5,
            presence_penalty=0.5,
            stop=[" \n"]
            )

        json_data2 = json.dumps(response.choices)
        aianswer = json.loads(json_data2)
        print(aianswer[0]["text"])
    except Exception as e:
        print(e)
        print("error aiprocess1")
        return "nope"
    return aianswer[0]["text"]
#tivenAI
async def aiprocess2(aifinal_question, aifinal_questionoriginal):
    global totalaierrors
    request = {
        'prompt': aifinal_question,
        'max_new_tokens': 540,
        'preset': 'None',
        'do_sample': True,
        'temperature': 0.5,
        'top_p': 0.5,
        'typical_p': 1,
        'epsilon_cutoff': 0,  # In units of 1e-4
        'eta_cutoff': 0,  # In units of 1e-4
        'tfs': 1,
        'top_a': 0,
        'repetition_penalty': 1.18,
        'repetition_penalty_range': 0,
        'top_k': 20,
        'min_length': 0,
        'no_repeat_ngram_size': 0,
        'num_beams': 1,
        'penalty_alpha': 0,
        'length_penalty': 1,
        'early_stopping': False,
        'mirostat_mode': 0,
        'mirostat_tau': 5,
        'mirostat_eta': 0.1,

        'seed': -1,
        'add_bos_token': True,
        'truncation_length': 2048,
        'ban_eos_token': False,
        'skip_special_tokens': True,
        'stopping_strings': []
    }
    try:
        response = requests.post(aiurl, json=request)

        if response.status_code == 200:
            result = response.json()['results'][0]['text']
            print(aifinal_question)
            print(result)
    except Exception as e:
        print(e)
        print("error aiprocess2")
        totalaierrors += 1
        return "nope"
    return result

#synthesize voice for AI response and broadcast it to channel
async def speech_synthesize(ai_response):
    command = ["espeak", "--stdout", ai_response]
    wave_file = sp.Popen(command, stdout=sp.PIPE).stdout
    # converting the wave speech to pcm
#    command = ["ffmpeg", "-i", "-", "-ac", "1", "-f", "s32le", "-"]
    command = ["ffmpeg", "-i", "-", "-ac", "1", "-f", 's16le', '-ar', '48000', '-']
    sound = sp.Popen(command, stdout=sp.PIPE, stderr=sp.DEVNULL,
                     stdin=wave_file).stdout.read()
    # sending speech to server
    mumble.sound_output.add_sound(sound)
    return

#no loop yet
async def background_loop():
    global totalaierrors
    global dcerrors
    await client.wait_until_ready()
    #mumble.callbacks.set_callback(PYMUMBLE_CLBK_DISCONNECTED, exit_program)
    mumble.callbacks.set_callback(PYMUMBLE_CLBK_TEXTMESSAGERECEIVED, onmumblemsg)
    backcounter = 0
    return

#discord stuff, not ready yett
@client.event
async def on_message(message): 
    rmsg = message.content
    global aikeynumber, totalaierrors
    channel = message.channel
    rmsg2 = rmsg.upper()
    chn = channel
    author = message.author.id

    if message.author == client.user:
        return
    if message.author.bot: 
        return
    elif rmsg2.startswith("ICARUS 201930195036891758973189") and len(rmsg2) > 12:
        print('More than 17 characters, continue.. ' + 'using key n' + str(aikeynumber))
        async with message.channel.typing():
            if totalaierrors > 2:
                return
            
        return 

def Main():
    client.run(token)   

if __name__ == "__main__":
#     asyncio.run(Main())
    Main()
