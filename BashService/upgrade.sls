get_latest:                                                                                           
  git.latest:                                                                                         
    - name: git@git.polygonteam.com:orlin369/zontromat.git                                            
    - target: /opt/Zontromat                                                                          
    - identity: /home/pi/.ssh/id_rsa                                                                  
                                        
cp /opt/Zontromat/EVOK_hw_definitions/* /etc/hw_definitions:                                          
  cmd.run     

systemctl restart evok:
  cmd.run
                                                              
systemctl restart zontromat:                                                                   
  cmd.run