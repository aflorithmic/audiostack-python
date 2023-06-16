from datetime import date

import audiostack
import boto3
import requests
import os

audiostack.api_key = os.environ["AUDIO_STACK_DEV_KEY"]
audiostack.api_base = "https://staging-v2.api.audio"# metadata

today = date.today().strftime("%b-%d-%Y")
news_product_name = "gateway-timeout"

# speech related
today_speech = date.today().strftime("%d %B %Y")

# Let's create a script!
_01 = """
    Heute ist der siebzehnte November 2022.
"""

_02 = """
    'Verhandlungen zu Haustarif bei VW\n' +
    '\n' +
    '\n' +
    'Die IG Metall und das Management von Volkswagen setzen heute Vormittag ihre Gespräche über einen neuen Haustarif für die Beschäftigten des Automobilherstellers fort. Unmittelbar vor der zweiten Runde wollen sich IG-Metall-Mitglieder zu einer Kundgebung vor der Volkswagen-Arena in Wolfsburg treffen. Die Gewerkschaft fordert unter anderem acht Prozent mehr Lohn.\n' +
    '\n' +
    '\n' +
    '\n' +
    'Wasserstoff-Studie\n' +
    '\n' +
    '\n' +
    'E.ON stellt heute in Berlin eine neue Studie zum Zustand der Wasserstoffwirtschaft in Deutschland vor. Hintergrund ist das Ziel der Bundesregierung, den Ausbau des Wasserstoffsegments möglichst schnell voranzutreiben. In der Studie geht es um die aktuellen Rahmenbedingungen und Zukunftsperspektiven.\n' +
    '\n' +
    '\n' +
    '\n' +
    'Gedenkveranstaltungen\n' +
    '\n' +
    '\n' +
    'In Berlin und anderen Städten finden heute Veranstaltungen zum Gedenken an die Novemberpogrome vor 84 Jahren statt. Zudem jährt sich heute der Tag des Mauerfalls zum 33. Mal.\n' +
    '\n'
"""

_03 = """
    'Top-Personalien sorgen für Aufmerksamkeit\n' +
    '\n' +
    '\n' +
    'Mit Nelly Kennedy übernimmt bei Volkswagen Pkw eine Digitalexpertin die Führungsposition im internationalen Marketing. Kennedy, die zuletzt das globale Brähnd Marketing von Google verantwortete, folgt ab Mitte Februar 2023 auf Jochen Sengpiehl, der zur Volkswagen Group China wechselt. Thomas Schäfer, Chef der Marke Volkswagen Pkw, sagte: “Wir machen die Marke Volkswagen wieder zur Laf Bränd nahbar, kundenfokussiert und authentisch.” Eine andere Top-Personalie, nämlich der Eintritt der Grünen-Politikerin Julia Willi Hamburg in den Aufsichtsrat des VW-Konzerns, wird kontroverser bewertet. Denn Hamburg tritt den Posten nicht als Wirtschafts-, sondern als Kultusministerin an. Die mangelnde fachliche Nähe sorgte für Verwunderung und kritische Einlassungen. \n' +
    '\n' +
    '\n' +
    '\n' +
    'ID.4 meistert Dauertest mit Bravour\n' +
    '\n' +
    '\n' +
    'Der Dauertest des VW-Elektro-SUVs ID.4 lief über ein Jahr und mehr als 20.000 Kilometer. Am Ende fiel das Urteil der Experten des österreichischen Automobilclubs Ö A M T C beinahe euphorisch aus: “Der ID.4 ist ein richtig gutes Reiseauto.” Die Tester bemängelten lediglich, dass die Parksensoren wegen der massiven Kennzeichenhalterungen offenbar “grundlos” piepten. Auch von YouTubern in den USA und Australien wird der ID.4 rundum positiv bewertet. “Man bekommt am meisten für sein Geld”, heißt es etwa im Video von Out of Sspec Reviews. \n' +
    '\n'
"""

