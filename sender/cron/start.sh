echo "export CADVISOR_IPS=$CADVISOR_IPS" > /cron/cronfile
mkdir /cron/bin/Cron
ln /cron/bin/runcron /cron/bin/Cron/sender.sh
rsyslogd && cron && tail -f /var/log/syslog /var/log/cron.log
