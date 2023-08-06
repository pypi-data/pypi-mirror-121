# API lib

## File layout
What's in files in the folder.


### API entities
File [api entities](api_entities.py) has all the plain dataclasses used 
to interact with the API.

Nothing notable there.

### Consumer
Consumer API client reference implementations, manages mods' local 
installation, update, etc.

Public interface exposes these functions:
1. `ConsumerClient.filter_mods(...)`
2. `ConsumerClient.inspect_mod(...)`
3. `ConsumerClient.get_mod_download_metadata(...)`
4. `ConsumerClient.save_mod(...)`
5. `ConsumerClient.update_mod(...)`
6. `ConsumerClient.delete_mod(...)`

Here we'll focus on internals, namely, efficient updates.
The key to that is in 2 functions:
1. `ConsumerClient._execute_plan(...)`
2. `_plan_update(...)`

The `_plan_update(...)` function uses metadata about the current 
version of the mod stored locally next to the binary file of the mod itself,
and a new version metadata. Chunk by chunk, it checks if the chunk is a new
one or not, and based on that constructs a plan, in which a single 
entry represents a chunk. That entry specifies what to do - either
1. Download a new chunk
2. Or, the offset, size, hash, sequence #, of the chunk to cut from the current
version.

`ConsumerClient._execute_plan(...)` does exactly that, 
it executes the update plan.


### Creator
Consumer API client reference implementations.

Handles authentication, mod creation, uploading new versions, etc.
Since uploads are handled by a separate service triggered by cloud storage, 
the client has to do a lot to handle local case properly to 
somewhat reproduce the same behaviour at developer machine. 

The most interesting parts probably are:
1. Authentication, token refresh handling.
2. Upload handling.

To get into the first, pay close attention to:
1. `CreatorClient.authenticate(..)`
2. `CreatorClient._authenticate(..)`
3. `CreatorClient.refresh_token(..)`
4. `@auth_check` decorator

The second happens in 2 steps:
1. `CreatorClient.initiate_upload(..)`, and
2. `CreatorClient.upload_mod(..)`

Among the data the first returns, there's a 'policy document'
that is used in the second for GCP Storage to accept an upload 
to a protected storage bucket.
