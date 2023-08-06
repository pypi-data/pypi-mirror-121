# Vankrupt workshop clients
Here you'll find reference implementations of clients 
for interacting with vankrupt workshop APIs.

The library comes with a relatively thin API and CLI clients for 
both uploading mods, and downloading/upgrading them. 

## API library
API client/library [readme](vankrupt_workshop_client/api/README.md) 
will be most helpful for you, if you are looking for references 
on how to implement uploader/downloader clients.
The documentation on how exactly to process downloads, updates, 
perform uploads is there as well.

## CLI client
CLI client [readme](vankrupt_workshop_client/README.md) 
is a good reference on how exactly to use API clients and tie them up
to a concrete environment.


## General info / status
It works against the environment you choose, both cli clients can be configured
to work with `dev / prod / local` environments.

Currently it works against dev by default. When prod gets pulished, will 
work with that.


## Installation
The library is published to PyPi under the name 
[vankrupt-workshop-client](https://pypi.org/project/vankrupt-workshop-client).

Thus, to use it locally all you'd need to do is install it.
I'd recommend to do it the following way:
1. Create python virtual env:
    ```shell script
    python3 -m venv venv
    ```
2. Activate it:
    ```shell script
    source venv/bin/activate
    ```
3. Install:
    ```shell script
    pip install vankrupt-workshop-client
    ```
4. Use however you'd like, i.e.:
    ```shell script
    vankrupt_download filter-mods --page 1 --platform ps5
    ```
   For usage details, refer to 
   CLI client [readme](vankrupt_workshop_client/README.md).

Quickstart: run
1.
    ```shell script
    vankrupt_download --help
    ```
2.
    ```shell script
    vankrupt_upload --help
    ```
