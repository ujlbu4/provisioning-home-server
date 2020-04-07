
## Ansible Resources:
 - [Configuration Management 101: Writing Ansible Playbooks](https://www.digitalocean.com/community/tutorials/configuration-management-101-writing-ansible-playbooks) — норм
 - [Automating Server Setup with Ansible: A DigitalOcean Workshop Kit](https://www.digitalocean.com/community/meetup_kits/automating-server-setup-with-ansible-a-digitalocean-workshop-kit)
 - [How to Use Ansible Roles to Abstract your Infrastructure Environment](https://www.digitalocean.com/community/tutorials/how-to-use-ansible-roles-to-abstract-your-infrastructure-environment)


## TODO:
 - [x] zsh
    - [x] oh-my-zsh
    - [x] плагины и настройки к нему
 - [x] user'ов и их ssh ключи
 - [x] настройки firewall'а (ufw)
 - soft 
    - [x] docker
    - [x] openvpn server (конфиги, ключи и т.д)
    - [ ] socks5
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


## Ansible Galaxy

resources: 
 - https://docs.ansible.com/ansible/latest/galaxy/user_guide.html


Galaxy удобен тем, что он как `pip install` — не нужно заморачиваться с сабмодулями для ролей — создаешь requirements.txt файл, прописываешь нужные roles (community collections чот не зашли, либо я прост не встретил подходящих), запускаешь:
```
ansible-galaxy role install -r requirements.yml
```
и оно все приезжает, ты это коммитишь в репу, ну и апдейтишь при необходимости. 

Примечание: чтобы ansible-galaxy устанавливал в нужную папку по умолчанию, то проще ее прописать в `ansible.cfg` — поле `roles_path`


## Playbook Filters

resources:
 - https://docs.ansible.com/ansible/latest/user_guide/playbooks_filters.html — отличный раздел, в котором приведены вомзожные операции на jinja2 переменными (которые повсеместно используются в плейбуках)
 - https://docs.ansible.com/ansible/latest/dev_guide/developing_plugins.html — developing plugins

В общем, для одной из community ролей потребовалось преобразовать массив пользователей в массив словарей пользователей:
```
['user1', 'user2'] --> [{'username': 'user1'}, {'username': 'user2'}]
```
стандартных фильров для такой операции не нашлось и как позже оказалось, самым простым и быстро было создать свой фильтр по образу и подобию существующих ([тыц](https://github.com/ansible/ansible/blob/devel/lib/ansible/plugins/filter/core.py)):



## Troubleshooting

resources:
    - https://docs.ansible.com/ansible/latest/reference_appendices/faq.html#running-in-a-virtualenv

В моменты, когда не все ansible фильтры отрабатывали, хоть и брались из документации, была мысля, что поскольку ansible преобразует все playbook'и на контроллер машине и использует jinja2 (питоновская либа), то подумал, что возможно у меня в system-site-packages питоновских стоит старая версия jinja'ы и поэтому он не может найти нужный фильтр.

Поэтому, чтобы чисто запустить ансибл на нужной версии питона и с читыми актуальными site-package'ами для него, то можно заюзать `virtualenv`. 

У меня, конечно, проблема оказалось не в этом, но на будущее все равно полезно знать про такой момент.



## OpenVPN setup

resources:
 - ansible
    - https://www.techchorus.net/blog/run-your-own-openvpn-server/ — при первом взгляде норм статься с инсрукциями и примерами как что настрорить
        - [gavika.openvpn](https://github.com/gavika/openvpn) — см. playbook execution flow
        - [gavika.easy_rsa](https://github.com/gavika/easy_rsa)
        - а вообще хз, предлагет запускать 3 раза в правильном порядке — "You are responsible to execute the roles the required number of times and in required order", чот идемпотентностью и не пахнет (updated: по коду все же пока этот варик нравится больше чем с stouts в котором много возни было, текущий я ставить не пробовал, но идеалогически он выглядит более правильным)
    - https://itnext.io/setup-privacy-with-openvpn-using-ansible-b9e613a66f85 — более кардкодный способ, выглядит что как-будто в лоб [вот эту инструкцицию (digitalocean)](https://www.digitalocean.com/community/tutorials/how-to-set-up-an-openvpn-server-on-ubuntu-16-04) автоматизировал
        - [исходники](https://github.com/MiteshSharma/OpenVPNAnsible)
    - https://dteslya.engineer/automation/2019-02-25-ansible-openvpn/ — вот еще чувак, но чот мне не нравится его решение
        - [исходинки](https://github.com/dteslya/ansible-ovpn-mikrotik)
        - вот [пример того](https://github.com/dteslya/ansible-ovpn-mikrotik/blob/01caae618929a5a6077496a599c9a79f983bb1b2/playbooks/roles/add_clients/tasks/add_gen_key.yml#L51), что не нравится
    - https://github.com/Stouts/Stouts.openvpn — использовал этот, но возни было много (думаю попробовать и переехать на gavika)
        - смущает что ключи не подписывают для openvpn-server'а, а сразу используют сгенерированные в rsa, с другой стороны для pet-project'а возможно это норм


 - troubleshooting
    - https://habr.com/ru/post/233971/ — отличный, подробный обзор openvpn, CA, клиентов — какие оно работает и т.д (дает собственно понимание зависимостей и как следствие сильно помогает в дебаге и настройки конфигов)
    - OpenVPN client connection not started , no logs get written
> в общем, проблема такая, что `service openvpn status` пишет, что стартанул, но файл с логами не создается (т.е. я даже не мог задебажить почему vpn не подключается), ответы нашел здесь:
        - https://unix.stackexchange.com/questions/292091/ubuntu-server-16-04-openvpn-seems-not-to-start-no-logs-get-written
        - https://a20.net/bert/2016/09/27/openvpn-client-connection-not-started-on-ubuntu-16-04/
        - плюс почитать в принципе про [systemd](https://wiki.archlinux.org/index.php/Systemd_(%D0%A0%D1%83%D1%81%D1%81%D0%BA%D0%B8%D0%B9))


TODO:
 - [ ] загружать ранее сгенеренные ключи (для случая, когда на новый сервак переехали с нуля, чтобы не перездавать всем клиентам новые ключи (*.ovpn) )