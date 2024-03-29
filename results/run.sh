#!/usr/bin/env bash

set -ex

python ../src/main.py query_year bm32312 -651
python ../src/main.py query_year bm41222 -653
python ../src/main.py query_year bm76738 -646
python ../src/main.py query_year bm35115 -667
python ../src/main.py query_year bm32234 -590
python ../src/main.py query_year bm38462 -603
python ../src/main.py query_year vat4956 -567
python ../src/main.py query_year bm33066 -522

python ../src/main.py query_all bm32312
python ../src/main.py query_all bm41222
python ../src/main.py query_all bm41222 shamash
python ../src/main.py query_all bm41222 kandalanu
python ../src/main.py query_all bm41222 nabopolassar
python ../src/main.py query_all bm76738
python ../src/main.py query_all bm35115
python ../src/main.py query_all bm32234
python ../src/main.py query_all bm38462
python ../src/main.py query_all vat4956
python ../src/main.py query_all vat4956 lunar
python ../src/main.py query_all vat4956 lunar_six
python ../src/main.py query_all vat4956 planet
python ../src/main.py query_all bm33066
python ../src/main.py query_all bm33066 eclipse
python ../src/main.py query_all bm33066 lunar_six
python ../src/main.py query_all bm33066 planet