_04 = """
    'Erstens. China steigert Pkw-Verkäufe\n' +
    '\n' +
    '\n' +
    'Im Oktober wurden in China im Vergleich zum Vorjahr 7,3 Prozent mehr Fahrzeuge an Endkunden verkauft. In den Vormonaten lagen die Wachstumsraten bei bis zu 20 Prozent. Die Einzelhandelsverkäufe für Elektroautos stiegen im Oktober um 75 Prozent. Spitzenreiter war der Konzern Bi Vai Di, der mehr Fahrzeuge auslieferte als Tesla. Wie der Branchenverband PCA mitteilte, stiegen die Verkäufe im Großhandel währenddessen um 11 Prozent. Der Export lag im Oktober bei 270.000 Einheiten, ein Plus von 42 Prozent. Wesentlich zum Wachstum des chinesischen Pkw-Marktes habe die Entscheidung der chinesischen Regierung beigetragen, die Kfz-Steuer zu senken. \n' +
    '\n' +
    '\n' +
    'Zweitens. Musk Tesla-Aktien\n' +
    '\n' +
    '\n' +
    'US-Unternehmer Elon Musk hat nach der teuren Twitter-Übernahme erneut Tesla-Aktien im Wert von rund vier Milliarden Dollar verkauft. Das geht aus Informationen der Börsenaufsicht S E C hervor. Der Tesla-Chef gilt als einer der reichsten Menschen der Welt. Er hatte Twitter für rund 44 Milliarden Dollar übernommen. In diesem Jahr verkaufte er bereits Tesla-Aktien im Wert von 15,5 Milliarden Dollar. Twitter schreibt Musk zufolge rund vier Millionen Dollar Verlust pro Tag. Zuletzt brachen die Werbeerlöse ein, da große Unternehmen wie Volkswagen und der Pharmakonzern Pfizer ihre Anzeigen beim Online-Dienst auf Eis legten.  \n' +
    '\n' +
    '\n' +
    '\n' +
    'Drittens. Stand der US-Wahlen - Trump ruft zu Protesten auf\n' +
    '\n' +
    '\n' +
    'Bei den Zwischenwahlen in den USA ist nach der Schließung der Wahllokale in zahlreichen Bundesstaaten weiter offen, welche Partei künftig im US-Kongress das Sagen haben wird. Ein zuletzt vorhergesagter überwältigender Sieg der Republikaner zeichnete sich aber bis zum späten Dienstagabend (Ortszeit) nicht ab. Erste Prognosen zeigen, dass sich die Demokraten zunächst besser behaupten als angenommen. Die zur Wahl stehenden Senatssitze in Colorado, Connecticut und New Hampshire haben die Republikaner nach derzeitigem Stand jedenfalls nicht gewonnen. Am frühen Morgen (Stand 08:35 Uhr MEZ) lagen die Demokraten im Repräsentantenhaus bei 173 Sitzen, die Republikaner bei 198 . Im Senat stand es 48 zu 47 . Der ehemalige US-Präsident Donald Trump sprach bereits während der Wahl über angebliche Unregelmäßigkeiten bei der Stimmabgabe und rief zu Protesten auf. \n'
"""

_05 = """
    'Erstens. VW ernennt Nelly Kennedy zur neuen Marketingleiterin erschienen in W und V am 09.11.2022\n' +
    '\n' +
    '\n' +
    '\n' +
    'Zweitens. WAZ-Autopilot - Musterschüler Trinity erschienen in WAZ online am 09.11.2022'
"""

_06 = """
    'Nelly Kennedy wird Volkswagen Marketingchefin\n' +
    '\n' +
    '\n' +
    'Die Digitalexpertin Nelly Kennedy übernimmt ab Mitte Februar 2023 die Leitung des internationalen Marketings von Volkswagen. Sie folgt auf Jochen Sengpiehl, der zur Volkswagen Group China gewechselt ist. Kennedy verfügt über 30 Jahre Erfahrung im Brand Marketing, zuletzt als Senior Global Director im Brand Marketing von Google. Thomas Schäfer, Chef der Marke Volkswagen Pkw, sagte: “Wir machen die Marke Volkswagen wieder zur Love Brand – nahbar, kundenfokussiert und authentisch.” Das Marketing spiele dabei eine große Rolle. Marketing-Vorständin Imelda Labbé ergänzte, mit Kennedy werde Volkswagen die Neuausrichtung der Marke und Marketingaktivitäten konsequent vorantreiben. \n' +
    '\n' +
    '\n' +
    '\n' +
    'Bürgerdialog zur Trinity-Fabrik: Zeitplan bleibt\n' +
    '\n' +
    '\n' +
    'Rund 200 Besucher kamen am Montag zum Bürgerdialog über die Gigafactory in Wolfsburg- Warmenau, um sich über den Stand der Planungen zu informieren. Zuletzt hatte es wegen der geplatzten Verhandlungen über zwei Grundstücke Zweifel an der termingerechten Durchführung des Baus gegeben. Nun stellte Trinity-Sprecher Christian Schiebold klar, dass sich nur die Planungs- und Genehmigungsphase sowie vorbereitende Arbeiten verschieben, an den Meilensteinen für den Fabrikbau jedoch festgehalten werde. Mitte 2026 sollen die ersten Trinity-Limousinen vom Band rollen. Bei der Veranstaltung konnten sich die Bürger anhand von Modellen und Animationen rund um die Themen Fabrikmodell, Lieferantenpark, Standortentwicklung, Bebauungsplan, Mobilität und Umwelt informieren. \n' +
    '\n' +
    'VW ID.4 im Dauertest\n' +
    '\n' +
    '\n' +
    'Der ÖAMTC hat den VW ID.4 ein Jahr lang “in der Hitze, in der Kälte, voll beladen, auf flotten Autobahnetappen und sogar im Anhängerbetrieb” getestet. Nach mehr als 20.000 Kilometern lobten die Experten des österreichischen Automobil- und Reiseclubs vor allem Geräumigkeit, Fahrwerk und Reisekomfort des Elektro-SUV. Probleme gab es einzig mit “grundlosem” Parksensoren-Alarm aufgrund zu massiver Kennzeichenhalterungen. Die ermittelten Verbrauchsdaten variierten erheblich zwischen 17 und 30 kWh je 100 Kilometer. Je nach Außentemperatur und Einsatzzweck (Zugbetrieb) lag die Reichweite im Test damit zwischen 240 und mehr als 500 Kilometern. Fazit: “Der ID.4 ist ein richtig gutes Reiseauto.” \n'
"""

