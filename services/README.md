# making the things work automatically

I create a service for dagit and dagster deamon on
the RPI.
I also use nginx to display the dbt docs and maybe serve dagit on a differnet location.




## Building a service for dagit and deamon
I'm building this based on blogpost [here](https://scribe.rip/codex/setup-a-python-script-as-a-service-through-systemctl-systemd-f0cc55a42267) ([medium](https://medium.com/codex/setup-a-python-script-as-a-service-through-systemctl-systemd-f0cc55a42267))
and [dagster docs](https://docs.dagster.io/deployment/guides/service)
* create a systemctl configuration
* copy to correct location
* activate it
* restart systemctl deamon

I need to copy these two files to /etc/systemd/system/
(you need super user rights, so first copy them to the dagster folder and use the commandline
  to sudo copy them.
```
sudo cp /home/dagster/services/dagsterdeamon.service /etc/systemd/system/dagsterdeamon.service
sudo cp /home/dagster/services/dagit.service /etc/systemd/system/dagit.service
```
)

then activate them.
`sudo systemctl daemon-reload`
`sudo systemctl enable dagit.service`

```
Created symlink /etc/systemd/system/multi-user.target.wants/dagit.service → /etc/systemd/system/dagit.service.
```

`sudo systemctl start dagit.service`


when you have errors, check the logs: `journalctl -u dagit.service`

Alright it fails because this machine had not had libpq5 installed.
other gotchas: systemctl has not access to the same env variables.
If you add a line to point to variables file it will work.

enabled dagster deamon.
```
sudo systemctl enable dagsterdeamon.service
sudo systemctl start dagsterdeamon.service
sudo systemctl status dagsterdeamon.service
sudo journalctl -u dagsterdeamon.service
```

```
-- Journal begins at Fri 2022-01-28 01:22:52 GMT, ends at Fri 2022-04-08 06:59:26 BST. --
Apr 08 06:55:43 rpi3.local systemd[1]: Started Dagster deamon service, keeps track of time..
Apr 08 06:55:47 rpi3.local dagster-daemon[21479]: 2022-04-08 06:55:47 +0100 - dagster.daemon - INFO - instance is configured with the following daemons: ['BackfillDaemon', '>
Apr 08 06:55:52 rpi3.local dagster-daemon[21479]: 2022-04-08 06:55:52 +0100 - dagster.daemon.SensorDaemon - INFO - Not checking for any runs since no sensors have been start>
Apr 08 06:56:48 rpi3.local dagster-daemon[21479]: 2022-04-08 06:56:48 +0100 - dagster.daemon.SensorDaemon - INFO - Not checking for any runs since no sensors have been
```

Lets enable the schedule!

let's see the load.
`top`
```
19390 root      20   0  204372  72300  17464 S   5.6   7.7   7:10.17 dagit
21479 root      20   0  180252  57252  15156 S   3.6   6.1   0:15.71 dagster-daemon
```


## installing nginx
sudo apt-get install nginx
`Created symlink /etc/systemd/system/multi-user.target.wants/nginx.service → /lib/systemd/system/nginx.service.`

- check if it works. use the webbrowser to go to rpi3.local/ (it shows the standard nginx page.)

settings should live here `/etc/nginx/nginx.conf`

idea:
* localhost:3000 is dagster -> redirect to /dagster
* serve the dbt docs on -> /dbt

copied everything to /home/dagster/dagster_project/services/
`sudo cp /home/dagster/services/dagster.conf /etc/nginx/sites-available/dagster.conf`

test nginx config `sudo nginx -t`
```
nginx: [emerg] invalid number of arguments in "root" directive in /etc/nginx/sites-enabled/dagster.conf:7
nginx: configuration file /etc/nginx/nginx.conf test failed
```

reload nginx. `sudo systemctl reload nginx`



`sudo cp /home/dagster/services/dagster.conf /etc/nginx/sites-available/dagster.conf`
`sudo cp /home/dagster/services/dagster.conf /etc/nginx/sites-enabled/dagster.conf`

removed them and start again in nginx.conf
(https://fedingo.com/how-to-serve-static-files-from-different-folder-in-nginx/)
/ works
/dbt/ not working
/dagster/ not working
check logs.

```sudo nginx -t
nginx: the configuration file /etc/nginx/nginx.conf syntax is ok
nginx: configuration file /etc/nginx/nginx.conf test is successful
```

sudo tail /var/log/nginx/access.log

```
/etc/nginx/nginx.conf: The main NGINX configuration file. This can be modified to make changes to the NGINX global configuration.
/etc/nginx/sites-available/: The directory where per-site “server blocks” can be stored. NGINX will not use the configuration files found in this directory unless they are linked to the sites-enabled directory (see below). Typically, all server block configuration is done in this directory, and then enabled by linking to the other directory.
/etc/nginx/sites-enabled/: The directory where enabled per-site “server blocks” are stored. Typically, these are created by linking to configuration files found in the sites-available directory.
```

replaced default dbt works. dagster doesn not.

access log `sudo tail /var/log/nginx/access.log`
```
2001:1c00:b0a:6d00:4003:abe4:f13e:287a - - [14/Apr/2022:07:47:40 +0100] "GET /dagster/ HTTP/1.1" 307 0 "-" "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:99.0) Gecko/20100101 Firefox/99.0"
```

error log
```
2022/04/14 07:47:39 [error] 21887#21887: *1 connect() failed (111: Connection refused) while connecting to upstream, client: 2001:1c00:b0a:6d00:4003:abe4:f13e:287a, server: rpi3.local, request: "GET /dagster/ HTTP/1.1", upstream: "http://[::1]:3000/", host: "rpi3.local"
```
