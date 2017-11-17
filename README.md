# ad2telegram.py
Crappy little Telegram bot for monitoring alarmdecoder network serial server.

Copy EXAMPLE.config to .config and edit the 'token' to include your bot's Telegram token. Edit the 'id' for your chat_id with your bot. You can get this by using "/start" and it will print to the console.

'id' in configuration must match for the /panel and /tail commands to work

Parameters for the ser2sock server are hardcoded. 

/start - prints the chat_id to the console, says "Hi!" to everyone. It all says "Hello ;)" if the chat_id matches.
/tail - return the last 4 messages from the panel
/panel <COMMAND> - send COMMAND to the panel just like you were connected to the ser2sock server. Check /tail for new status.

 
