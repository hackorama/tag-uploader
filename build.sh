set -x

PYTHON=/cygdrive/c/Python24/python
NSIS="/cygdrive/c/Program Files/NSIS/makensis.exe"

rm -rf ./build ./dist 
$PYTHON setup.py py2exe

cp license.txt ./dist
cp mytago.ico ./dist
cp uninstall.ico ./dist
cp Mytago.exe.manifest ./dist

cp mytago.nsi ./dist
cp files.nsi ./dist
cp unfiles.nsi ./dist

cd ./dist
"$NSIS" mytago.nsi
