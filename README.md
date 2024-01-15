To run part 2, follow the next steps:

Prerequisites:
(note: since python3 is preinstalled we don't need to install it)

- python3 -m ensurepip --upgrade
- pip install bcrypt
- pip install web_interface
- sudo apt install git-all
- git clone https://github.com/luc1an24/luxonis.git

Now we move into the cloned luxonis directory.

How to run:
- To start the server execute the following command:  python3 luxnonis/part2/main.py
- To start each client execute the following command: python3 luxnonis/part2/client.py

Known issues: 
- Clients don't have automatic listening mode, therefore to receive a new message a client command must be first triggered
- Client hint is not sent to the opponent client
- Client doesn't have knowledge if he is the first or second player therefore any one of the players can guess word
- Currently password, tcp port and tcp host are hardcoded for easier testing purposes
- Currently only TCP sockets are supported
- Web interface doesn't work as it should -> no response is returned on GET request
