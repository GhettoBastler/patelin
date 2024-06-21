clean:
	$(RM) build/*


build: clean
	pip freeze > requirements.txt
	sudo docker buildx build -t patelin --platform arm64 .
	sudo docker save patelin | gzip > build/patelin.tar.gz

.PHONY: clean build
