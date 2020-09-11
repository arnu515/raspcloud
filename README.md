# RaspCloud

Your data, stored on your server.

Are you worried about big tech companies like Google and Microsoft *snooping through your data* that you upload on the cloud? They say they don't do it, but you can't trust them, because they have done it before.

Behold **RaspCloud**, made up of two words, **raspberry pi** and **cloud**, because this is a cloud service for **your** raspberry pi (or any other server, really).

Since the data is stored on **your** server, only **you** have access to **your data**.

## Installation and setup

SSH into/get terminal access to your always online server (can be your raspberry pi that stays online all the time, or any VPS, dedicated, etc.) and clone this repository:
```sh
git clone https://github.com/arnu515/raspcloud raspcloud
cd raspcloud
```

Next, make sure you have [python3](https://python.org) and python3's package manager pip3 installed. Your package manager probably has python in its repos (usually goes by the name of `python3` for debian and fedora, but `python` for arch).

Install the required dependencies with:
```
pip install -r requirements.txt
```
_You can also use a virtual environment._

We need to add some environment variables first. Create a file called `.env`. We need to add this in it:
```
FERNET_KEY=<a fernet key>
FERNET_PWKEY=<another fernet key>
```
To get these keys, you can use the `python` `cryptography` module.
```python
from cryptography.fernet import Fernet
print(Fernet.generate_key().decode())
print(Fernet.generate_key().decode())
```
It will give you two keys as output. Copy and paste them in your .env

Finally, start the server by running the `start.sh` file:
```
sh start.sh
```

This will run a `gunicorn` server on port 80, so if that port is occupied, change it in the `start.sh` file:
```
gunicorn -b 0.0.0.0:<PORT> wsgi:app
```

Finally, visit your server's ip in your browser and **boom**! You should be greeted with a page prompting you to install RaspCloud.
_If your server is not on your local network, you may have to open up ports using your VPS provider's console or with `ufw` (**U**ncomplicated **F**ire**W**all)

```sh
# 1. Install UFW if it isn't
# sudo apt install ufw
# 2. Open port 80 (or whatever port you've set up)
sudo ufw allow 80 # or sudo ufw allow http
```

You can deploy RaspCloud with NGINX by following [this guide](https://www.linode.com/docs/platform/one-click/how-to-deploy-flask-with-one-click-apps/)  
*Yes, it is for Linode servers, but the steps are the same*

> You may have to use `sudo` before `sh start.sh` if port binding fails.

### Setup

Head over to the `/install` route on your RaspCloud and fill out the form. You'll be creating an **admin account**.  
Click `Finish configuration` and restart RaspCloud (Press Ctrl+C in the terminal and run `sh start.sh` again).

And now, log in to raspcloud and there! You have an interface that looks similar to Google Drive and OneDrive.

## Usage

### Adding items

Click the `+` icon on the navbar to open a sub-menu that allows you to create a folder and upload files *for now*.
> *Can't see the icons?* Refresh the page.

Clicking on either options opens a *modal* where you can enter a name for the folder or upload files respectively.

### Viewing items

Click on the folder icons/names to go into that folder. Click the file icons/names to download them (or view them if your browser supports viewing them).

## Credits

- Written in `python3` using `PycharmCE` editor
- `flask` micro-framework with extensions used for website
- See `requirements.txt` for the python packages used
- Stackoverflow, for helping me with bugs and other problems
- FontAwesome 5, for the amazing icons