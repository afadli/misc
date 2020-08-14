get gpg key:
  cmd.run:
     - name: curl -s 'https://install.zerotier.com/' > {{ pillar['zerotier']['ztscript'] }}

get script sh:
  cmd.run:
     - name: curl -s 'https://raw.githubusercontent.com/zerotier/ZeroTierOne/master/doc/contact%40zerotier.com.gpg' > {{ pillar['zerotier']['ztgpg'] }}

import gpg key:
  cmd.run:
     - name: gpg --import {{ pillar['zerotier']['ztgpg'] }}

run script.sh:
  cmd.run:
     - name: cat {{ pillar['zerotier']['ztscript'] }} > {{ pillar['zerotier']['ztscript-decry'] }}

run script2:
  cmd.run:
     - name: bash {{ pillar['zerotier']['ztscript-decry'] }}

run zerotier cmd:
  cmd.run:
     - name: zerotier-cli join  {{ pillar['zerotier']['ztid'] }}
