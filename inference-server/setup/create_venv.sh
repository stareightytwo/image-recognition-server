#!/bin/bash

if [[ -d venv ]]; then
    rm -rf venv/
fi

virtualenv venv
source venv/bin/activate

pip3 install --upgrade pip
pip3 install -r ../requirements.txt

if ! [[ -d darkflow ]]; then
	git clone https://github.com/thtrieu/darkflow.git
	cd darkflow

	pip3 install .

	git clone https://github.com/leetenki/YOLOtiny_v2_chainer.git
	mkdir bin
	mv YOLOtiny_v2_chainer/tiny-yolo-voc.weights bin/

	rm -rf YOLOtiny_v2_chainer
fi