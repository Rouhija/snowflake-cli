# Snowflake cli-työkalu
Tämä työkalu on tarkoitettu eräiden toimintojen automatisoimiseen Snowflakessa. Pääkäyttötarkoitus on helpottaa näkymien kopiointia skeemojen ja databasejen välillä.

## Asennusohjeet
Snowctl on Python3:lla kirjoitettu työkalu. Asennusta varten on python3 (versiot 3.6 - 3.9) oltava asennettuna koneelle, sekä Pythonin pip-pakettien asennus työkalu. Pip työkalu asentuu näiden asennuksien mukana automaattisesti. 
- [Windows asennus](https://www.python.org/downloads/release/python-385/)
- [Linux asennus](https://docs.python-guide.org/starting/install3/linux/)

Asennuksen jälkeen voit testata esim. Powershellistä, että tarvittavat ohjelmat ovat koneella.
python --version
pip --version

Tämän jälkeen voi itse snowctl:n asentaa seuraavalla komennolla
pip install snowctl

## Käyttöohjeet
Snowctl käynnistetään komentoikkunasta seuraavasti. Näin käynnistyy snowctl oma komentoikkuna. Ensimmäisellä kerralla ohjelma kysyy snowflake kredentiaaleja, tilin urlin yms.
```sh
snowctl
```

Ohjelmaa voi myös ajaa alla olevilla flageilla
```
usage: snowctl [-h] [-d] [-s] [-c] [-e]

optional arguments:
  -h, --help           näytä tämä apuviesti ja poistu
  -d, --debug          näytä debug-lokit konsolissa
  -s, --safe           kysy varmistusta ennen uusien näkymien luontia
  -c, --configuration  syötä uudelleen konfiguraation arvot
  -e, --echo           näytä nykyinen konfiguraatio
  -v, --version        näytä snowctl versionumero
```

Komennot snowctl konsolissa ovat seuraavat:
        use <database|schema|warehouse> <name>
            - vaihda databasea, skeemaa tai warehousea
        copy views
            - Kopioi näkymiä skeemojen tai databasejen välillä
        copy views filter
            - Kopioi näkymiä skeemojen tai databasejen välillä ja valitse, mitkä kolumnit jäävät pois
        list views <filter>
            - Näytä näkymät nykyisessä ympäristössä, voit filtteröidä hakutuloksia tekstin perusteella
        peek <view>
            - Näytä ensimmäinen datarivi näkymästä / taulusta
        sql <query>
            - Suorita vapaamuotoinen sql kysely
        exit/ctrl+C
            - Poistu snowctl konsolista