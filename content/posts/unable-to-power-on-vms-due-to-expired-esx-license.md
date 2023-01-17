+++
title = "Unable to power on VMs due to expired ESX license "
date = 2015-02-16T11:01:00Z
updated = 2017-07-07T19:29:28Z
tags = ["Vmware", "License"]
blogimport = true 

+++

I knew ESX alone is free. Although I always get "License Expired" warning at the right bottom of my vSphere, as long as I can still use it, I never thought about fix it. Today I rebooted it after enabled a feature, and found I can no longer power up my VMs, due to license issue. I didn't have a chance to take any screen dump. <br /><br /><div>I followed these two posts from https://communities.vmware.com/message/2305075 and solved this problem, once for all. Thanks for sharing! </div><div><br /><div class="jive-rendered-content"><div style="height: 8pt; min-height: 8pt; padding: 0px;"><i>Once you login to download the product, you are provided with a licence key - see image below.</i>&nbsp;</div><div style="height: 8pt; min-height: 8pt; padding: 0px;"></div><a href="https://communities.vmware.com/servlet/JiveServlet/showImage/2-2187239-26162/VMware-Hypervisor.png" name="&amp;lpos=apps_scodevmw : 78"><img alt="VMware-Hypervisor.png" class="jive-image jive-image-thumbnail" height="401" src="https://communities.vmware.com/servlet/JiveServlet/downloadImage/2-2187239-26162/450-401/VMware-Hypervisor.png" width="450" /></a> </div></div><div></div><div><i>"Open vSphere client, then select host icon and open Configuration tab.</i></div><div><i>Under Software list, open Licensed Features and at the upper right corner, click on Edit...</i></div><div><i>Select "Assign a new license key to this host", then insert your own free license key provided you by VMWare site."</i></div>