_07 = """
    'Vergleich: Skoda Räpid Spaceback und Hyundai i30\n' +
    '\n' +
    '\n' +
    'Die Auto Zeitung hat zwei beliebte Rivalen des VW Golf auf dem Gebrauchtwagenmarkt gegenübergestellt: den Skoda Räpid Spaceback und den Hyundai i30. Dabei sah die Zeitung den Koreaner in Sachen Fahrkomfort und Antriebsauswahl vorne, bezeichneten aber auch den Škoda als gute Alternative in der Kompaktklasse. Insgesamt habe der Hyundai i30 die modernere Sicherheitsausstattung und sei das ausgereiftere Auto, der Škoda hingegen werde gebraucht günstiger gehandelt, so das Fazit der Autoren.\n' +
    '\n'
"""

_08 = """
    'Kritische Stimmen zu Julia Hamburg im VW-Aufsichtsrat\n' +
    '\n' +
    '\n' +
    'Julia Willie Hamburg (Grüne) sitzt künftig neben Niedersachsens Ministerpräsident Stephan Weil (SPD) im Aufsichtsrat des VW-Konzerns. Diese Personalie sorgt für Kritik. Denn anders als ihre Vorgänger kommt die Grünen-Politikerin nicht aus dem Wirtschaftsressort, sondern ist als Kultusministerin für Schulen und Bildung zuständig. Die mangelnde fachliche Nähe sorgte bereits im Vorfeld für Verwunderung. Kritiker bemängelten die Entscheidung als parteipolitisch motiviert. In Europas größtem Autokonzern ist das Land Niedersachsen der zweitmächtigste Aktionär. Die Grünen hatten als Oppositionsfraktion im Landtag mehrfach kritische Anfragen zur Rolle Volkswagens in China gestellt.\n' +
    '\n' +
    '\n' +
    '\n' +
    'Blume offizieller VfL-Wolfsburg-Fan\n' +
    '\n' +
    '\n' +
    'Er ist zwar bekennender Fan von Eintracht Braunschweig, doch nun trat VW-Chef Oliver Blume auch dem Fanclub des VfL Wolfsburg bei. Vor dem Bundesligaspiel gegen Borussia Dortmund, das mit einem 2:0 Heimsieg endete, unterzeichnete er auf der Fanmeile zusammen mit VW-Markenchef Thomas Schäfer die Mitgliedschaft. “Ich werde so oft wie möglich live im Stadion sein, um unsere Wölfe anzufeuern”, ließ der gebürtige Braunschweiger über die Zeitschrift Kicker verlauten. VW werde auch unter seiner Führung das VfL-Engagement aufrechterhalten, betonte der Konzernchef. “Das Sportengagement ist ein wichtiges Fundament für ein nachhaltiges Miteinander in der Gesellschaft. Diese Verantwortung nehmen wir gerne wahr.”\n' +
    '\n' +
    '\n' +
    'Dieselprozess\n' +
    '\n' +
    '\n' +
    'Am 53. Verhandlungstag im Abgasprozess gegen Volkswagen konnte auch ein neuer Zeuge wenig Erhellendes beitragen. Der 47-jährige Entwicklungsingenieur arbeitete zunächst beim Zulieferer IAV und seit 2011 bei VW in der Abteilung, die den Auftrag für die “spezielle Funktionstechnik” erteilte, die letztlich zu “Dieselgate” führte. Der Zeuge wurde rund fünf Stunden lang vernommen. Dabei räumte der Entwicklungsingenieur zwar ein, bereits zu seiner Zeit bei IAV mit dem Thema der Manipulation von Akustik-Software im Dieselmotor in Berührung gekommen zu sein und dabei ein “Störgefühl” gehabt zu haben. An entscheidende Details seiner Arbeit konnte er sich jedoch nicht mehr erinnern. \n' +
    '\n' +
    '\n' +
    'Porsche SE erwartet Schulden\n' +
    '\n' +
    '\n' +
    'Die Volkswagen-Dachholding Porsche SE rechnet durch den Erwerb von Stammaktien der VW-Tochter Porsche AG zum Jahresende mit einem Schuldenberg: Die Netto-Liquidität werde auf minus 6,4 Milliarden bis minus 6,9 Milliarden Euro sinken, erklärte der Stuttgarter Dax-Konzern. Anfang Oktober wurde bereits die erste Tranche von 17,5 Prozent der Stammaktien für 7,1 Milliarden Euro gekauft. Eine zweite Tranche von 7,5 Prozent soll Anfang 2023 erworben und über eine Sonderdividende finanziert werden. Der Gewinn der Porsche SE stieg in den ersten neun Monaten dieses Jahres um 22 Prozent auf 4 Milliarden Euro. \n' +
    '\n'
"""

