
# Networked Tsuro Implementation 

This project was built with Upasna Madhok during NU's Spring 2018 Software Construction course. It is built exclusively with Python. 

[Tsuro](https://boardgamegeek.com/boardgame/16992/tsuro) is a 2-8 player board game, where players take turns laying tiles adjacent eachother on the board. Each tile is unique and has a set of paths that connect with the paths of the other tiles. A path may lead off the game board. The objective of the game is to place your tiles such that you eliminate other players by forcing them off the board and become the last player in the game.

It includes two main things:
* A **game server** that accepts connections by game players at a specified port. This server executes legal game play by identifiying valid moves, maintaining and updating the state of the game, and removing cheating players.
* Simple heuristic based **automated players** that can connect to the server and select various moves. 

The server and automated players commmunicate with eachother via paired XML messages encoded as bytes sent over the socket connection. The XML grammar used to define messages sent over the wire was specified by the instructor. When a message is sent from one entity to the other, the other entity must receive the full message, decode the XML message and convert the data to Python data structures, update the data structures, and select and construct a valid XML message to send back. Most of this work happens in `obj2xml.py` and `xml2obj.py` in /src.

* To install necessary requirements, type `make setup`
* To run tests, type `make test`
* To run a Tsuro tournament locally (not over the wire) with automated players, type `make tournament`

To connect our automated player implementation to another Tsuro server programmed to communicate with XML over a socket connnection, cd into src and run `python3 networkAdministrator [name-of-player] [host] [port]`

To run our tournament server and accept connections from other automated players, cd into src and run `python3 networkedGame [port]`

## Todos:
* add a GUI and support for a human input
* devise more sophisticated automated players
