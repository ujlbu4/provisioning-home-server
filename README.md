


## Connection

После того как прогнали `vagrant up` ключи будут скопированы в папки root'а и vagrant пользователей, соответственно зайти под ssh сможем только под ними

```
ssh root@172.16.20.10
# или
ssh -A vagrant@172.16.20.10
```

чтобы не писать имя пользователя, можно прописать его в конфиге .ssh

```
Host 172.16.20.*
    StrictHostKeyChecking no
    UserKnownHostsFile=/dev/null
    User vagrant
    IdentityFile /Users/ujlbu4/.ssh/id_rsa
```


## Resources
 - как добавить свои ssh ключи на вагрант машину: https://stackoverflow.com/questions/30075461/how-do-i-add-my-own-public-key-to-vagrant-vm