# relay_node_simulations
Simulations of using a relay node to send information from a source to a server. There is a service time created by the server

Source -> RelayNode -> Server -> sink

The relay node acts as a buffer. 
When the contents of the buffer are transmitted to the server, a batch is created with all of the requests in the buffer, and the batch is sent over to the server. 
The server will process the batch and assign it a service time. 
