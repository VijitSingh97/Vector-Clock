# Vector Clock

## Overview

Vector clock implementation by Vijit Singh.
Features:

- flask endpoint receiving message from other servers
- requests with counter information are sent randomly to a server every 15 seconds
- internal events occur every 15 seconds

Counter is printed before and after every internal event, message is received, or message is sent.

## Running this project

This project has been hardcoded in several places to use exactly 3 servers

To start all three servers:

``` bash
./start.sh
```

To stop all three servers:

``` bash
./stop.sh
```
