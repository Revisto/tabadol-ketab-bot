# Tabadol-Ketab Telegram Bot
## _A Telegram Bot that you can search a book inventory in [Tabadol-Ketab](https://tabadolketab.com/) with._

![](https://revisto.ir/static/projects-cover/tabadol-ketab.jpg)

Tabadol-Ketab-Telegram-Bot is a fast and user-friendly way telegram bot for checking Tabadol-Ketab book inventory.

## ✨ How To Use

1. Open your Telegram
2. Find this bot -> [@tabadol_ketab_bot](http://t.me/tabadol_ketab_bot)
3. Send your book name and get answers
4. Enjoy!

## ⚙️ Installation Your Own Telegram Bot

tabadol-ketab-bot only and only requires [Docker](https://www.docker.com/) to be run.

Install Docker and start the bot, docker takes care of other dependencies.

```sh
apt install docker-ce
```

Now clone the repo:
```sh
git clone https://github.com/Revisto/tabadol-ketab-bot
cd tabadol-ketab-bot
```

Let's take care of .env files...

```sh
cp tabadol-ketab/.env.example tabadol-ketab/.env
```
.env file contains your telegram bot access token.
```
telegram_robot_access_token = 1234567891:ABCD_123456ABCD123456abcd1234567891
```

## Docker

Make sure that you have done all installation steps and made .env files.
then, build it and run it.
```sh
docker build -t tk_bot .
docker run -d tk_bot
```

## 🤝 Contributing

Contributions, issues and feature requests are welcome.<br />
Feel free to check [issues page](https://github.com/revisto/tabadol-ketab-bot/issues) if you want to contribute.<br /><br />


## Show your support

Please ⭐️ this repository if this project helped you!


## 📝 License

GNUv2

**Free Software, Hell Yeah!**
