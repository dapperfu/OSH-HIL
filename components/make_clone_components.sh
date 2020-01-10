find . -name .git | xargs -n1 -IXX git --git-dir=XX remote get-url origin | xargs -n1 echo git clone > clone_components.sh
