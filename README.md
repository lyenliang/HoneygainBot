# Honeygain Bot

Honeygain bot lets you automatically participate in the [Lucky Pot game](https://www.honeygain.com/lucky-pot-rules/).

This bot uses your Honeygain email and password to login when it runs for its first time. After that, it saves the cookies and local storages of Honeygain on your computer so that it can use them to login in the future.

## Usage Instructions

1. Copy `secrets.py.template` file and name the new file as `secrets.py`. 

   `cp secrets.py.template secrets.py`

   This can help you prevent from accidentally committing your Honeygain account password to github.

2. Type your Honeygain email and password in `secrets.py` file.

3. Run `pip install -r requirements.txt` to install required python packages

4. Setup a script to run `python HoneygainBot.py` daily. For example, you may use [crontab](https://crontab.guru/) to trigger this bot
    ```
    30 23 * * * /path/to/your/python /path/to/honeygain-bot/HoneygainBot.py`
    ```

If you find this bot useful, please consider using [my registration link](https://r.honeygain.me/I745M22C51) to create your honeygain account. This will add you in my referral list and both you and I will get a reward from Honeygain. 

## Future Plans

* Use docker to run Honeygain bot to reduce compatibility issues on different operating systems.
* Find a suitable platform to trigger the bot daily.