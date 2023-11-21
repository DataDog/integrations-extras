# CHANGELOG - bind9_check

## 0.1.0

***Added***:

* first version

## 1.0.1

***Added***

* Ability to define custom tags at the instance level
* Ability to define a timeout for the DNS stats endpoint in `init_config`

***Fixed***

* Logical error where service check was "OK" even if it can't connect, causing two service checks to be posted
* Any unreachable DNS stats endpoint caused the agent to hang indefinitely waiting for the request to finish

***Changed***

* Minor changes to the format of the example config file
* Instance parameter "url" and its value will always be added as a tag for each instance
