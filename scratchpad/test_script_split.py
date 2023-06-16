import audiostack
import os
import requests

audiostack.api_base = "https://staging-v2.api.audio"
audiostack.api_key = os.environ["AUDIO_STACK_DEV_KEY"]





text = "Berlin. Leere Gasspeicher, teurer Strom : Deutschland zitterte vergangenes Jahr vor dem bevorstehenden Winter. Die Angst: der wirtschaftliche Abschwung. Selbst das Bundeswirtschaftsministerium warnte noch im November vor einer Rezession. Doch trotz der düsteren Prognosen kam das Land überraschend gut durch die kalten Monate, der große Knall blieb aus. Wie konnte das passieren? Marcel Fratzscher, Präsident des Deutschen Instituts für Wirtschaftsforschung DIW, unterstellt der deutschen Wirtschaft eine bemerkenswerte Resilienz in der Krise. Vor allem die starken Wirtschaftshilfen der Bundesregierung spielen eine entscheidende Rolle. und dass es gelungen ist, Energiesicherheit zu gewährleisten, erklärt er dieser Redaktion auf Nachfrage. Energiesicherheit bringt Deutschland durch den Winter Das sieht auch sein Kollege Torsten Schmidt, Leiter des Kompetenzbereichs Wachstum, Konjunktur und Öffentliche Finanzen am Leibniz-Institut für Wirtschaftsforschung, so. Vor allem konnte eine Gasmangellage in diesem Winter vermieden werden, da viele Unternehmen ihren Gasverbrauch deutlich eingeschränkt haben, erklärt er. Auch die privaten Haushalte hätten durch Einsparungen deutlich daran mitgewirkt, dass die Gasspeicher noch immer gut gefüllt seien. Die Politik habe außerdem zur Stabilisierung der Lage beigetragen, indem sie die Insolvenz der großen Versorgungsunternehmen abgewendet hat. Und: Durch die in diesem Jahr in Kraft getretenen Strom- und Gaspreisbremsen werden die Unternehmen und pri vaten Haushalte spürbar entlastet, so Schmidt. Zwar war die Energiesicherheit auch an gestiegene Kosten gekoppelt, doch die hohen Energiepreise hätten laut Schmidt nur wenige Branchen schwer getroffen. In Ausnahmefällen – etwa im Bereich der chemischen Industrie und der Metallerzeugung und -verarbeitung – konnten Firmen die Kosten nicht ohne weiteres an die Kunden weitergeben. Die Folge: Die Produktion in Deutschland musste reduziert werden. Viele andere Branchen werden von den hohen Energiekosten aber kaum belastet, sagt Schmidt. Zudem können die Unternehmen in einigen Branchen Produktion nachholen, weil sich Lieferengpässe auflösen. Und auch die Chemiebranche stabilisiert sich langsam wieder. Laut Branchenexpertin Anna Wolf vom ifo-Institut blickt die Branche wieder etwas zuversichtlicher in die Zukunft. Die Versorgung mit Vorprodukten habe sich spürbar verbessert, so Wolf. Jedoch bleibe die Nachfrage schwach, der Auftragsbestand sinke und aus dem Export würden keine Impulse erwartet. Bundesregierung ist vorsichtig optimistisch Die Bundesregierung geht in ihrer jüngsten Prognose trotzdem von einem leichten Wirtschaftswachstum in diesem Jahr aus, obwohl das Bruttoinlandsprodukt BIP im letzten Quartal 2022 überraschend um 0,2 Prozent gesunken war. Kommt es im laufenden ersten Vierteljahr 2023 zum zweiten Minus in Folge, sprechen Volkswirte bereits von einer technischen Rezession . Zwar ist es laut der jüngsten Konjunktur-Prognose des ifo-Instituts durchaus möglich, dass das BIP im ersten Quartal nochmals um 0,2 Prozent zurückgehen wird, für das ganze Jahr gehen die Experten aber von einer Erholung aus. Der Gipfel der Inflation ist erreicht, sagt ifo-Konjunkturforscher Timo Wollmershäuser. Sinkende Energiepreise und eine allmähliche Auflösung der Lieferschwierigkeiten in der Industrie seien die Ursachen dafür. Da die Zinsen laut Schmidt aber noch steigen werden und die Inflation erst allmählich zurückgehen dürfte, ist eine schnelle Erholung eher unwahrscheinlich. So sehen es auch die ifo-Experten: Werde die Wirtschaftsleistung 2023 noch in etwa auf der Höhe des Vorjahres verharren, dürfte sie erst im kommenden Jahr kräftiger zulegen – um geschätzte 1,7 Prozent. Der Grund: Für eine Erholungsphase befindet sich Deutschland in einer ungewöhnliche Situation, da die Zinsen in Abschwungphasen üblicherweise gesenkt werden und dann zu Beginn des Aufschwungs niedrig sind. Aber angesichts der hohen Inflation sind der Europäischen Zentralbank die Hände gebunden, erklärt Schmidt. Und sagt: Sie muss die Zinsen noch weiter erhöhen, um ihren Auftrag zu erfüllen. Stabiler Arbeitsmarkt hilft deutscher Wirtschaft Die konjunkturelle Schwäche wird laut ifo-Institut auch die Erholung auf dem Arbeitsmarkt in diesem Jahr etwas verlangsamen. Der Anstieg der Arbeitslosenzahl um knapp 50000 geht vor allem auf geflüchtete Ukrainer zurück, die nun allmählich in den Arbeitsmarkt integriert werden. Bereits im kommenden Jahr dürfte die Arbeitslosenquote wieder auf 5,1 Prozent sinken, nach 5,4 Prozent in diesem und 5,3 Prozent im vergangenen Jahr, schätzen die Wirtschaftsexperten. Sowohl Fratzscher als auch Schmidt heben den stabilen Arbeitsmarkt als einen wichtigen Grund dafür hervor, warum Deutschland zuletzt stabil durch die Krise kam. Der Arbeitsmarkt ist für eine konjunkturelle Schwächephase relativ stabil, so Schmidt. Viele Unternehmen haben bereits vor dem Energiepreisschock unter einem Mangel an Arbeitskräften gelitten. Neueinstellungen wurden nur in geringem Maße reduziert. In dieser Situation sei daher die Sorge der Arbeitnehmer vor einem Arbeitsplatzverlust vergleichsweise gering. Dementsprechend halten sie sich kaum mit Anschaffungen zurück, was wiederum den Konsum stabilisiert, führt Schmidt weiter aus. Und auch die in der Corona -Krise aufgelaufenen Ersparnisse stabilisierten das Konsumverhalten derzeit. Forderung: Jetzt in erneuerbare Energien investieren Fratzscher ergänzt, dass der Arbeitsmarkt und die anhaltend geringe Arbeitslosigkeit zwar ein wichtiger Erfolg für Deutschland seien, der zunehmende Fachkräftemangel bremse jedoch die notwendige wirtschaftliche und ökologische Transformation des Landes. Die wichtigste wirtschaftspolitische Aufgabe für die Bundesregierung wird es sein, bessere Rahmenbedingungen für Unternehmen herzustellen, so Fratzscher. Dazu gehören eine bessere Infrastruktur, weniger Bürokratie und Regulierung und ein Abbau des Fachkräfteproblems. Die große Rezession mag ausgeblieben sein, doch die Experten geben keine Entwarnung. Fratzscher warnt davor, dass eine Eskalation des Krieges in der Ukraine oder der Spannungen zwischen den USA und China die deutsche Wirtschaft empfindlich treffen und in eine Rezession treiben könnten. Und auch die Klimakrise ist laut Schmidt eine Gefahr für die wirtschaftliche Stabilität: Die Politik sollte die aktuelle Energiekrise nutzen, um ihre klimapolitischen Ziele voranzubringen, fordert er. Denn die aktuelle Verteuerung fossiler Energieträger gibt einen starken Anreiz, alternative Energien zu nutzen. Insbesondere müsse in erneuerbare Energien investiert werden.\n"
text = text + text + text + text
print(len(text))


