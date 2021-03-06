#!/bin/sh

# if this doesn't work, go to https://www.dropbox.com/sh/pfx619wnjdck2lj/AAAeQjd_dv29oPymNoKJWfEYa?dl=0
# and get the download link from there

eebo_zips_url="https://ucd02cc615acf8e7f1719d158a3e.dl.dropboxusercontent.com/zip_download_get/BBU2AXBLG_dQjthH_rC07-XRE_I1PXOCjURD28nbkuwjprvfE3v_pqFOUex9SUAhhrm-cmj0YBq-cJYlAm2UjIjtuTEPxlwWYJHo9NQmujvkqQ?_download_id=1461240365575096507288853614259105910800945992200607443741746527044&_notify_domain=www.dropbox.com&dl=1"
eebo_zip_path="data-raw/eebo-zips-from-dropbox.zip"

# wget -O "data-raw/eebo-zips-from-dropbox.zip" $eebo_zips_url
# or
curl -o $eebo_zip_path $eebo_zips_url

# check file integrity
unzip -t $eebo_zip_path

mkdir -p "data-raw/eebo-zips"
# you can use the -u option to only update files if you had a partial download
unzip -j -d "data-raw/eebo-zips" $eebo_zip_path "*P5_XML_OXF*.zip"

# save space
rm $eebo_zip_path