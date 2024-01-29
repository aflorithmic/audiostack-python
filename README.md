<p align="center">
<a href="https://www.api.audio/" rel="noopener">
 <img src="https://uploads-ssl.webflow.com/60b89b300a9c71a64936aafd/60c1d07f4fd2c92916129788_logoAudio.svg" alt="api.audio logo"></a>
</p>

<h3 align="center">audiostack SDK</h3>

---

<p align="center"> audiostack is the official <a href="https://audiostack.ai/" rel="noopener">audiostack</a> Python 3 SDK. This SDK provides easy access to the api.audio API for applications written in python.
    <br>
</p>

## Maintainers <a name = "maintainers"> </a>

- https://github.com/Sjhunt93

## License <a name = "license"> </a>

This project is licensed under the terms of the MIT license.


## 🧐 About <a name = "about"></a>

This repository is actively maintained by [Audiostack](https://audiostack.ai/). For examples, recipes and api reference see the [api.audio docs](https://docs.audiostack.ai/reference/quick-start). Feel free to get in touch with any questions or feedback!

## :book:  Changelog

You can view [here](https://docs.audiostack.ai/changelog) our updated Changelog.

## :speedboat:  Quickstarts <a name = "quickstarts"></a>

Get started with our [quickstart recipes](https://docs.audiostack.ai/docs/introduction).

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

This library needs to be configured with your account's api-key which is available in your [api.audio Console](https://console.api.audio). Import the audiostack package and set `audiostack.api_key` with the api-key you got from the console:

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

The library needs to be configured with your account's secret key which is available in your [Aflorithmic Dashboard](https://platform.audiostack.ai/). Set `audiostack.api_key` with the api-key you got from the dashboard:

```python
audiostack.api_key = "your-key"
```

### Authentication with environment variable (recommended) <a name = "authentication_env"></a>

You can also authenticate using `audiostack_key` environment variable and the audiostack SDK will automatically use it. To setup, open the terminal and type:

```sh
export audiostack_key=<your-key>
```

If you provide both an environment variable and `audiostack.api_key` authentication value, the `audiostack.api_key` value will be used instead.
