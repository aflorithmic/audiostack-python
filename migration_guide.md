# apiaudio -> audiostack sdk migration guide
In general the audiostack SDK has a large number of improvements over its predecessor. It operates in a broadly similar way.

## Objects
All objects are now split into one of four families, these are Content, Speech, Production and Delivery.

The following objects have been migrated as follows:

- ```Script.<function>() -> Content.Script.<function>()```
- ```Media.<function>() -> Content.Media.<function>()```
- ```Speech.<function>() -> Speech.TTS.<function>()```
- ```Voice.<function>() -> Speech.Voice.<function>()```
- ```Lexi.<function>() -> Speech.Diction.<function>()```
- ```Mastering.<function>() -> Production.Mix.<function>()```
- ```Sound.<function>() -> Production.Sound.<function>()```

The following objects are deprecated

- Birdcache

The following objects are in development

- Connector
- Orchestrator
- Webhooks

The following objects are new.

```Delivery.Encoder```

## Response types

Our API supports the following HTTP protocools, and the SDK represents these though methods on each object. I.e. Script.create() represents making a POST request.

POST: `.create()`
- creates a new resource, in the SDK this returns an `item` of type resource (i.e. `script`)

PUT `.update()`
- updates a new resource, in the SDK this returns an updated `item` of type resource (i.e. `script`)

GET: `.get()` or `.list()`
- Gets an existing resource, in the SDK this returns an  `item` of type resource (i.e. `script`), **or** a `list` of `items`

DELETE `.delete()`
- Deletes a resource, in the SDK this does not return any object


### Object types

Calls to most object functions, will create an instance of an item object. For example, calling `Script.create()` returns a `Script.Item` object. These objects can have operations such as `update`, `delete` and `download` applied directly to them. For example, a script can be deleted either through the static `Script.delete()` method or by calling `.delete()` on a `Script.Item` object.

## Per service changes
The following section outlines changes for each service.

### Script
#### Breaking changes
- Script create always creates a new resource, it never updates an existing one. `scriptId` can no longer be defined by the end-user. In addition the script syntax has changed, a guide for this can be found here: https://dash.readme.com/project/audiostack/v1.0/docs/script-syntax.

### New features
- Scripts can be updated with the `.update` method.

### TTS (formally just Speech)
#### Breaking changes
- Speech files can no longer be retrieved by `scriptId`, instead every call to `TTS.create()` will create a new resource, and return a unique `speechId`. Likewise the URL returned for each TTS asset is now a unique link and will never expire.


#### New features
- TTS assets can be listed and deleted by `scriptId`, `scriptName`, `projectName` and `moduleName`.
- TTS resources can be made public with the `public` value in `TTS.create()` 
- A `TTS.create()` request can take either a `scriptId` str value, or a `scriptItem` object (the client side python object return from a `Script.create()` call).


### Mix (formally Mastering)

#### Breaking changes
- Mastered files can no longer be retrieved by scriptId, instead every call to `Mix.create()` will create a new resource, and return a unique `productionId`. Likewise the URL returned for each TTS asset is now a unique link and will never expire.
- To produce a mixed file (formally mastering) requires a `speechId` instead of a `scriptId`
- `endFormat` can no longer be specified in the `Mix.create()` call, instead see the `Delivery` endpoints.

#### New features
- Mixed assets can be listed and deleted by `scriptId`, `scriptName`, `projectName` and `moduleName`.
- Mixed resources can be made public with the `public` value in `Mix.create()` 
- A `Mix.create()` request can take either a `speechId` str value, or a `speechItem` object (the client side python object return from a `Speech.create()` call).


## v1 vs v2

The following apiaudio code:

```python
import apiaudio
apiaudio.api_key = "your-key"

# script creation
script = apiaudio.Script.create(scriptText="Hello world")

# speech creation
response = apiaudio.Speech.create(scriptId=script["scriptId"], voice="Aria")

print(response)

# mastering process
response = apiaudio.Mastering.create(
	scriptId=script.get("scriptId"),
	soundTemplate="jakarta"
	)
print(response)

# download
filepath = apiaudio.Mastering.download(scriptId=script["scriptId"], destination=".")
print(filepath)
```

Can be reproduced in v2 as follows:

```python
import audiostack
audiostack.api_key = "your-key"

script = audiostack.Content.Script.create(scriptText="hello world")
print(script.message, script.scriptId)

tts = audiostack.Speech.TTS.create(scriptItem=script, voice="Aria")
print(tts)
tts.download(autoName=True)

mix = audiostack.Production.Mix.create(speechItem=tts, soundTemplate="jakarta")
print(mix)

enc = audiostack.Delivery.Encoder.encode_mix(productionItem=mix, preset="mp3_low")
enc.download()
```
