install: MakeTemplate

MakeTemplate: obj/MakeTemplate.o obj/TemplateMaker.o obj/MiniEvent.o obj/Tree.o
	g++ -o MakeTemplate obj/MakeTemplate.o `root-config --libs`

obj/TemplateMaker.o: src/TemplateMaker.cxx src/TemplateMaker.h src/Tree.cxx src/Tree.h src/MiniEvent.cxx src/MiniEvent.h
	g++ -c `root-config --cflags` src/TemplateMaker.cxx
	mkdir -p obj
	mv TemplateMaker.o obj

obj/MiniEvent.o: src/MiniEvent.cxx src/MiniEvent.h
	g++ -c `root-config --cflags` src/MiniEvent.cxx
	mkdir -p obj
	mv MiniEvent.o obj

obj/Tree.o: src/Tree.cxx src/Tree.h
	g++ -c `root-config --cflags` src/Tree.cxx
	mkdir -p obj	
	mv Tree.o obj

obj/MakeTemplate.o: src/TemplateMaker.cxx src/TemplateMaker.h src/Tree.cxx src/Tree.h src/MiniEvent.cxx src/MiniEvent.h
	g++ -c `root-config --cflags` src/MakeTemplate.cxx
	mkdir -p obj
	mv MakeTemplate.o obj

clean:
	rm obj/*.o MakeTemplate

