# ansible_role_exporter

Просьба указать переменные:
ansible_become_password:
ansible_ssh_private_key_file:
в файле socket-exporter-deploy/group_vars/all/vault.yml и зашифровать его через ansible vault.
Запустить playbook командой ansible-playbook playbook.yml -i inventory.ini --ask-vault-pass