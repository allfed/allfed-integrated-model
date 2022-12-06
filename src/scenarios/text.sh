
function s(){
    #!/bin/sh
    i3-msg "workspace 3;"
    exec /opt/sublime_text/sublime_text --fwdargv0 "$0" "$@" &
    # echo $0
    # echo $@
    # # input="$@"
    # # firstletter=${input:0:1}
    # # if [ "$firstletter" == "/" ]; then
    # #    i3-msg "workspace 3; exec subl ${1+"$1"} ${2+"$2"}"
    # # else
    # #    i3-msg "workspace 3; exec subl $PWD/$1"
    # # fi
    # input="$@"
    # firstletter=${input:0:1}
    # if [ "$firstletter" == "/" ]; then
    #    i3-msg "workspace 3; exec subl "$@""
    # else
    #    i3-msg "workspace 3; exec subl $PWD/$1"
    # fi
}

s