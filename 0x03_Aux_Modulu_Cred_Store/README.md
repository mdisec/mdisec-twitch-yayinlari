# MSF-Development-Twitch-Series
Bu repo'da https://twitch.tv/mdisec kanalında yapılan kanlı-canlı siber güvenlik eğitimlerine dair kodlar bulunmaktadır. Her klasör, ilgili eğitimde anlatılanları içermektedir.

```
✗ createuser -s twitch
✗ createdb twitch
✗ psql -U twitch
psql (11.2)
Type "help" for help.

twitch=# \password
Enter new password: 
Enter it again: 
twitch=#

✗ pip -r requirements.txt
✗ export FLASK_APP=app.py   
✗ python -m flask run 

You can check inserted datas with following query
twitch=# select * from public.user;
```

This app is heavily based on `https://github.com/anfederico/Flaskex`