# ListOptimizer - Telegram Bot
The bot allows the user to optimize their shopping list automatically. 
The bot contains a map of the store and automatically sorts the list to optimize users’ path through the store. The path is constructed using dynamic programming so it is guranteed to be the shortest.

Positions are automatically categorized and assigned to departments using word embeddings. This project uses Navec, which is Russian language based. In order to make categorization work in other languages, other word embeddings should be used.

The bot takes 3 basic commands:

/del# - delete position from the list.

/clear - clear the list.

/sort - sort the list.

If bot receives a message without a command it treats it as an item to add to the list.

# Launch

There are different ways to launch a telegram bot, this is what i did:

- Launch a Debian virtual machine on a remote server
- Install and set following software:
  - python3 - to run the code
  - git - to load and update the code
  - mySQL - to store shopping lists for multiple users
  - tmux - to keep the bot running after ssh session is shut down.
- Fill your credentials into "config.py"
- Launch "bot.py"

  
# Technologies
- Python 3
- Aiogram
- mySQL
- Navec