_09 = """
    'Rückrufe bei Tesla\n' +
    '\n' +
    '\n' +
    'Tesla hat freiwillig 40.168 Fahrzeuge der Baureihen Model S und Model X (2017 bis 2021) zurückgerufen, bei denen es zu einem Ausfall der Servolenkung kommen kann. Dies geht aus einem am Dienstag veröffentlichten Antrag bei der National Highway Traffic Safety Administration vom 1. November hervor. Eine verringerte oder verlorene Servolenkung beeinträchtigt nicht die Lenkkontrolle, kann aber einen höheren Lenkaufwand des Fahrers erfordern, insbesondere bei niedrigen Geschwindigkeiten, so die Behörde. Laut Tesla hätten inzwischen 97 Prozent der Fahrzeuge ein Software-Update per Funk erhalten, das den Fehler behebt.\n' +
    '\n'
"""

_10 = """
    'Deutsche Umwelthilfe darf klagen\n' +
    '\n' +
    '\n' +
    'Die Deutsche Umwelthilfe darf weiter gegen unzulässige Thermofenster klagen. Der Europäische Gerichtshof (EuGH) hat dem Verein in der Frage Recht gegeben, ob gemeinnützige Umweltorganisationen gegen Behördenentscheidungen auf die Einhaltung von Umweltstandards klagen dürfen. Nach deutschem Recht konnten solche Organisationen bislang nicht geltend machen, dass sie besonders betroffen sind. Im konkreten Fall ging es um eine Klage gegen einen Bescheid des Kraftfahrt-Bundesamtes, der einen VW-Typ mit einem der bemängelten Thermofenster genehmigt hatte. Offen ließ der EuGH jedoch den entscheidenden Punkt, ob die Autokäufer in dem Fall gegenüber den Herstellern einen Anspruch auf Schadenersatz haben. Der deutsche Bundesgerichtshof hat dies bislang zurückgewiesen.\n' +
    '\n' +
    '\n' +
    '\n' +
    'Bosch einigt sich auf Millionenzahlung\n' +
    '\n' +
    '\n' +
    'Der deutsche Autozulieferer Bosch hat sich im Zuge der globalen Abgasproblematik mit dem US-Bundesstaat Kalifornien auf eine Zahlung von 25 Millionen US-Dollar geeinigt. Mit der Zahlung werden laut dem kalifornischen Generalstaatsanwalt Rob Bonta Vorwürfe beigelegt, denen zufolge der Konzern in die Krise verstrickt war. Bosch war vorgeworfen worden, mehreren Autoherstellern Komponenten, Software und Programmierleistungen zur Verfügung gestellt zu haben, obwohl dem Unternehmen bekannt war, dass diese Umwelt- und Verbraucherschutzgesetze verletzten. Bosch erkenne die Richtigkeit der Vorwürfe nicht an und übernehme keinerlei Haftung. Die Vereinbarung muss noch von einem Gericht genehmigt werden.\n' +
    '\n' +
    '\n' +
    '\n' +
    'Habeck gegen Elmos-Verkauf\n' +
    '\n' +
    '\n' +
    'Die Bundesregierung will den Einfluss Chinas auf sensible Bereiche der deutschen Infrastruktur begrenzen. Wirtschaftsminister Robert Habeck hat sich dafür ausgesprochen, den Verkauf einer Chipfertigung der Firma Elmos in Dortmund an chinesische Investoren zu untersagen. Der Deal würde die “öffentliche Ordnung und Sicherheit Deutschlands” gefährden. Das Kabinett wird das Verbot voraussichtlich heute beschließen. Zuletzt hatte die Beteiligung des chinesischen Konzerns Cosco von 24,9 Prozent an einem Hamburger Hafenterminal für Kontroversen gesorgt. Bundeskanzler Olaf Scholz setzte das Geschäft aber durch. Die Bundesregierung will im kommenden Jahr eine neue China-Strategie vorlegen, die restriktiver ausfallen könnte, als der Kurs vorheriger Regierungen. \n' +
    '\n' +
    '\n' +
    '\n' +
    'Investitionsstrategie von Katar\n' +
    '\n' +
    '\n' +
    'Volkswagen, Siemens, Deutsche Bank, Hochtief, Hapag-Lloyd, RWE: Das Emirat Katar ist an zahlreichen deutschen Großkonzernen beteiligt und besetzt dort wichtige Posten. Bisher trete Katar als Finanzinvestor auf. Es sei aber nicht ausgeschlossen, dass der Golfstaat eines Tages seinen Einfluss für eigene Interessen nutzt, sagte Rolf Langhammer vom Kieler Institut für Weltwirtschaft. Das Emirat steht wegen Menschenrechtsverletzungen in der Kritik. Deutsche Unternehmen, an denen es beteiligt ist, profitieren allerdings von lukrativen Aufträgen. Katar versuche einerseits, den ökologischen Wandel im Westen hinauszuzögern, um fossile Energieträger wie LNG zu verkaufen, andererseits investiere das Emirat in erneuerbare Energien für künftigen Wohlstand.\n'
"""

