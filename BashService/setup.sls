copy_public_key:                                                                                      
  file.recurse:                                                                                       
    - name: "/home/pi/.ssh/"                                                                          
    - source:                                                                                         
      - salt://auth/                                                                                  
    - replace: True                                                                                   
    - file_mode: 600                                                                                  
                                                                                                      
git@git.polygonteam.com:orlin369/zontromat.git:                                                       
  git.latest:                                                                                         
    - target: /opt/Zontromat                                                                          
    - identity: /home/pi/.ssh/id_rsa                                                                  
    - branch: master                                                                                  
                                                                                                      
cd /opt/Zontromat/Zontromat && pip3 install -r requirements.txt:                                      
  cmd.run                                                                                             
                                                                                                      
cd /opt/Zontromat/BashService && cp zontromat.service /etc/systemd/system/ && systemctl enable zontromat.service && systemctl start zontromat.service:                                  
  cmd.run                                                                                             
                                                                                                      
cp /opt/Zontromat/EVOK_hw_definitions/* /etc/hw_definitions:                                          
  cmd.run        