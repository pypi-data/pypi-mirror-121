# CLI clients
In this document it is assumed, that you have library installed.


## General info / status
There are 2 cli clients:
1. vankrupt_download
2. vankrupt_upload

The pattern of usage is the same for both of them:
```shell script
vankrupt_upload [OPTIONS] COMMAND [ARGS]
```
Both of them have `--help` and `--version` options:
```shell script
vankrupt_upload --help
```
```shell script
vankrupt_upload --version
```
Both of them store their respective config files under current OS user's
default config folder (i.e. for ubuntu that's 
`~/.config/vankrupt_workshop_client/version/some_config_file`).


## CLI uploader
You can override where this client will store its metadata 
(access and refresh keys for authentication) using the `--config_store`
option.

You as well can override which environment to act against using
the `--env` option. Note that each environment would have 
a separate 'login state' (i.e. you can be logged in at dev, but not local).

It is pretty minimalistic, in terms of breadth, but feature-full
enough client you can use to upload mods. It remembers your 
refresh token and stores them in config folder, and puts it to use
when needed.


### Commands
To see help on a particular command, enter, e.g.:
```shell script
vankrupt_upload create-mod --help
```
It has following commands:
1. create-mod
2. echo
3. get-me
4. login
5. logout
6. upload

All of them are pretty self explanatory, use help if anything's unclear.

Note: to execute some of these commands you'll be asked to authenticate first.


## CLI downloader
You can override which environment to act against using
the `--env` option. Note that each environment would have 
a separate 'login state' (i.e. you can be logged in at dev, but not local).

This client focuses solely on mod download/update/storage/upkeep tasks.
It has all the capabilities needed to efficiently update maps.
And please not, that the reference downloading API client puts way too
much effort into making sure everything's fine. For instance, it 
checks each chunk's custom hash, sequence linearity, etc. at each step,
where possible, that's generally speaking, an overkill, checking md5 
of the final artifact is sufficient enough for the production client
to be shipped to the user. 


### Commands
It has commands:
1. init
2. deinit
5. filter-mods
6. inspect-mod

You can use these without initial setup, but to perform any 
storage-related tasks, you'd have to run "init" command first.

Storage commands:
1. download
2. update
3. delete
4. list-downloaded

Again, use help if anything's unclear.
