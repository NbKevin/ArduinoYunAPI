## Hearty: Server

_**Hearty**_ is a final project for the course _Solar Solution_ of _Interactive Media Arts_ at NYU Shanghai. It is a wearable heart rate monitor powered by a polycrystalline silicon solar panel. Data collected will be transmitted through the on-board Wifi chip of _Arduino Yun_ to the server and then be retrieved for further analysis.

This repository contains the code responsible for the server. It is written in _Python_ and built upon _Flask_ framework to process HTTP requests. _Mongo DB_ and its adapter drivers are used for manipulating the database.

#### Launching the server

This repository itself can be opened as a _PyCharm_ project. Users of _PyCharm_ can directly clone the repository, open it and launch the `yun_api`.

Alternatively, just clone it and launch the `yun_api.py` file with a _Python_ executable of version `3.0` or higher.

#### Arduino Sketch

The server expects the _Arduino Yun_ to send data in certain format as described in the file `yun/heart_rate_adapter.py`. Corresponding sketch can be found at `yun/heart_rate_json_bridge.ino` with detailed documentation.

#### Licence and more

This project, as referred to by the name _**Hearty**_, releases its code part under the licence of Apache 2.0. You can find more information on the [documentation site](http://ima.nyu.sh/documentation) of _Interactive Media Arts_.

> Copyright 2015, Nb/Kevin<bn628@nyu.edu>
>
>  Licensed under the Apache License, Version 2.0 (the "License");
>  you may not use this file except in compliance with the License.
>  You may obtain a copy of the License at
>
>      http://www.apache.org/licenses/LICENSE-2.0
>
>  Unless required by applicable law or agreed to in writing, software
>  distributed under the License is distributed on an "AS IS" BASIS,
>  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
>  See the License for the specific language governing permissions and
>  limitations under the License.