data = f"""
    <as:section> 
        hello {text}
    </as:section>
"""


# scriptText = data

r = requests.post(url="http://localhost:3000/staging/script", json={"scriptText" : data}, headers={"x-api-key" : "1234"})
data = r.json()
scriptId = data["data"]["scriptId"]

# script = audiostack.Content.Script.create(scriptText=data, scriptName="25b")
# print("response from creating script", script.response)
# scriptId = script.scriptId
#scriptId = "7040c9f1-f9cc-4733-a3a1-4b3af27f4470"

#scriptId = "1b6699c9-abb0-4ef6-9c2e-fe90d43edd29"
# print(scriptId)
# # create one tts resource
#audiostack.api_base = "http://localhost:3000/staging"

tts = audiostack.Speech.TTS.create(scriptId=scriptId, voice='lena', useDictionary=True, useTextNormalizer=True)
print(tts.response)


tts2 = audiostack.Speech.TTS.get(speechId=tts.speechId)
print(tts2.response)
# tts.download()
# #print(tts.speechId)

# # now generate several different templates of this

mix = audiostack.Production.Mix.create(speechItem=tts, soundTemplate="vinylhits")
print(mix)
# #mix.download()

encoded = audiostack.Delivery.Encoder.encode_mix(productionItem=mix, preset="mp3")
encoded.download(fileName="final")
