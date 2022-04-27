check_bad(){
  if [ $? -gt 0 ]; then
    echo Bad
    bads=$(($bads+1))
  else
    echo Good
  fi
}

echo Test started
bads=0
mkdir test_dir
mkdir test_dir/moved
touch test_dir/test_file
echo Making database
python taginit
ls .nintag_db
echo Cleaning.

echo Show item without tag.
if [ "$(ls test_dir | python tagshow)" = 'moved [  ]' ]; then
  echo Good
else
  echo Bad
  bads=$(($bads+1))
fi
echo Make new tag.
echo hoge | python tagmake
echo Change attr of tag.
echo -e "hoge\\nBOLD\\nCYAN\\nDEFAULT" | python tagcolor
check_bad
echo Change attr of tag again.
echo -e "hoge\\nBOLD\\nRED\\nDEFAULT" | python tagcolor
check_bad
echo Adding tag test
ls -d test_dir/* | python tagadd hoge
echo Show test
ls -d test_dir/* | python tagshow
mv test_dir/test_file test_dir/moved
ls -d test_dir/moved/* | python tagshow | column
echo Speed test
time python -c ''
time ls -d test_dir/moved/* | python tagshow
time ls -d test_dir/moved/*
echo Cleaning up
rm -r test_dir
echo Ended
echo Bads "$bads"
