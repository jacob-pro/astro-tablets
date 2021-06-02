if cat /proc/version | grep microsoft; then
  CMD="cmd.exe /c"
else
  CMD=
fi

SCRIPT="python ../src/main.py query"
set -e
set -x

$CMD $SCRIPT bm32312 --year -651 --slim > bm32312_scores.txt
$CMD $SCRIPT bm41222 --year -653 --slim > bm41222_scores.txt
$CMD $SCRIPT bm41222 shamash > bm41222_shamash_scores.txt
$CMD $SCRIPT bm41222 kandalanu > bm41222_kandalanu_scores.txt
$CMD $SCRIPT bm41222 nabopolassar > bm41222_nabopolassar_scores.txt
$CMD $SCRIPT bm76738 --year -646 --slim > bm76738_scores.txt
$CMD $SCRIPT bm35115 --year -667 --slim > bm35115_scores.txt
$CMD $SCRIPT bm32234 --year -590 --slim > bm32234_scores.txt

