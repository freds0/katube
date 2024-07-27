#!/bin/bash
echo $PORTA

if [[ -z "$PORTA" ]]; then
    echo -e "\nPor favor, exporte a porta utilizada no comando de ssh!\nUtilize:\nexport PORTA=sua_porta"
    exit 1
else
    echo -e "\nAbrindo container."
fi
sudo docker run \
        -it \
        -p $PORTA:8888\
        --rm \
        --ipc=host \
        --volume "/home/aluno_marceloferreira/katube-gama":"/app" \
        --ulimit memlock=-1 \
        --name 'ermis-dataset'\
	--gpus all\
        --memory=200g\
        --ulimit stack=67108864 \
        katube-gamma
