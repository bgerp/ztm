copy_build:
  file.managed:
    - name: /opt/build.tar.gz
    - source: salt://files/build.tar.gz

rm -rf /opt/Zontromat-backup:
  cmd.run

mv /opt/Zontromat /opt/Zontromat-backup:
  cmd.run

mkdir /opt/Zontromat:
  cmd.run
tar -xvzf /opt/build.tar.gz -C /opt/Zontromat:
  cmd.run
cp /opt/Zontromat-backup/Zontromat/settings.yaml /opt/Zontromat/Zontromat/settings.yaml:
  cmd.run
cp /opt/Zontromat-backup/Zontromat/session.txt /opt/Zontromat/Zontromat/session.txt:
  cmd.run  
cp /opt/Zontromat/hw_definitions/* /etc/hw_definitions:
  cmd.run
systemctl restart evok:
  cmd.run
systemctl restart zontromat:
  cmd.run