text = """
	<as:section name="_01">
    {}
    </as:section>
	<as:section name="_02">
    {}
    </as:section>
	<as:section name="_03">
    {}
    </as:section>
	<as:section name="_04">
	{}
	</as:section>
	<as:section name="_05">
	{}
	</as:section>
	<as:section name="_06">
	{}
	</as:section>
	<as:section name="_07">
	{}
	</as:section>
	<as:section name="_08">
	{}
	</as:section>
	<as:section name="_09">
	{}
	</as:section>
	<as:section name="_10">
	{}
	</as:section>
""".format(_01,
           _02,
           _03,
           _04,
           _05,
           _06,
           _07,
           _08,
           _09,
           _10)

script_text = audiostack.Content.Script.create(scriptText=text, scriptName='{}'.format(news_product_name))
print(script_text)
# Create text to speech !
speech = audiostack.Speech.TTS.create(
    scriptItem=script_text, useDictionary=True,
    sections={
        "_01": {"voice": "joanna", "speed": 95},
        "_02": {"voice": "joanna", "speed": 98},
        "_03": {"voice": "joanna", "speed": 95},
        "_04": {"voice": "joanna", "speed": 98},
        "_05": {"voice": "joanna", "speed": 95},
        "_06": {"voice": "joanna", "speed": 98},
        "_07": {"voice": "joanna", "speed": 95},
        "_08": {"voice": "joanna", "speed": 98},
        "_09": {"voice": "joanna", "speed": 95},
        "_10": {"voice": "joanna", "speed": 98},
    },
)
print(speech)
#Mastering creation

mastering = audiostack.Production.Mix.create(
    #speechItem=speech,
    speechId="ded3a133f136f25512fee6e408774b25",
    public=True
)

# Check the response
print('Response from mastering', mastering)

# Download file
files = mastering.data["files"][0]
r = requests.get(files["url"], allow_redirects=True)
file_name = '{}-{}.wav'.format(news_product_name, today)
open('outputs/{}'.format(file_name), 'wb').write(r.content)

# Upload file
# s3_client = boto3.client('s3')
# response = s3_client.upload_file('outputs/{}'.format(file_name), "hype1000", file_name,
#                                  ExtraArgs={'ContentType': "audio/mpeg", 'ContentDisposition': "inline"})
# # print("#############################")
# # print('Successfully uploaded file: https://hype1000.s3.eu-central-1.amazonaws.com/{}'.format(file_name))
