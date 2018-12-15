BASEDIR=$(dirname $(readlink -f $0))
VENV=venv/bin/activate

cd $BASEDIR
source $VENV
python run.py -o backup -t mysql
sleep 10
python run.py -o backup -t mongo
sleep 10
python run.py -o backup -t file