# Contiki CoAP CLI

## Requirement
* Python 2.7
* pip

## Installing
* pip install -r requirements.txt

## Database Connection
* Please copy `example.cfg` and rename it to `config.cfg`. The programe will read this file to connect the mysql database.

## Command Line
* getallmotes
    * Ex : getallmotes fd00::201:1:1:1
    * (get all motes address from host, then created list table)

* list
    * Ex : list
    * (show current list, not last new, if you want new table, just run getallmotes again)

* post
    * Ex : post fd00::202:2:2:2 bcollect thd=5&pp=2
    * (post node's resource and query to node)

* postall
    * Ex : postall bcollect thd=5&pp=2
    * (postall resource and query to nodes)

* observe
    * Ex : observe fd00::202:2:2:2 bcollect
    * (observing bcollect resource)

* observeall
    * Ex : observeall
    * (auto observing all node's bcollect resource.)

* observelist
    * Ex : observelist
    * (show current observing list)

* delete
    * Ex : delete fd00::202:2:2:2
    * (cancel observing node)

* auto
    * Ex : auto start
    * (will auto start observing node, if off-link node, can auto reobserve.)
    * Ex : auto start 60
    * (60 number is check observe timer, you can set any number, not string.)
    * Ex : auto stop
    * (canceling auto function.)

* quit
    * Ex : quit
    * (exiting tool, it will auto cancel observing nodes)