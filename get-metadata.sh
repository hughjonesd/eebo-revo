
batchsize=20

for zipfile in $(ls data-raw/eebo-zips/*.zip); do
  ((i=i%batchsize)); ((i++==0)) && wait
  zipname=$(basename $zipfile)
  # grep xml removes the directory entries e.g. "B36.zip B36/"
  zipinfo -1 $zipfile | sed -e "s/^/$zipname\t/" | grep xml | python3 get-metadata.py &
done

wait