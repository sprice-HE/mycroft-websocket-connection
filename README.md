# mycroft-websocket-connection
Python code to connect and send an utterance (in text form) to the Mycroft message bus websocket.
It sends it as a "recognizer_loop:utterance", so mycroft will respond to the message. 
You will need a mycroft skill to forward the "speak" response if you want it sent somewhere other than your speakers.
Read the code comments for additional guidance.
