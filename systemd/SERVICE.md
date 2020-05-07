# Installing a service

```
sudo cp cocktail.service /lib/systemd/system

sudo systemctl daemon-reload
sudo systemctl enable cocktail.service
sudo systemctl start cocktail.service
```

General checks
```
sudo systemctl status cocktail.service
sudo journalctl -u cocktail.service -b
ps -ef | grep cocktail | grep -v grep
```