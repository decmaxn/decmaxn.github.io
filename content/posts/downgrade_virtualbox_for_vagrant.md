---
title: "Downgrade_virtualbox_for_vagrant"
date: 2023-03-04T16:02:13-05:00
draft: false
tags: ["Vagrant","Virtualbox","tips"]
---

# Don't just upgrade virtualbox to the latest when work with vagrant

Check [Vagrant official Doc](https://developer.hashicorp.com/vagrant/docs/providers/virtualbox) for compatible version of Virtualbox. I have found misleading information from other places.

# Now I have to downgrade Virtualbox.

```cmd
# Uninstall current version of virtualbox 7
choco uninstall virtualbox

# Search available versions
choco search virtualbox --exact --all-versions

# Install a compatible version
choco install virtualbox --version=6.1.42 --force
```

