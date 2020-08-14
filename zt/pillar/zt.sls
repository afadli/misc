{% set location ='/root' %} 
{% set networkid =' ' %} 
   
zerotier:
   ztlocation: /root/
   ztgpg: "{{ location }}/zerotier.gpg"
   ztscript: "{{ location }}/zerotier.sh"
   ztscript-decry: "{{ location }}/zerotier-decry.sh"
   ztid: "{{ networkid }}"
