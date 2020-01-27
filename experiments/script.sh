
for letter in {A,B,C,D,E,F,G}
do
  mkdir mode_$letter

  for i in {00..49}
  do
    mkdir mode_$letter/map_$i
    mv *mode_$letter\_map_$i\_* mode_$letter/map_$i
    mv *mode_$letter\_exec* mode_$letter
  done
done
