install: Tree

Tree: obj/Tree.o
	g++ -o Tree obj/Tree.o `root-config --libs`

obj/Tree.o: src/Tree.cxx src/Tree.h
	g++ -c `root-config --cflags` src/Tree.cxx
	mkdir -p obj
	mv Tree.o obj

clean:
	rm obj/*.o

