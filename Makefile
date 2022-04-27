.PHONY: test clean
test: test1
test1:
	mkdir test_dir;\
	mkdir test_dir/moved;\
	touch test_dir/moved/hoge;\
	NINTAG_DB=${HOME}/.config/nintag/nintag.db;\
	rm ${NINTAG_DB};\
	ls | python tagshow | column;\
	echo hoge | python tagmake;\
	echo "hoge\\nBOLD\\nCYAN\\nDEFAULT" | python tagcolor;\
	ls -d test_dir/* | python tagadd hoge;\
	ls -d test_dir/* | python tagshow | column;\
	ls -d test_dir/moved/* | python tagshow | column;\
	rm -r test_dir

test_dir/test_file:
	touch test_dir/test_file
clean: ${HOME}/.config/nintag/nintag.db
	${HOME}/.config/nintag/nintag.db
