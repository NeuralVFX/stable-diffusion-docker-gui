xhost +local:docker 

docker run -ti --runtime=nvidia -v $PWD/mount:/app/mount --rm -v /tmp/.X11-unix:/tmp/.X11-unix -e DISPLAY -e XAUTHORITY sdgui
