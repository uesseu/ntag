check_bad(){
  if [ $? -gt 0 ]; then
    echo Bad
    bads=$(($bads+1))
  else
    echo Good
  fi
}
label(){
  echo =============
  echo \| $@
}

label Test started
bads=0
mkdir test_dir
mkdir test_dir/moved
touch test_dir/test_file
label No database error test
ntag-status
check_bad
label Making database
ntag-init
check_bad
label Cleaning.

label Show item without tag.
if [ "$(ls test_dir/moved -d | ntag-show)" = 'test_dir/moved [  ]' ]; then
  echo Good
else
  echo Bad
  ls test_dir/moved -d | ntag-show
  bads=$(($bads+1))
fi
label Make new tag.
echo hoge | ntag-make
label Change attr of tag.
echo -e "hoge\\nBOLD\\nCYAN\\nDEFAULT" | ntag-color > /dev/null
check_bad
label Change attr of tag again.
echo -e "hoge\\nBOLD\\nRED\\nDEFAULT" | ntag-color > /dev/null
check_bad
label Adding tag test
ls -d test_dir/* | ntag-add hoge
ls -d test_dir/* | ntag-add fuga
label Show test
ls -d test_dir/* | ntag-show
mv test_dir/test_file test_dir/moved
ls -d test_dir/moved/* | ntag-show | column
label Remove test
ls -d test_dir/moved/* | ntag-remove hoge
check_bad
if [ "$(ls -d test_dir/moved/* | ntag-show | column)"\
  = 'test_dir/moved/test_file [  ]' ]; then
  echo Good
else
  echo Bad
  ls test_dir/moved -d | ntag-show
  bads=$(($bads+1))
fi
label Remove \'None\' test
ls -d test_dir/moved/* | ntag-remove None
ls -d test_dir/moved/* | ntag-remove NULL
ls -d test_dir/* | ntag-add hoge
check_bad
label Remove tag test
ntag-delete hoge
ls -d test_dir/* | ntag-show
label Speed test
time ls -d test_dir/* | ntag-show
time echo .exit | sqlite3
label Cleaning up
rm -r test_dir
rm .nintag_db
label Ended
echo Bads "$bads"
