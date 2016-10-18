install: RunDresser

RunDresser: obj/RunDresser.o obj/dresser.o obj/miniTree.o src/RunDresser.cxx
	g++ -o RunDresser obj/RunDresser.o `root-config --libs`

obj/miniTree.o: src/miniTree.cxx src/miniTree.h
	g++ -c `root-config --cflags` src/miniTree.cxx
	mkdir -p obj	
	mv miniTree.o obj

obj/dresser.o: src/dresser.cxx src/dresser.h src/miniTree.cxx src/miniTree.h
	g++ -c `root-config --cflags` src/dresser.cxx
	mkdir -p obj
	mv dresser.o obj

obj/RunDresser.o: src/dresser.cxx src/dresser.h src/miniTree.cxx src/miniTree.h src/RunDresser.cxx
	g++ -c `root-config --cflags` src/RunDresser.cxx
	mkdir -p obj
	mv RunDresser.o obj

clean:
	rm obj/*.o RunDresser