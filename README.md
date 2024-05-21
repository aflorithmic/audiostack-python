<p align="center">
<a href="https://www.api.audio/" rel="noopener">
 <img src="https://uploads-ssl.webflow.com/60b89b300a9c71a64936aafd/60c1d07f4fd2c92916129788_logoAudio.svg" alt="api.audio logo"></a>
</p>

<h3 align="center">Audiostack SDK</h3>

---

<p align="center"> This is the official <a href="https://audiostack.ai/" rel="noopener">audiostack</a> Python 3 SDK. This SDK provides easy access to the Audiostack API for applications written in Python.
    <br>
</p>

## 🧐 About <a name = "about"></a>

This repository is actively maintained by [Audiostack](https://audiostack.ai/). For examples, recipes and api reference see the [api.audio docs](https://docs.audiostack.ai/reference/quick-start). Feel free to get in touch with any questions or feedback!

## :book:  Changelog

You can view [here](https://docs.audiostack.ai/changelog) our updated Changelog.

## 🏁 Getting Started <a name = "getting_started"></a>

### Installation

You don't need this source code unless you want to modify it. If you want to use the package, just run:

```sh
pip install audiostack -U
```

### Prerequisites <a name = "requirements"></a>

Python `^3.8.1`

### Authentication

This library needs to be configured with your account's API key which is available in your [Audiostack platform](https://platform.audiostack.ai/audiostackapi). Import the audiostack package and set `audiostack.api_key` with the API key you got from the console:

```python
import audiostack
audiostack.api_key = "your-key"
```

If you belong to multiple organizations, by default the API will use the first organization you had access to. You can specify the organization by setting the `assume_org_id` attribute:

```python
audiostack.assume_org_id = "your-org-id"

```

### Create your first audio asset

#### ✍️ First, create a Script.

Audiostack Scripts are the first step in creating audio assets. Not only do they contain the text to be spoken, but also determine the final structure of our audio asset using the [Script Syntax](https://docs.audiostack.ai/docs/script-syntax).

It also supports a [unified SSML syntax](https://docs.audiostack.ai/docs/ssml-tags), which is a standard way to control speech synthesis.

```python
script = audiostack.Content.Script.create(scriptText="""
<as:section name="intro" soundsegment="intro">
Hey there, <as:placeholder id="username">friend</as:placeholder>! Welcome to Audiostack - the audio creation platform that allows you to create high quality audio assets using just a few lines of code.
</as:section>
<as:section name="main" soundsegment="main">
Whether it's a podcast, a video, a game, or an app, Audiostack has you covered. You can create voiceovers, sound effects, music, and more.
</as:section>
<as:section name="outro" soundsegment="outro">
We are excited to see what you'll create with our product!
</as:section>
""")
```

#### 🎤 Now, let's read it out load. 

We integrate all the major TTS voices in the market. You can browse them in our [voice library](https://library.audiostack.ai/).

Let's use the voice "Isaac", substitute the `username` placeholder with `mate` and download the produced files. Each section results in a seperate audio file.

```python
tts = audiostack.Speech.TTS.create(scriptItem=script, voice="isaac", audience={"username": "mate"})
tts.download(fileName="example")
```

When you listen to these files, you'll notice each of them has a certain silence padding at the end. This might be useful for some use cases, but for this example, let's remove it.

```python
tts = audiostack.Speech.TTS.remove_padding(speechId=tts.speechId)
```

#### 🎛️ Now let's mix the speech we just created with a [sound template](https://library.audiostack.ai/sound).

```python
mix = audiostack.Production.Mix.create(speechItem=tts, soundTemplate="chill_vibes")
```

Various sound templates consist of various segments. In our example, we're using three segments: intro, main and outro. 

You can list all the sound templates to see what segments are available or even [create your own](https://docs.audiostack.ai/docs/custom-sound-design-templates)!

Mixing comes with a lot of options to tune your audio to sound just right. 
[More on this here.](https://docs.audiostack.ai/docs/advance-timing-parameters)

#### 🎧 At this point, we can download the mix as a wave file, or convert it to another format.

```python
enc = audiostack.Delivery.Encoder.encode_mix(productionItem=mix, preset="mp3_high")
enc.download(fileName="example")
```

Easy right? 🔮 This is the final result:

https://github.com/aflorithmic/audiostack-python/assets/64603095/6948cddb-4132-40a7-b84d-457f3fc0803d

## :speedboat: More quickstarts <a name = "quickstarts"></a>

Get started with our [quickstart recipes](https://docs.audiostack.ai/docs/introduction).

## Maintainers <a name = "maintainers"> </a>

- https://github.com/Sjhunt93

## License <a name = "license"> </a>

This project is licensed under the terms of the MIT license.

