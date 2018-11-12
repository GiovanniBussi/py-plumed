
for file in $(find . -name "Portfile.in")
do
sed "s/__version__/$(git log -1 --format="%h")/g
     s+__root__+$PWD+g" $file > ${file%.in}

done
