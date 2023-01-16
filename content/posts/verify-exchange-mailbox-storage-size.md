---
title: "Verify Exchange Mailbox Storage Size"
date: 2012-12-12
draft: false
---

Microsoft best practices recommend than an Exchange Mail Store does not surpass the 75GB limit. A Typical Exchange server has many Mailbox Store. When you create a mailbox, it’s important to use a store not bigger than 75GB. Here is how to find out the size of each store.

Start Exchange System Manager, Browse to the mailbox store you want to check.
```
Root -> Administrative Groups -> Location -> Servers -> ServerName -> The Storage Group -> The mailbox Store.
```
Right click the store --> properties --> go to Databased tab
Locate the path to the exchaneg databse (edb) file and streaming database (stm) file.
The size of both files together is the current mailbox storage size.
