#!/usr/bin/env bash

set -ex

python ../src/cli.py query bm32312 --year -651 --slim > bm32312_scores.txt
python ../src/cli.py query bm41222 --year -653 --slim > bm41222_scores.txt
python ../src/cli.py query bm41222 shamash > bm41222_shamash_scores.txt
python ../src/cli.py query bm41222 kandalanu > bm41222_kandalanu_scores.txt
python ../src/cli.py query bm41222 nabopolassar > bm41222_nabopolassar_scores.txt
python ../src/cli.py query bm76738 --year -646 --slim > bm76738_scores.txt
python ../src/cli.py query bm35115 --year -667 --slim > bm35115_scores.txt
python ../src/cli.py query bm32234 --year -590 --slim > bm32234_scores.txt
python ../src/cli.py query bm38462 --year -603 --slim > bm38462_scores.txt
python ../src/cli.py query vat4956 --year -567 --slim > vat4956_scores.txt
python ../src/cli.py query bm33066 --year -522 --slim > bm33066_scores.txt
python ../src/cli.py query bm33066 eclipse_only > bm33066_eclipse_scores.txt
python ../src/cli.py query bm33066 lunar_six_only > bm33066_lunar6_scores.txt
python ../src/cli.py query bm33066 planet_only > bm33066_planet_scores.txt
