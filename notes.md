### Compiling package
```sh
# Test
python setup.py develop
# Compile
python setup.py bdist_wheel
# Upload
python -m twine upload dist/*
# Upgrade
pip install snowctl --upgrade
```

### Dependencies
- tqdm==4.45.0
- twine==3.1.1

### Reading
- [PyPi](https://dzone.com/articles/executable-package-pip-install)

Tässä pari juttua, mitä vielä tarvittaisiin snowctl-ohjelmaan (laitettu prioriteettijärjestyksessä):

Näkymän kopiointi vanhan näkymän päälle (COPY OR REPLACE VIEW…)
Nyt näkymän kopiointi ei onnistu, jos saman niminen näkymä on jo olemassa kohde schemassa.
Uuden näkymän tekeminen PAAKAYTTAJAT-scheman näkymästä
Jos pääkäyttäjät näkymässä on näkymä ”CREATE VIEW VIEW_TEST AS SELECT col1, col2 FROM SEURE_EDW_DEV.PUBLIC.D_ALUE”
Niin uusi, kopioitu näkymä olisi muotoa ”CREATE VIEW SEURE_DM_DEV.ANALYTIIKKA_TESTI.VIEW_TEST AS SELECT col1, col2 FROM SEURE_DM_DEV.PAAKAYTTAJAT.VIEW_TEST”
Mahdollisuus kopioda näkymä eri nimellä toiseen schemaan
Eli luodun näkymän nimen voisi antaa: SEURE_DM_DEV.PAAKAYTTAJAT.VIEW_TEST -> SEURE_DM_DEV.ANALYTIIKKA_TESTI.VIEW_TEST_ANALYTIIKKA (esimerkkinä)