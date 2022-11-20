# Honeygain Bot

Honeygain bot lets you automatically participate in the [Lucky Pot game](https://www.honeygain.com/lucky-pot-rules/).

This bot uses your Honeygain email and password to login when it runs for its first time. After that, it saves the cookies and local storages of Honeygain on your computer so that it can use them to login in the future.

## Usage Instructions

1. Type your Honeygain email and password in `secrets.py` file.

2. Run `pip install -r requirements.txt` to install required python packages

3a. Setup a script to run `python HoneygainBot.py` daily. For example, you may use [crontab](https://crontab.guru/) to trigger this bot
    ```
    10 * * * * /path/to/your/python /path/to/honeygain-bot/HoneygainBot.py
    ```

OR

3b. Run the script with the argument `true` like this: `python HoneygainBot.py true`. This will allow the script to run daily.

If you find this bot useful, please consider using [my registration link](https://r.honeygain.me/I745M22C51) to create your honeygain account. This will add you in my referral list and both you and I will get a reward from Honeygain. 

