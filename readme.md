# Web - TAGS
### Description
URL links catalog inside blockchain.
The links is divided into networks, types, languages and TAGS. Also any link can have many descriptions added by other users ...
### Instalation
* Download and install Emercoin wallet from https://emercoin.com/
* Add folowing params to your ~/.emercoin/emercoin.conf file in Linux %APPDATA%\emercoin\emercoin.conf file in Windows
```
rpcuser=USER
rpcpassword=PASSWORD
rpcallowip=localhost
rpcport=PORT
```
* Install Python
* Run `git clone https://github.com/Alex014/WEB_TAGS.git`
* Run `cd WEB_TAGS` and then
```
pip install flask
pip install requests
pip install json-rpc
```
* Run `./run.sh`
* GOTO http://127.0.0.1:5000/config and configure connection to Emercoin wallet
### Inside structure (in blockchain)
#### Name: webtags:something
#### Value:
* LINK
```
{
    "url": "[ANY type of URL]", 
    "network": "[INET|TOR|YGGRASSIL|I2P ... ]", 
    "type": "[video|torrent|blog ... ]", 
    "lang": "[en|de|cn ... ]", 
    "tags": "[any,combination,of,tags,coma,separated]", 
    "description": "[Any type of text ... ]"
}
```
* Description of existing link
```
{
    "url": "[URL of existing link]", 
    "description": "[Any type of text ... ]"
}
```
### Using
* Emercoin https://emercoin.com/
* Python https://www.python.org/
* Requests https://requests.readthedocs.io/
* Flask framework https://flask.palletsprojects.com/
* SQLITE https://www.sqlite.org/
* Bootstrap http://getbootstrap.com/
### Donate
* Emercoin EQkpLeX4FhqxnoXdPMJqnaHxJHHgNgTKLh
* Bitcoin 1JU7QyyiavuKeZvCkxA269a3wnf8qb1S5p