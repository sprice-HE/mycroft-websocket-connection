#This script runs external to mycroft to listen on a websocket
#for a message (in text form) then send that text to the 
#mycroft message bus as an utterance for mycroft to respond to.
#A skill is needed in mycroft to take the "speak" response and 
#forward it on to whatever service you'd like.
#The Telegram skill is a good reference for taking the "speak"
#event and forwarding it on to another event listener.


import websockets, asyncio, logging

logging.basicConfig(filename="/yourfilepath/filename", level=logging.INFO)

async def sendMycroftUtt(msg):
    try:
		#this is your mycroft message bus websocket location, this is the default location
		url='ws://localhost:8181/core'
		#connect and send msg to mycroft message bus
        async with websockets.connect(url) as websocket:
			#the message is a string without "", those are added below
			#so don't pass a string like '"message"'
			#if you print or log m, the utterances value should look like: ["your message"]
            m = '{"type": "recognizer_loop:utterance", "data": {"utterances": ["' + str(msg) +'"],"lang":"en-us"'+'}'+'}'
            result = await websocket.send(m)
            logging.info(result)
            #Once sent it will disconnect from the mycroft message bus
    
    except Exception as e:
        logging.error(e)


async def getMessages():
#This function connects to a websocket and waits for a message
#from whatever service you want mycroft get get messages from
#It loops continuously
    uri = 'ws://host:port/path(if there is a path)'
    async for websocket in websockets.connect(uri):
        try:
            r = await websocket.recv()
            res = json.loads(r)
            #message may be in a nested dictionary, need
            #to extract just the message text. For example,
            #this message is the 4th level down.
            msg=res["level 1"]["level 2"]["level 3"]["message"]
            logging.info(msg)
            await sendMycroftUtt(msg)
        except websockets.ConnectionClosed:
            logging.info("Connection closed...restarting")
            continue
        except Exception as e:
            logging.info("Error occured in getMessages:")
            logging.info(e)
            continue

if __name__=="__main__":
    asyncio.run(getMessages())
