<p align="center">
<a href="https://www.api.audio/" rel="noopener">
 <img src="https://uploads-ssl.webflow.com/60b89b300a9c71a64936aafd/60c1d07f4fd2c92916129788_logoAudio.svg" alt="api.audio logo"></a>
</p>

<h3 align="center">apiaudio - audiostack SDK</h3>

---

<p align="center"> audiostack is the official <a href="https://www.api.audio/" rel="noopener">api.audio</a> Python 3 SDK. This SDK provides easy access to the api.audio API for applications written in python.
    <br>
</p>

## Maintainers <a name = "maintainers"> </a>

- https://github.com/Sjhunt93

## License <a name = "license"> </a>

This project is licensed under the terms of the MIT license.

# 📝 Table of Contents

- [Changelog](CHANGELOG.md)
- [About](#about)
- [Changelog](#changelog)
- [Quickstarts](#quickstarts)
- [Getting Started](#getting_started)
- [Hello World](#hello_world)
- [Authentication](#authentication)
- [Authentication with environment variable](#authentication_env)
- [Super Organizations](#super-organizations)
- [Documentation](#documentation)
  - [Script](#script)
  - [Speech](#speech)
  - [Voice](#voice)
  - [Sound](#sound)
  - [Mastering](#mastering)
  - [Media](#media)
  - [SyncTTS](#synctts)
  - [Birdcache](#birdcache)
  - [Pronunciation Dictionary](#pronunciationdictionary)
  - [Connector](#connector)
  - [Orchestrator](#orchestrator)
  - [Webhooks](#webhooks)
  - [Logging](#logging)
- [Maintainers](#maintainers)
- [License](#license)

## 🧐 About <a name = "about"></a>

This repository is actively maintained by [Aflorithmic Labs](https://www.aflorithmic.ai/). For examples, recipes and api reference see the [api.audio docs](https://docs.api.audio/reference). Feel free to get in touch with any questions or feedback!

## :book:  Changelog

You can view [here](CHANGELOG.md) our updated Changelog.

## :speedboat:  Quickstarts <a name = "quickstarts"></a>

Get started with our [quickstart recipes](https://github.com/aflorithmic/examples).

## 🏁 Getting Started <a name = "getting_started"></a>

### Installation

You don't need this source code unless you want to modify it. If you want to use the package, just run:

```sh
pip install audiostack -U
#or
pip3 install audiostack -U
```


### Prerequisites <a name = "requirements"></a>

Python 3.6+

## 🚀 Hello World <a name = "hello_world"></a>

Create a file `hello.py`

```python
touch hello.py
```

### Authentication

This library needs to be configured with your account's api-key which is available in your [api.audio Console](https://console.api.audio). Import the apiaudio package and set `apiaudio.api_key` with the api-key you got from the console:

```python
import audiostack
audiostack.api_key = "your-key"
```


### Create Text to audio in 4 steps

Let's create our first audio asset.

✍️ Create a new script, our `scriptText` will be the text that is later synthesized.

```python
script = audiostack.Content.Script.create(scriptText="hello world")
print(script.message, script.scriptId)
```

🎤 Render the scriptText that was created in the previous step. Lets use voice Aria. Lets download our tts file also.

```python
tts = audiostack.Speech.TTS.create(scriptItem=script, voice="Aria")
print(tts)
tts.download(autoName=True)
```

🎧 Now let's mix the speech we just created with a sound template.

```python
mix = audiostack.Production.Mix.create(speechItem=tts, soundTemplate="jakarta")
print(mix)
```

Lets convert out produced mix into a mp3 and download it.

```python
enc = audiostack.Delivery.Encoder.encode_mix(productionItem=mix, preset="mp3_low")
enc.download()
```

Easy right? 🔮 This is the final `hello.py` file.

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

Now let's run the code:

```sh
python hello.py
#or
python3 hello.py
```

Once this has completed, find the downloaded audio asset and play it! :sound: :sound: :sound: 


### Import <a name = "import"></a>

```python
import audiostack
```

### Authentication <a name = "authentication"></a>

The library needs to be configured with your account's secret key which is available in your [Aflorithmic Dashboard](https://console.api.audio). Set `audiostack.api_key` with the api-key you got from the dashboard:

```python
audiostack.api_key = "your-key"
```

### Authentication with environment variable (recommended) <a name = "authentication_env"></a>

You can also authenticate using `audiostack_key` environment variable and the apiaudio SDK will automatically use it. To setup, open the terminal and type:

```sh
export audiostack_key=<your-key>
```

If you provide both an environment variable and `audiostack.api_key` authentication value, the `audiostack.api_key` value will be used instead.

### Logging <a name = "logging"></a>

By default, warnings issued by the API are logged in the console output. Additionally, some behaviors are logged on the informational level (e.g. "In progress..." indicators during longer processing times).
The level of logging can be controlled by choosing from the standard levels in Python's `logging` library.

- Decreasing logging level for more detailed logs:
  ```python
  audiostack.set_logger_level("INFO")
  # audiostack.set_logger_level("CRITICAL") - set the highest level to disable logs
  ```

<!-- ### Super Organizations

In order to control a child organization of yours, please use the following method to *assume* that organization id.

Set your child organization id to `None` to stop assuming an organization. Subsequent calls to the api will use your own organization id.

```python
import apiaudio

apiaudio.set_assume_org_id('child_org_id')

# Stop using
apiaudio.set_assume_org_id(None)
```

See [organization](#organization) resource for more operations you can perform about your organization. -->

## 📑 Documentation <a name = "documentation"></a>
### `Diction` resource <a name = "diction"> </a>
#### Product Description
Our dictionary service is...


---
- `create()` Add word to a custom dictionary


	``` audiostack.Speech.Diction.create(<args>)```


	For each language, only a single word entry is permitted. However, each word can have multiple specializations. When a word is first registered a default specialization is always created, which will match what is passed in. Subsequent calls with different specializations will only update the given specialization. The exact repacement that will be used is determined by the following order of preference:voice name > language dialect > provider name > defaultFor example, a replacement specified for voice name sara will be picked over a replacement specified for provider azure.
	- Parameters:
		 - `lang` (string) - Language family, e.g. en or es.dictionary - use global to register a word globally (default).
		 - `word` *[required] (string) - Word to be replaced.
		 - `replacement` *[required] (string) - The replacement token. Can be either a plain string or a IPA token.
		 - `contentType` (string) - The content type of the supplied replacement, can be either basic (default) or ipa for phonetic replacements.
		 - `specialization` (string) - by default the supplied replacement will apply regardless of the supplied voice, language code or provider. However edge cases can be supplied, these can be either a valid; provider name, language code (i.e. en-gb) or voice name.

---
- `delete()` Deletes a word from a dictionary.


	``` audiostack.Speech.Diction.delete(<args>)```


	By default this will delete all specializations of the word, if you want to delete a specific specialization, supply this as a query parameter
	- Parameters:
		 - `lang` *[required] (string) - 
		 - `word` *[required] (string) - 
		 - `specialization` *[required] (string) - Delete a specific specialization

---
- `list()` List dictionaries


	``` audiostack.Speech.Diction.get(<args>)```


	Lists all  public dictionaries. This lists all the words but not the actual replacements. Listing of replacement tokens for inbuilt dicts is not available
	- Parameters:
		 - (none) 

---
- `list()` List dictionaries


	``` audiostack.Speech.Diction.get(<args>)```


	Lists all custom dictionaries. This lists all the words but not the actual replacements.
	- Parameters:
		 - (none) 

---
- `list()` Lists all words within a custom dictionary. Lang must be supplied.


	``` audiostack.Speech.Diction.get(<args>)```

	- Parameters:
		 - `lang` *[required] (string) - 

---
### `TTS` resource <a name = "tts"> </a>
#### Product Description

Our Text-to-speech provides harmonious access to more than 8 external TTS providers. Our single interface ensures no matter the provider your script content will be synthesized to the highest quality. We have a number of text inteligence services that you can use to improve and humanise synthetic voices, these are located in the `speech/lexi` endpoints. 


---
- `create()` Create a text-to-speech resource.


	``` audiostack.Speech.TTS.create(<args>)```


	To create speech you need to supply the scriptId of the script you wish to generate, and the voice you would like to generate this request.
	- Parameters:
		 - `scriptId` *[required] (string) - Reference to the Script that is to be synthesized, use `/script` to create and get it.
		 - `version` (string) - Specific version of the referenced Script.
		 - `voice` (string) - Either alias or original (provider's) ID. Available voices are listed at https://library.api.audio/

		 - `speed` (number) - Scalar for speed manipulation, range 0.5-3.
		 - `silencePadding` (string) - Amount of microseconds for silence padding. Half of the amount is inserted as silence at the beginning and at the end of each Speech file.
		 - `effect` (string) - Effect to apply to TTS.
		 - `audience` (object) - Object defining the values for Script parameters. E.g. for Script parameters in `Hello {{username}}, how's your {{weekday}} going?` the object would be `{"username": "Michael", "weekday": "Sunday"}`.

		 - `sections` (object) - Separate configurations for Script section. E.g. to specify a separate voice and speed for Script section `intro` the object would be `{"intro": {"voice": "Leah", "speed": 1.2}}`.

		 - `useDictionary` (boolean) - Whether to apply text corrections such as lexi and normalization
		 - `public` (boolean) - Makes returned URLs publicly available

---
- `list()` Lists multiple text-to-speech resources.


	``` audiostack.Speech.TTS.get(<args>)```


	Returns a list of speech files that have been created. Can be filtered by `projectName`, `moduleName`, `scriptName` and `scriptId`.
	- Parameters:
		 - `projectName` (string) - 
		 - `moduleName` (string) - 
		 - `scriptName` (string) - 
		 - `scriptId` (string) - 
		 - `paginationToken` (string) - 
		 - `verbose` (boolean) - 

---
- `get()` Retrieve a text-to-speech resource.


	``` audiostack.Speech.TTS.get(<args>)```

	- Parameters:
		 - `speechId` *[required] (string) - 

---
- `delete()` Deletes a text-to-speech resource


	``` audiostack.Speech.TTS.delete(<args>)```

	- Parameters:
		 - `speechId` *[required] (string) - 

---
- `create()` Synthesize speech directly from text.


	``` audiostack.Speech.TTS.create(<args>)```


	#### sync Product DescriptionGood for time-critical applications. **Maximum runtime is 30 seconds**.\n### Caching\nTTS responses are globally cached to improve performance. You can set `Cache-Control` to `no-cache` to skip the cache.\nFollowing parameters are hashed as the cache key:\n  - text\n  - voice\n  - speed\n  - metadata\n  - effect\n  - bitrate\n  - sampling_rate\n  - output specified by the `Accept` header\n\nCache is missed when any of these parameters change.\n
	- Parameters:
		 - `text` *[required] (string) - Text to synthesize. Maximum 800 characters.
		 - `ssml` (string) - Text in SSML format to synthesize. Maximum 1000 characters. Expected SSML format varies depending on provider of the voice.
		 - `voice` *[required] (string) - Either alias or original (provider's) ID. Available voices are listed at https://library.api.audio/

		 - `metadata` (boolean) - Return JSON with base64 encoded audio and visemes, if available.
		 - `sampling_rate` (string) - Sampling rate of the output. Applicable to wave format.
		 - `bitrate` (string) - Bitrate of the output. Applicable to mp3 format.
		 - `effect` (string) - Effect to apply to TTS.
		 - `speed` (number) - Scalar for speed manipulation, range 0.5-3.

---
### `Script` resource <a name = "script"> </a>
#### Product Description

Simply put, a script is the format that makes creating and audio with audiostacks, accessible, scalable and awesome. In summary a script contains a series of commands for producing beautifully rendered text-to-speech, that can later be mixed with custom media files and dynamically adjustable sound templates. In the most basic example, a script with the text ``hello world`` will permit our speech services #here to render a syntehtic rendition of the words ``hello world``.

To annotate a script we have a collection of *markup* syntax used to signify sections, sound effects, dictionary flags and more.

These can be grouped as:

### Section Tag:
The sytax for this uses ``<< tagName :: identifier >>``, for example ``<<sectionName::into>>`` to signify the following script text belongs to the intro section. Valid tag names are `sectionName`, `soundSegment`, `soundEffect`, ,`media`.

### Dictionary flag:
The syntax for a dictionary flag uses either `<!word>` or ``<` word or sentence>``. The first is used when a word can have multiple pronunciations, for example, the french city *"Nice"*, ordinarily it would be pronounced as nice (as in what a nice place to eat), to force the alterative pronunciation, words should be marked with the `<!nice>` syntax. The ``<`>`` syntax is used to force the text between the start ``<` `` and end `>` flags to be preserved as is, i.e. no text correction services are applied. See this link for more documentation on this.

### Audience parameters
Audience parameter syntax can be used to customise or 'fill in' variable words/text during the TTS creation stage. The syntax for this is ``{{name|default text}}``, for example you might have the the scriptText ``"hello {{name|new user}} and welcome to audio stack"``. This permits a single script to be created, and have unlimited variants of this synthesised with our speech creation services. See here for a comprehensive guide to audience parameters.

### SSML
SSML stands for Speech Synthesis Markup Language, and many TTS providors supply a collection of these tags for customising the sonice rendering of TTS voices, for example, changing prosidy, speaking speed, or inserting pauses between words. The syntax is ``<SSMLTagName parameters> ``, for a comprehensive list of SSML tags see this helpful guide.


---
- `create()` Create a Script resource.


	``` audiostack.Content.Script.create(<args>)```


	Creates a new script resource. Scripts are organised by directories, of which there are 3, projectName, moduleName, scriptName. Within this structure an indivdual script has a scriptId that is unique. It is possible to have multiple scripts under a given ``projectName/moduleName/scriptName`` structure. Therefore repeated calls to this endpoint will create multiple scripts. Use script update (PUT) to update an existing script (with its unique scriptId)A script's default version is v0. You can create multiple versions of one scriptId, which is handy in cases of multilingual coverage, targeted content etc. To create another version of a script use the PUT method.
	- Parameters:
		 - `projectName` (string) - 
		 - `moduleName` (string) - 
		 - `scriptName` (string) - 
		 - `scriptText` *[required] (string) - 

---
- `update()` Updates a Script resource.


	``` audiostack.Content.Script.update(<args>)```


	Updates an existing script resource. Additional versions can be appended to a given scriptId. To do this supply the version field with a named version. For example, `en` or `es`. By default `v0` is reserved and represents the fist version created when the original script was created with a (POST) request.
	- Parameters:
		 - `scriptId` *[required] (string) - The scriptId of the resource to be updated.
		 - `scriptText` *[required] (string) - Script text to replace, or add to new version
		 - `version` (string) - By default this will update v0, however you can set this field to update/create an additional version of this scriptId

---
- `get()` Get a single script.


	``` audiostack.Content.Script.get(<args>)```

	- Parameters:
		 - `scriptId` *[required] (string) - 
		 - `preview` *[required] (string) - Preview the effect of applying various text correction processes, normalisation and dictionary.
		 - `voice` *[required] (string) - Which TTS voice should be used to generate the preview, note that this required as different voices require different text correction processes.

---
- `delete()` Deletes a script and all its versions (if applicable).


	``` audiostack.Content.Script.delete(<args>)```

	- Parameters:
		 - `scriptId` *[required] (string) - 

---
- `get()` Get a single version of a script with a given scriptId.


	``` audiostack.Content.Script.get(<args>)```

	- Parameters:
		 - `scriptId` *[required] (string) - 
		 - `version` *[required] (string) - 
		 - `preview` *[required] (string) - Preview the effect of applying various text correction processes, normalisation and dictionary.
		 - `voice` *[required] (string) - Which TTS voice should be used to generate the preview, note that this required as different voices require different text correction processes.

---
- `delete()` Deletes a single version of a script.


	``` audiostack.Content.Script.delete(<args>)```

	- Parameters:
		 - `scriptId` *[required] (string) - 
		 - `version` *[required] (string) - 

---
### `Scripts` resource <a name = "scripts"> </a>
#### Script Management Description

Scripts should be organised into a `projectName/moduleName/scriptName` structure. There are then two methods that are useful for managing content within this structure. These are `/scripts (GET)`, `/scripts (DELETE)`, both of these methods use the same query parameters that allow scripts to either be listed or deleted by given structure. For example, you could list all scripts within a given project, or delete all scripts within a given project and module structure.

---
- `list()` Lists multiple script resources.


	``` audiostack.Content.Scripts.get(<args>)```


	A maximum of 1000 scripts can be returned in a single GET request, a `paginationToken` will be returned that can be passed to the same method again to list the next 1000 scripts.To condense the output JSON, you can supply `verbose=False`, which will remove all of the non-essential details. Leaving only the script directory structure and ID in the response.
	- Parameters:
		 - `projectName` (string) - 
		 - `moduleName` (string) - 
		 - `scriptName` (string) - 
		 - `scriptId` (string) - 
		 - `paginationToken` (string) - 
		 - `verbose` (boolean) - 

---
- `delete()` Deletes multiple script resources.


	``` audiostack.Content.Scripts.delete(<args>)```


	todo
	- Parameters:
		 - `projectName` (string) - 
		 - `moduleName` (string) - 
		 - `scriptName` (string) - 

---
### `List_projects` resource <a name = "list_projects"> </a>

---
- `list()` Lists all projects that have been created.


	``` audiostack.Content.List_projects.get(<args>)```

	- Parameters:
		 - (none) 

---
### `List_modules` resource <a name = "list_modules"> </a>

---
- `list()` Lists all modules that have been created, and lists in which project they exist.


	``` audiostack.Content.List_modules.get(<args>)```

	- Parameters:
		 - `projectPrefix` *[required] (string) - Filter responses by a given projectName

---
### `Voice` resource <a name = "voice"> </a>
#### Product Description
Out voice service manages voices. You can list and filter ones we have created for you, or in turn you can create your own with our voice cloning product.
Library page: https://library.api.audio/.

---
- `list()` List all available voices.


	``` audiostack.Speech.Voice.get(<args>)```


	Todo
	- Parameters:
		 - `limit` (number) - Max. amount of items to be returned
		 - `offset` (number) - Pagination offset. Should be incremented by the value of `itemsLimit` with each request.

		 - `sort` (string) - Sort order of items by an attribute.

		 - `language` (string) - Language of the voice.

		 - `languageCode` (string) - ISO language code of the voice, e.g. en-US

		 - `accent` (string) - Accent of the voice.
		 - `gender` (string) - Gender of the voice.
		 - `ageBracket` (string) - Age bracket of the voice.
		 - `tags` (string) - Tags of the voice. Multiple tags separated by comma are accepted.

		 - `industryExamples` (string) - Multiple tags separated by comma are accepted.

		 - `timePerformance` (string) - Relative response time.

		 - `provider` (string) - Provider of the voice.


---
- `list()` Lists voice parameters.


	``` audiostack.Speech.Voice.get(<args>)```


	Lists all the voice parameters used to describe and filter voices
	- Parameters:
		 - (none) 

---
### `Name` resource <a name = "name"> </a>

---
- `get()` Get data for a single voice.


	``` audiostack.Voice.Name.get(<args>)```

	- Parameters:
		 - `name` *[required] (string) - Alias or original voice ID.

---
### `Sound` resource <a name = "sound"> </a>
#### Product Description

Out sound service manages sound templates. You can list and filter ones we have created for you, or in turn you can create your own.

---
- `create()` Create a sound template resource.


	``` audiostack.Production.Sound.create(<args>)```


	To do
	- Parameters:
		 - `templateName` *[required] (string) - Name of the template
		 - `description` (string) - Description of the template
		 - `isElastic` (boolean) - Elastic templates are currently not available to self-serve customers

---
- `get()` Lists sound templates.


	``` audiostack.Production.Sound.get(<args>)```


	To do
	- Parameters:
		 - `tags` (string) - 
		 - `collections` (string) - 
		 - `type` (string) - 
		 - `genre` (string) - 
		 - `tempo` (string) - 

---
- `update()` Updates sound templates.


	``` audiostack.Production.Sound.update(<args>)```


	To do
	- Parameters:
		 - `templateName` *[required] (string) - Name of the template to update
		 - `description` (string) - Description of the template
		 - `genre` (string) - Update the assigned genre
		 - `tempo` (string) - Update the assigned tempo
		 - `collections` (array) - Update the assigned collections
		 - `tags` (array) - Update the assigned tags

---
- `delete()` Deletes a sound template


	``` audiostack.Production.Sound.delete(<args>)```

	- Parameters:
		 - `name` *[required] (string) - 

---
### `Mix` resource <a name = "mix"> </a>
#### Product Description

Our production endpoints replicate the functionality of a recording studio. Mixing together multiple streams of audio and enhancing these with studio grade effects, such as ducking, de-essing, EQ and compression. You can use our `sectionProperties` argument to arrange sources across a virtual timeline, and align these to fixed markers.


---
- `create()` Creates a mix of multiple audio resources.


	``` audiostack.Production.Mix.create(<args>)```


	todo
	- Parameters:
		 - `speechId` *[required] (string) - Reference to the speechId that is to be mixed with other audio resources
		 - `version` (string) - Specific version of the referenced Script.
		 - `soundTemplate` (string) - Name of the sound template to be mixed with other audio resources
		 - `mediaFiles` (number) - List of media files to be mixed with other audio resources
		 - `forceLength` (float) - Force the output length of the final mix. A value of 0.0 indicates no forced length.
		 - `sectionProperties` (object) - 
todo

		 - `acousticSpace` (string) - Applies an acoustic reverb to the speech track
		 - `masteringPreset` (string) - Mastering preset to use, for example heavyDucking.
		 - `public` (boolean) - Makes returned URLs publicly available

---
- `get()` Retrieve a mixed resource.


	``` audiostack.Production.Mix.get(<args>)```

	- Parameters:
		 - `productionId` *[required] (string) - 

---
- `delete()` Deletes a mixed resource


	``` audiostack.Production.Mix.delete(<args>)```

	- Parameters:
		 - `productionId` *[required] (string) - 

---
- `list()` Lists available encoder presets.


	``` audiostack.Production.Mix.get(<args>)```

	- Parameters:
		 - (none) 

---
### `Mixes` resource <a name = "mixes"> </a>

---
- `list()` Lists multiple mixed resources.


	``` audiostack.Production.Mixes.get(<args>)```


	Returns a list of mixed files that have been created. Can be filtered by `projectName`, `moduleName`, `scriptName` and `scriptId`.
	- Parameters:
		 - `projectName` (string) - 
		 - `moduleName` (string) - 
		 - `scriptName` (string) - 
		 - `scriptId` (string) - 
		 - `paginationToken` (string) - 
		 - `verbose` (boolean) - 

---
### `Encoder` resource <a name = "encoder"> </a>
#### Product Description

Out Delivery endpoints put the finishing touches on your mixed audio assets. Our encoder can be used to convert your file into a different format i.e. `mp3`. Our connector endpoints allow you to publish these assets onwards.


---
- `create()` Changes the audio encoding of a mixed audio file


	``` audiostack.Delivery.Encoder.create(<args>)```


	For most use cases, the preset can be either `custom` or one of the values returned from the `/encoder/presets` list. When using `custom` the other fields can be supplied. Please note not all fields are supported in conjunction with one another. For example `sampleRate` cannot be used in conjunction with `bitRateType`.
	- Parameters:
		 - `productionId` *[required] (string) - Reference to the productionId that is to be encoded
		 - `preset` (string) - named preset to use or 'custom'
		 - `public` (boolean) - Make the output a publicly available URL 
		 - `bitRateType` (string) - Supplied value must be either 'constant' or 'variable
		 - `bitRate` (string) - Can be between 0-9 for variable bit rates, or between 32 and 320 for constant bit rates
		 - `sampleRate` (int) - Sample rate, should be between 24000 and 96000
		 - `format` (string) - Can be wav, mp3, flac or ogg
		 - `bitDepth` (int) - Can be 16, 24, or 32
		 - `channels` (int) - Supply 1 for mono or 2 for stereo
		 - `masteringPreset` (string) - Mastering preset to use, for example heavyDucking.

---
