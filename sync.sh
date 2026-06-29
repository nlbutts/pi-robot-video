#!/bin/bash
rsync -avz -e "sshpass -p robots ssh" "$(dirname "$0")/" robots@pi:~/pi-robot-video/
