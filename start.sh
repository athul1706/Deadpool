if [ -z $UPSTREAM_REPO ]
then
  echo "Cloning main Repository"
  git clone https://github.com/Athul1223/Deadpool.git /Deadpool
else
  echo "Cloning Custom Repo from $UPSTREAM_REPO "
  git clone $UPSTREAM_REPO /Deadpool
fi
cd /EvaMaria
pip3 install -U -r requirements.txt
echo "Starting Bot...."
python3 bot.py
