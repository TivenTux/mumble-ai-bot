import os
from os import environ
import time
import requests
import subprocess as sp
import json
import pymumble_py3
import re
import asyncio
from pymumble_py3.constants import *
import openai

############ conf ############
#use number 1 for openAI or 2 for custom api
aiselection = 1
#openAI settings
#create api at https://platform.openai.com/account/api-keys
if environ.get('openaikey') is not None:
    openaikey = os.environ['openaikey']
else:
    openaikey = ''

#hosted LLM settings - use this if you dont want to use openAI and host your LLM elsewhere
aihost = '127.0.0.1:9500'
aiurl = f'http://{aihost}/api/v1/generate'

#general ai settings
pass_username = 1 #1 to enable, 0 to disable. Provides the user's name to the prompt (and lets the bot know who is talking with it).

#mumble settings for bot
if environ.get('mumble_host') is not None:
    mumble_host = os.environ['mumble_host']
else:
    mumble_host = '127.0.0.1'
if environ.get('portnumber') is not None:
    portnumber = os.environ['portnumber']
else:
    portnumber = '64738'
if environ.get('bot_nickname') is not None:
    bot_nickname = os.environ['bot_nickname']
else:
    bot_nickname = 'Phoenix'
#if passwd is set, use it else dont use pass
if environ.get('mumble_passwd') is not None:
    mumble_passwd = os.environ['mumble_passwd']
else:
    mumble_passwd = ''
if environ.get('bot_keyword') is not None:
    bot_keyword = os.environ['bot_keyword']
else:
    bot_keyword = 'Phoenix'

mumble_use_cert = 0 #change to 1 if you want to use certificate. remember to generate it first
certfilemumble = './constants/public.pem'
keyfilemumble = './constants/private.pem'
mumble = pymumble_py3.Mumble(str(mumble_host), bot_nickname, port=int(portnumber), password=mumble_passwd, reconnect=True)
if mumble_use_cert == 1:
    mumble = pymumble_py3.Mumble(str(mumble_host), bot_nickname, port=portnumber, password=mumble_passwd, reconnect=True, certfile=certfilemumble, keyfile=keyfilemumble)



#init some stuff
aikeynumber = 0
dcerrors = 0
totalaierrors = 0
punishedusers = []
mumbleusercomment = ' '
#check length to help with message cleaning later
nicknamelen = len(bot_nickname)


def on_start():
    '''
    start library thread and connection process
    '''
    print('--ready--')
    mumble.start()
    mumble.callbacks.set_callback(PYMUMBLE_CLBK_TEXTMESSAGERECEIVED, onmumblemsg)
    while 1:
        time.sleep(1)
    return

def finPrompt(text, username=""):
    '''
    Takes question text and username (if any) and returns final prompt.
    '''
    if username != "":
        return "Below is a conversation between a user named " + username + " and an AI assistant named " + bot_nickname + ".\n" + bot_nickname + " was made by Tiven and provides helpful answers.\n" + username + ": " + text + "\n" + bot_nickname + ":"
    else:
        return "Below is a conversation between a user and an AI assistant named " + bot_nickname + ".\n" + bot_nickname + " was made by Tiven and provides helpful answers.\n" + "User: " + text + "\n" + bot_nickname + ":"

async def msgprocess(text, usern):
    '''
    Takes text and username, processes the prompt and calls openAI,SpeechSynth and msgsend.
    '''
    try:
        if aiselection == 1:
            if pass_username == 1:
                aifinal_question = finPrompt(text, usern)
                ai_response = await aiprocess1(aifinal_question, openaikey)
            else:
                aifinal_question = finPrompt(text)
                ai_response = await aiprocess1(aifinal_question, openaikey)
        if aiselection == 2:
            if pass_username == 1:
                aifinal_question = finPrompt(text, usern)
                ai_response = await aiprocess2(aifinal_question, text)
            else:
                aifinal_question = finPrompt(text)
                ai_response = await aiprocess2(aifinal_question, text)
    except Exception as e:
        print(e, 'ai api error')
        return
    try:
        await speech_synthesize(ai_response)
    except Exception as e:
        print(e, 'speech synthesizer error')
    try:
        await msgsend(ai_response)
    except Exception as e:
        print(e, 'mumble text send error')
    return

async def msgsend(ai_response):
    '''
    Takes AI response and sends it to the mumble channel.
    '''
    msg = ai_response.encode('utf-8', 'ignore').decode('utf-8')
    mumblechan = mumble.channels[mumble.users.myself['channel_id']]
    mumblechan.send_text_message(msg)
    return

#clean up message, find author and forward
def onmumblemsg(text):
    '''
    Takes message text, gets author's name and forwards it.
    '''
    print('received msg.. passing through')
    print(text)
    rmsg = text.message
    #get username from message and process the rest of the message
    rmsg = rmsg[nicknamelen:]
    try:
        usern = str(mumble.users[text.actor]['name'])
        usern = cleanupname(usern)
    except Exception as e:
        print(e)
        usern = ''
    rmsg2 = text.message.upper()

    if text.actor == 0 or text.session:
    # Some servers will send a welcome message to the bot once connected.
    # It doesn't have a valid "actor". Simply ignore it here.
        print('ignoring pm: ' + rmsg2)
        return
    upper_bot_keyword = bot_keyword.upper()
    if rmsg2.startswith(upper_bot_keyword):
        start_this_now = asyncio.run(msgprocess(rmsg, usern))
    else:
        print('ignoring pm: ' + rmsg2)
    return

#remove any special characters from user name
def cleanupname(datainput):
    '''
    Takes username and removes any special characters.
    '''
    cleanedupname=re.sub("[^A-Za-z]","",datainput)
    cleanedupname = cleanedupname[0].upper() + cleanedupname[1:]
    #print ('clean: ', cleanedupname)
    return (cleanedupname)


#openAI
async def aiprocess1(aifinal_question, aiapikey):
    '''
    Takes question and chatgpt apikey and returns AI response.
    '''
    try:
        openai.api_key = aiapikey
        response = openai.Completion.create(
            model="text-davinci-003", #available models here: https://platform.openai.com/docs/models/overview
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
        print(e, "--error aiprocess1")
        return "nope"
    return aianswer[0]["text"]
#tivenAI
async def aiprocess2(aifinal_question, aifinal_questionoriginal):
    '''
    Takes question and original question, and returns AI response.
    '''
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
        print(e,"--error aiprocess2")
        totalaierrors += 1
        return "nope"
    return result

#synthesize voice for AI response and broadcast it to channel
async def speech_synthesize(ai_response):
    '''
    Takes AI response, generates speech and sends to the channel.
    '''
    command = ["espeak", "--stdout", ai_response]
    wave_file = sp.Popen(command, stdout=sp.PIPE).stdout
    # converting the wave speech to pcm
#    command = ["ffmpeg", "-i", "-", "-ac", "1", "-f", "s32le", "-"]
    command = ["ffmpeg", "-i", "-", "-ac", "1", "-f", 's16le', '-ar', '48000', '-']
    sound = sp.Popen(command, stdout=sp.PIPE, stderr=sp.DEVNULL,
                     stdin=wave_file).stdout.read()
    # sending speech to mumble channel
    mumble.sound_output.add_sound(sound)
    return


def Main():
    on_start()  

if __name__ == "__main__":
    Main()
    # loop = asyncio.get_event_loop()
    # loop.run_until_complete(Main())