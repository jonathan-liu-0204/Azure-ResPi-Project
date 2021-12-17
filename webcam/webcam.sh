#!/bin/bash

DATE=$(date +"%Y-%m-%d_%H%M")

fswebcam -r 1920x1080 --no-banner $DATE.jpg