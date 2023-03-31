# Win_feature changes will fail the tasks behind it, and it's solution


<div style="font-family: Calibri; font-size: 11.0pt; margin: 0in;">The problem with these code is, after Server-Gui-Shell, Server-Gui-Mgmt-Infra are uninstalled, the windows will reboot immediately, leaving index.html template deployment failed.&nbsp;</div><div style="font-family: Consolas; font-size: 11.0pt; margin-left: .375in; margin: 0in;">vagrant@acs:~/pywinrm$ cat iis.yaml</div><div style="font-family: Consolas; font-size: 11.0pt; margin-left: .375in; margin: 0in;">---</div><div style="font-family: Consolas; font-size: 11.0pt; margin-left: .375in; margin: 0in;">- hosts: s12</div><div style="font-family: Consolas; font-size: 11.0pt; margin-left: .375in; margin: 0in;">&nbsp; tasks:</div><div style="font-family: Consolas; font-size: 11.0pt; margin-left: .375in; margin: 0in;">&nbsp; - name: Ensure IIS seb service is installed</div><div style="font-family: Consolas; font-size: 11.0pt; margin-left: .375in; margin: 0in;">&nbsp;&nbsp;&nbsp; win_feature:</div><div style="font-family: Consolas; font-size: 11.0pt; margin-left: .375in; margin: 0in;">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; name: web-server</div><div style="font-family: Consolas; font-size: 11.0pt; margin-left: .375in; margin: 0in;">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; state: present</div><div style="font-family: Consolas; font-size: 11.0pt; margin-left: .375in; margin: 0in;">&nbsp; - name: Ensure Server GUI is not installed</div><div style="font-family: Consolas; font-size: 11.0pt; margin-left: .375in; margin: 0in;">&nbsp;&nbsp;&nbsp; win_feature:</div><div style="font-family: Consolas; font-size: 11.0pt; margin-left: .375in; margin: 0in;">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; name: Server-Gui-Shell</div><div style="font-family: Consolas; font-size: 11.0pt; margin-left: .375in; margin: 0in;">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; state: absent</div><div style="font-family: Consolas; font-size: 11.0pt; margin-left: .375in; margin: 0in;">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; restart: true</div><div style="font-family: Consolas; font-size: 11.0pt; margin-left: .375in; margin: 0in;">&nbsp; - name: Deploy index.html file</div><div style="font-family: Consolas; font-size: 11.0pt; margin-left: .375in; margin: 0in;">&nbsp;&nbsp;&nbsp; template:</div><div style="font-family: Consolas; font-size: 11.0pt; margin-left: .375in; margin: 0in;">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; src: iisstart.j2</div><div style="font-family: Consolas; font-size: 11.0pt; margin-left: .375in; margin: 0in;"><br /></div><div style="font-family: Calibri; font-size: 11.0pt; margin: 0in;">You can put that Windows Feature block to the last of this playbook, or use handlers as below. However neither is best way. </div><div style="font-family: Calibri; font-size: 11.0pt; margin: 0in;"><br /></div><div style="font-family: Consolas; font-size: 11.0pt; margin: 0in;">vagrant@acs:~/pywinrm$ cat iis.yaml</div><div style="font-family: Consolas; font-size: 11.0pt; margin: 0in;">---</div><div style="font-family: Consolas; font-size: 11.0pt; margin: 0in;">- hosts: s12</div><div style="font-family: Consolas; font-size: 11.0pt; margin: 0in;">&nbsp; handlers:</div><div style="font-family: Consolas; font-size: 11.0pt; margin: 0in;">&nbsp; - name: Reboot</div><div style="font-family: Consolas; font-size: 11.0pt; margin: 0in;">&nbsp;&nbsp;&nbsp; win_reboot:</div><div style="font-family: Consolas; font-size: 11.0pt; margin: 0in;">&nbsp; tasks:</div><div style="font-family: Consolas; font-size: 11.0pt; margin: 0in;">&nbsp; - name: Ensure IIS seb service is installed</div><div style="font-family: Consolas; font-size: 11.0pt; margin: 0in;">&nbsp;&nbsp;&nbsp; win_feature:</div><div style="font-family: Consolas; font-size: 11.0pt; margin: 0in;">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; name: web-server</div><div style="font-family: Consolas; font-size: 11.0pt; margin: 0in;">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; state: present</div><div style="font-family: Consolas; font-size: 11.0pt; margin: 0in;">&nbsp;&nbsp;&nbsp; when: ansible_os_family == "Windows"</div><div style="font-family: Consolas; font-size: 11.0pt; margin: 0in;">&nbsp; - name: Ensure Server GUI is not installed</div><div style="font-family: Consolas; font-size: 11.0pt; margin: 0in;">&nbsp;&nbsp;&nbsp; win_feature:</div><div style="font-family: Consolas; font-size: 11.0pt; margin: 0in;">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; name: Server-Gui-Shell</div><div style="font-family: Consolas; font-size: 11.0pt; margin: 0in;">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; state: absent</div><div style="font-family: Consolas; font-size: 11.0pt; margin: 0in;">&nbsp;&nbsp;&nbsp; notify:</div><div style="font-family: Consolas; font-size: 11.0pt; margin: 0in;">&nbsp;&nbsp;&nbsp; - Reboot</div><div style="font-family: Consolas; font-size: 11.0pt; margin: 0in;">&nbsp; - name: Deploy index.html file</div><div style="font-family: Consolas; font-size: 11.0pt; margin: 0in;">&nbsp;&nbsp;&nbsp; template:</div><div style="font-family: Consolas; font-size: 11.0pt; margin: 0in;">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; src: iisstart.j2</div><div style="font-family: Consolas; font-size: 11.0pt; margin: 0in;">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; dest: c:\inetpub\wwwroot\iisstart.htm</div><div style="font-family: Consolas; font-size: 11.0pt; margin: 0in;"><br /></div><div style="font-family: Consolas; font-size: 11.0pt; margin: 0in;">Here is the best way according to ansible document:-</div><div style="direction: ltr;"> <table border="1" cellpadding="0" cellspacing="0" style="border-collapse: collapse; border-color: #A3A3A3; border-style: solid; border-width: 1pt; direction: ltr;" valign="top"> <tbody><tr>  <td style="border-color: #A3A3A3; border-style: solid; border-width: 1pt; padding: 4pt 4pt 4pt 4pt; vertical-align: top; width: .6673in;">  <div style="font-family: Calibri; font-size: 11.0pt; margin: 0in;">restart</div></td>  <td style="border-color: #A3A3A3; border-style: solid; border-width: 1pt; padding: 4pt 4pt 4pt 4pt; vertical-align: top; width: .6673in;">  <div style="font-family: Calibri; font-size: 11.0pt; margin: 0in;">no</div></td>  <td style="border-color: #A3A3A3; border-style: solid; border-width: 1pt; padding: 4pt 4pt 4pt 4pt; vertical-align: top; width: .6673in;">  <div style="font-family: Calibri; font-size: 11.0pt; margin: 0in;">True</div><div style="font-family: Calibri; font-size: 11.0pt; margin: 0in;">False</div></td>  <td style="border-color: #A3A3A3; border-style: solid; border-width: 1pt; padding: 4pt 4pt 4pt 4pt; vertical-align: top; width: 4.409in;">  <div style="font-family: Calibri; font-size: 11.0pt; margin: 0in;">Restarts the   computer automatically when installation is complete, if restarting is   required by the roles or features installed.</div><div style="font-family: Calibri; font-size: 11.0pt; margin: 0in;">DEPRECATED in   Ansible 2.4, as unmanaged reboots cause numerous issues under Ansible. Check   the reboot_required return value from this module to determine if a reboot is   necessary, and if so, use the win_reboot action to perform it.</div></td> </tr></tbody></table></div><div style="color: #595959; font-family: Calibri; font-size: 9.0pt; margin: 0in;">From &lt;<a href="http://docs.ansible.com/ansible/win_feature_module.html#support">http://docs.ansible.com/ansible/win_feature_module.html#support</a>&gt; </div><div style="font-family: Calibri; font-size: 11.0pt; margin: 0in;"><br /></div><div style="direction: ltr;"> <table border="1" cellpadding="0" cellspacing="0" style="border-collapse: collapse; border-color: #A3A3A3; border-style: solid; border-width: 1pt; direction: ltr;" valign="top"> <tbody><tr>  <td style="border-color: #A3A3A3; border-style: solid; border-width: 1pt; padding: 4pt 4pt 4pt 4pt; vertical-align: top; width: .7152in;">  <div style="font-family: Calibri; font-size: 11.0pt; margin: 0in;">restart_needed </div></td>  <td style="border-color: #A3A3A3; border-style: solid; border-width: 1pt; padding: 4pt 4pt 4pt 4pt; vertical-align: top; width: 3.9152in;">  <div style="font-family: Calibri; font-size: 11.0pt; margin: 0in;">DEPRECATED in   Ansible 2.4 (refer to C(reboot_required) instead). True when the target   server requires a reboot to complete updates (no further updates can be   installed until after a reboot) </div></td>  <td style="border-color: #A3A3A3; border-style: solid; border-width: 1pt; padding: 4pt 4pt 4pt 4pt; vertical-align: top; width: .6868in;">  <div style="font-family: Calibri; font-size: 11.0pt; margin: 0in; text-align: center;">success   </div></td>  <td style="border-color: #A3A3A3; border-style: solid; border-width: 1pt; padding: 4pt 4pt 4pt 4pt; vertical-align: top; width: .6847in;">  <div style="font-family: Calibri; font-size: 11.0pt; margin: 0in; text-align: center;">boolean   </div></td>  <td style="border-color: #A3A3A3; border-style: solid; border-width: 1pt; padding: 4pt 4pt 4pt 4pt; vertical-align: top; width: .6479in;">  <div style="font-family: Calibri; font-size: 11.0pt; margin: 0in; text-align: center;">True   </div></td> </tr><tr>  <td style="border-color: #A3A3A3; border-style: solid; border-width: 1pt; padding: 4pt 4pt 4pt 4pt; vertical-align: top; width: .7152in;">  <div style="font-family: Calibri; font-size: 11.0pt; margin: 0in;">reboot_required </div></td>  <td style="border-color: #A3A3A3; border-style: solid; border-width: 1pt; padding: 4pt 4pt 4pt 4pt; vertical-align: top; width: 3.9152in;">  <div style="font-family: Calibri; font-size: 11.0pt; margin: 0in;">True when the   target server requires a reboot to complete updates (no further updates can   be installed until after a reboot) </div></td>  <td style="border-color: #A3A3A3; border-style: solid; border-width: 1pt; padding: 4pt 4pt 4pt 4pt; vertical-align: top; width: .6868in;">  <div style="font-family: Calibri; font-size: 11.0pt; margin: 0in; text-align: center;">success   </div></td>  <td style="border-color: #A3A3A3; border-style: solid; border-width: 1pt; padding: 4pt 4pt 4pt 4pt; vertical-align: top; width: .6847in;">  <div style="font-family: Calibri; font-size: 11.0pt; margin: 0in; text-align: center;">boolean   </div></td>  <td style="border-color: #A3A3A3; border-style: solid; border-width: 1pt; padding: 4pt 4pt 4pt 4pt; vertical-align: top; width: .6479in;">  <div style="font-family: Calibri; font-size: 11.0pt; margin: 0in; text-align: center;">True   </div></td> </tr></tbody></table></div><div style="font-family: Calibri; font-size: 11.0pt; margin: 0in;">                                                                                               </div><div style="color: #595959; font-family: Calibri; font-size: 9.0pt; margin: 0in;">From &lt;<a href="http://docs.ansible.com/ansible/win_feature_module.html#support">http://docs.ansible.com/ansible/win_feature_module.html#support</a>&gt;&nbsp;</div>
