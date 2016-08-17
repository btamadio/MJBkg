install: MakeTemplate

MakeTemplate: obj/MakeTemplate.o
	g++ -o MakeTemplate obj/MakeTemplate.o `root-config --libs`

obj/MakeTemplate.o: src/TemplateMaker.cxx src/TemplateMaker.h src/Tree.cxx src/Tree.h
	g++ -c `root-config --cflags` src/MakeTemplate.cxx
	mkdir -p obj
	mv MakeTemplate.o obj

clean:
	rm obj/*.o MakeTemplate

