echo ------ Installing required packages ------
pip install beautifulsoup4
echo ------ ${bold}Done ✓${normal} ------
echo ------ Initializing message parsing ------
echo ------ This process can take upto 5 minutes ------
python parser.py
echo ------ ${bold}Awesome, Done ✓${normal}  ------
echo ------ Launching Website ------


open http://localhost:8000/

# get python version

PYV=`python -c "import sys;t='{v[0]}'.format(v=list(sys.version_info[:2]));sys.stdout.write(t)";`
if (( $PYV == 2 ))
then
    python -m SimpleHTTPServer #Python 2
elif (( $PYV == 3 ))
then
    python -m http.server #Python 3
else
    echo YOU MUST INSTALL PYTHON 2 OR 3
fi




