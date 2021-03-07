git pull

pip install -r requirements.txt

overmind quit

while pgrep overmind >/dev/null; do
    echo "Waiting for overmind to stop..."
    sleep 1
done

docker run -d -p 5672:5672 rabbitmq

overmind start -D
