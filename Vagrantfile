Vagrant.configure("2") do |config|
  # Ubuntu virtual machine
  config.vm.box = "ubuntu/jammy64"
  config.vm.hostname = "python-devops-app"

  # Private IP address
  config.vm.network "private_network", ip: "192.168.56.10"

  # Windows port 8000 -> VM port 8080
  config.vm.network "forwarded_port",
  guest: 8000,
  host: 8080

  # Share the complete project with Ubuntu
  config.vm.synced_folder ".", "/vagrant"

  # VirtualBox resources
  config.vm.provider "virtualbox" do |vb|
    vb.name = "dsti-python-devops-project"
    vb.memory = 2048
    vb.cpus = 2
  end

  # Run Ansible inside Ubuntu
  config.vm.provision "ansible_local" do |ansible|
    ansible.install = true
    ansible.playbook = "/vagrant/iac/playbooks/playbook.yml"
    ansible.inventory_path = "/vagrant/iac/playbooks/inventory.ini"
    ansible.limit = "all"
  end
end