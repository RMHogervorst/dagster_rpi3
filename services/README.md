I create a service for dagit and dagster deamon on
the RPI.


I'm building this based on blogpost [here](https://scribe.rip/codex/setup-a-python-script-as-a-service-through-systemctl-systemd-f0cc55a42267) ([medium](https://medium.com/codex/setup-a-python-script-as-a-service-through-systemctl-systemd-f0cc55a42267))
and [dagster docs](https://docs.dagster.io/deployment/guides/service)

I need to copy these two files to /etc/systemd/system/
(you need super user rights, so first copy them to the system and use the commandline
  to sudo copy them.`sudo cp dagsterdeamon.service /etc/systemd/system/dagsterdeamon.service`)

then activate them.
`sudo systemctl daemon-reload`
`sudo systemctl enable dagit.service`
Created symlink /etc/systemd/system/multi-user.target.wants/dagit.service → /etc/systemd/system/dagit.service.

`sudo systemctl start dagit.service`
Failed to start dagit.service: Unit dagit.service has a bad unit file setting.
See system logs and 'systemctl status dagit.service' for details


2 possible solutions. Passing environment variables or doing it slightly differnet.
I passed env vars.
first seems to work, but I don't see it running a webbrowser.
LEt's check the logs. `journalctl -u dagit.service`
no logs, I see dagster running when I type top. (mistake! that was the top command under the user dagster, I make it very confusing for myself)

And now it spwes more logs. and the webserver runs!
Alright it fails because this machine had not had libpq5 installed.

configuration says:
it says
repo.py
python_file: /home/dagster/dagster_project/dagster_home/work/repo.py
working_directory: /home/dagster/dagster_project/dagster_home/work

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
Apr 08 06:56:48 rpi3.local dagster-daemon[21479]: 2022-04-08 06:56:48 +0100 - dagster.daemon.SensorDaemon - INFO - Not checking for any runs since no sensors have been start>
Apr 08 06:57:52 rpi3.local dagster-daemon[21479]: 2022-04-08 06:57:52 +0100 - dagster.daemon.SensorDaemon - INFO - Not checking for any runs since no sensors have been start>
Apr 08 06:58:48 rpi3.local dagster-daemon[21479]: 2022-04-08 06:58:48 +0100 - dagster.daemon.SensorDaemon - INFO - Not checking for any runs since no sensors have been start>
```

Lets enable the schedule!

let's see the load.
top

19390 root      20   0  204372  72300  17464 S   5.6   7.7   7:10.17 dagit
21479 root      20   0  180252  57252  15156 S   3.6   6.1   0:15.71 dagster-daemon

installing nginx
sudo apt-get install nginx
`Created symlink /etc/systemd/system/multi-user.target.wants/nginx.service → /lib/systemd/system/nginx.service.`
