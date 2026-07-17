# this launcher.py file is in all of my projects, it basically just restarts the bot if it crashes.

import subprocess
import time
import os

while True:
    os.system("color a")
    os.system("title Clanker Server")
    print("Starting Clanker...")
    
    subprocess.run(["python", "bot.py"])
    
    print("Bot stopped. Restarting in 5 seconds...")
    time.sleep(5)