main: test_dir test_dir/test_file
	-rm ${HOME}/.config/nintag/nintag.db
	ls | python tagshow
	echo hoge | python tagmake
	ls -d test_dir/* | python tagadd hoge
	ls -d test_dir/* | python tagshow
	mv test_dir/test_file test_dir/moved
	ls -d test_dir/moved/* | python tagshow
	cd test_dir/moved; ls 

test_dir:
	mkdir test_dir
test_dir/moved:
	mkdir test_dir/moved
test_dir/test_file:
	touch test_dir/test_file
clean: ./nintag.db
	rm ./nintag.db
