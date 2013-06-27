# -*- mode: ruby -*-
# vi: set ft=ruby :

$script = <<SCRIPT
git clone https://github.com/gtfierro/dotfiles/
cp -r dotfiles/.vim* .
cp -r dotfiles/.tmux* .
cp -r dotfiles/tmux* .
cp -r dotfiles/.zshrc .
cp -r dotfiles/.oh-my-zsh .
mkdir -p .vim/swaps
mkdir -p .vim/backups
rm -rf dotfiles
git clone https://github.com/gtfierro/BAS/
cd BAS/python
sudo python setup.py install
cd ../..
wget http://pysqlite.googlecode.com/files/pysqlite-2.6.3.tar.gz
tar xzf pysqlite-2.6.3.tar.gz
cd pysqlite-2.6.3
sed -i '6 s/^/#/' setup.cfg
sudo python setup.py install
cd ..
rm -rf pysqlite-2.6.3*
SCRIPT

Vagrant::Config.run do |config|
  # All Vagrant configuration is done here. The most common configuration
  # options are documented and commented below. For a complete reference,
  # please see the online documentation at vagrantup.com.

  # Every Vagrant virtual environment requires a box to build off of.
  config.vm.box = "precise64"

  # The url from where the 'config.vm.box' box will be fetched if it
  # doesn't already exist on the user's system.
  config.vm.box_url = "http://files.vagrantup.com/precise64.box"

  # Assign this VM to a host-only network IP, allowing you to access it
  # via the IP. Host-only networks can talk to the host machine as well as
  # any other machines on the same network, but cannot be accessed (through this
  # network interface) by any external networks.
  # config.vm.network :hostonly, "192.168.33.10"

  # Assign this VM to a bridged network, allowing you to connect directly to a
  # network using the host's network device. This makes the VM appear as another
  # physical device on your network.
  # config.vm.network :bridged

  # Forward a port from the guest to the host, which allows for outside
  # computers to access the VM, whereas host only networking does not.
  config.vm.forward_port 80, 8080
  config.vm.forward_port 8000, 8000

  # provision!
  config.vm.provision :puppet
  config.vm.provision :shell, :inline => $script
end
