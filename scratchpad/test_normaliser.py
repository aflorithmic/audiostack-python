import audiostack
import os

audiostack.api_base = "https://staging-v2.api.audio"

audiostack.api_key = os.environ["AUDIO_STACK_DEV_KEY"]

scriptText = """
"Die Volkshochschule in Hermsdorf bietet wieder Kurse für alle an, die den Umgang mit Laptops und Smartphones besser üben möchten. Die Digitalisierung ist mittlerweile fester Bestandteil in vielen Bereichen des Lebens und der Umgang mit digitalen Medien wird immer mehr zur Notwendigkeit im Alltag für alle Bürger. Die Kurse für den Umgang mit Smartphones und Laptops finden in der Volkshochschule bereits seit über vier Jahren statt und kommen im Großen und Ganzen gut an. Da der Einstieg in die digitale Welt oftmals nicht so einfach ist, besteht ein Kurs aus maximal sieben Teilnehmern, damit individuelle Probleme und Schwierigkeiten besser gemeinsam bearbeitet werden können. Für die zwei unterschiedlichen Kurse stehen zwei Dozenten zur Verfügung. Vorwissen ist nicht von Nöten, alles kann vor Ort im Kurs besprochen und gemeinsam geübt werden. Leiterin der Kreisvolkshochschule Hermsdorf Ines Beese möchte alle ermutigen, die Interesse an dem Thema haben, zu kommen und sich auszuprobieren. Im Gespräch mit der Redaktion erklärt sie auch, dass die Kurse an der Kreisvolkshochschule nicht nur reine Lehrveranstaltungen sind, sondern auch in gewisser Weiser ein sozialer Treffpunkt, wo die Teilnehmer auch mal gemeinsam einen Kaffee trinken und sich austauschen. Der Seniorenbeirat begrüßt die Angebote Für die Smartphone-Kurse muss jeder Teilnehmer ein eigenes Smartphone mitbringen. Die Marke spiele dabei keine Rolle, der Dozent helfe bei jedem Modell weiter. Bei den Laptop-Kursen können zunächst auch erstmal die Geräte der Kreisvolkshochschule genutzt werden. Hier ist kein eigener Laptop zwingend erforderlich, um am Kurs teilnehmen zu können. Auch wenn sich der Kurs explizit an alle Menschen jeden Alters richten, so sind es oftmals eher die älteren, die selbst nicht mit digitalen Medien aufgewachsen sind, die den Kurs besuchen. Für die kommenden Termine fehlt es aber aktuell noch an Interessenten. Runa Hüttner vom Seniorenbeirat Eisenberg merkt an, dass der Seniorenbeirat dieses Angebot begrüßt. Ein ähnliches Angebot gab es bereits in Zusammenarbeit mit Schülern, welches aber aufgrund der Altersdiskrepanz weniger funktionierte. Mit einem geschulten Dozenten im Rahmen des Volkshochschulkurses erhofft sich der Seniorenbeirat eine bessere Vermittlung von Medienkompetenz. Der Kurs Smartphone für Einsteiger findet wöchentlich ab dem 28. Februar 2023 um 9:15 Uhr statt. Der Kurs Laptop  PC für Fortgeschrittene findet wöchentlich ab dem 01. März 2023 um 14:00 Uhr statt. Der Kurs Laptop  PC für Einsteiger findet wöchentlich ab 01. März 2023 um 17:00 Uhr statt. In der Geschäftsstelle Mozartstraße in Eisenberg findet der Kurs Smartphone für Einsteiger wöchentlich ab 02. März 2023 um 9:15 Uhr statt."
"""

script = audiostack.Content.Script.create(scriptText=scriptText)
print("response from creating script", script.response)
scriptId = script.scriptId

# create one tts resource
tts = audiostack.Speech.TTS.create(scriptItem=script, voice="klaus", useDictionary=True, useTextNormalizer=True)
print(tts.speechId)

# now generate several different templates of this

mix = audiostack.Production.Mix.create(speechItem=tts, soundTemplate="vinylhits")
print(mix)


encoded = audiostack.Delivery.Encoder.encode_mix(productionItem=mix, preset="mp3")
encoded.download(fileName="final")
