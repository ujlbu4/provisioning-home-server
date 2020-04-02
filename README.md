
## Ansible Resources:
 - [Configuration Management 101: Writing Ansible Playbooks](https://www.digitalocean.com/community/tutorials/configuration-management-101-writing-ansible-playbooks) — норм
 - [Automating Server Setup with Ansible: A DigitalOcean Workshop Kit](https://www.digitalocean.com/community/meetup_kits/automating-server-setup-with-ansible-a-digitalocean-workshop-kit)
 - [How to Use Ansible Roles to Abstract your Infrastructure Environment](https://www.digitalocean.com/community/tutorials/how-to-use-ansible-roles-to-abstract-your-infrastructure-environment)


## TODO:
 - [ ] zsh
    - [ ] oh-my-zsh
    - [ ] плагины и настройки к нему
 - [ ] user'ов и их ssh ключи
 - [ ] vpn конфиги, ключи и т.д
 - [ ] настройки firewall'а (ufw)
 - soft 
    - [ ] home-assistant
        - [ ] hassio
        - [ ] hacs
    - [ ] ? mattermost
    - [ ] ? gitlab-agent

## Пробросить ssh ключи на vagrant машину

resources:
    - как добавить свои ssh ключи на вагрант машину: https://stackoverflow.com/questions/30075461/how-do-i-add-my-own-public-key-to-vagrant-vm

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


## Testing Ansible Connection 

resources:
- [testing connection](https://www.digitalocean.com/community/tutorials/how-to-install-and-configure-ansible-on-ubuntu-18-04#step-3-%E2%80%94-testing-connection)

From your local machine or Ansible control node, run:
```
ansible all -m ping -u vagrant
```

This command will use Ansible’s built-in ping module to run a connectivity test on all nodes from your default inventory, connecting as `vagrant`. The ping module will test:
- if hosts are accessible;
- if you have valid SSH credentials;
- if hosts are able to run Ansible modules using Python.

если все норм вернется что-то типа:
```
homeserver.v | SUCCESS => {
    "ansible_facts": {
        "discovered_interpreter_python": "/usr/bin/python3"
    },
    "changed": false,
    "ping": "pong"
}
```