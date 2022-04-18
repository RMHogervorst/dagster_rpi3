# todos

- [ ] make an a push notification op (pushover)
- [ ] knmi data predictions? (http://weerlive.nl/delen.php) or https://openweathermap.org/api/hourly-forecast (can I use that for free?)
- [x] build dbt project init
- [ ] fill in project
* [x] create service for daemon (use venv)
* [x] create service for dagit (use venv) (missing system library `sudo apt install libpq5`)

serving pages:
- [x] install nginx on rpi3
- [ ] move dagster from rpi3.local:3000 to rpi3.local/dagster/
  - [ ] maybe set not to 0.0.0.0:3000 but 127.0.0.1:3000
  - [ ] redirect from nginx
- [x] display dbt static page on rpi3.local/dbt/


* [ ] push this repo to github
* [ ] create cronschedule that pulls from github (risk!) and auto deploys

I will automatically copy the dagster_home folder.

git push to github and download?
