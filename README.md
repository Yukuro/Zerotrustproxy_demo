# Zeme  -  Zero-trust proxy (Experimental)
Zeme is a tool to implement the zero-trust network concept in your home network.
<br/>
(It's an experimental version, and the home network could be invaded...)

## Demo
1. Launch target server
    ```sh
    python be_attacked_server.py # Yarare-server
    ```
2. Launch proxy(incruding trust inference)
    ```sh
    python proxy.py
    ```
3. Turn on the proxy in your OS
    - (in my case)
        - 127.0.0.1:8080
4. Launch attacker script
    ```sh
    python attacker.py #It isn't open to prevent misuse.
    ```
5. You can see Attacker's trust score go down in proxy.py
## Requirements
- This script does not require any external dependencies, except for the standard library (for now)

## Note
- In the current version, the following attack can be prevented
    - only F5 attack (through HTTP)
