+++
title = "EliteBook 8570p Can not get IP from DHCP with NDIS driver"
date = 2012-11-30T20:23:00Z
updated = 2017-07-07T19:36:38Z
tags = ["Altiris", "Deploy", "PXE", "OS"]
blogimport = true 

+++

Working on this issue for a few days now. Finally identified the problem is on the driver side, not the DHCP or PXE server side - all other computer works just fine.&nbsp; Find online the t<a href="http://communities.intel.com/thread/31340" target="_blank">his thread,</a> and Symantec support also confirmed my finding. <br /><br />It seems Intel has got a support case opened at Nov 8, 2012,&nbsp; Please refer to <a href="http://communities.intel.com/message/171833" target="_blank">here</a>, but I can't wait. Symantec Support suggest to use WinPE, I end up went this way.<br /><br />This problem also have another symptom<span style="font-size: small;"> like <a href="http://communities.intel.com/thread/31340" target="_blank"><span style="font-weight: normal;">82579LM - DOS NDIS2-driver does not work - no ping response.</span></a></span>
