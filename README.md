# Markdown syntax guide

## Benchmarking
The aim of this project is to conduct benchmarking to assess the performance of different websocket libraries. Different techniques are used for different cases throughout the benchmarking process.

## Test Environment
- CPU: Intel Core i7-9750H 2.60GHz
- RAM: 16 GB
- Operating System: Windows 10 Pro
- Number of Threads: 1

## Servers
Two different libraries are used for server implementations:
- Autobahn
- Socketify

## Clients
Two different libraries are used for client implementations:
- Autobahn
- Websocket-Client

Additionally, the results of a sync **Websockets** client will be provided in the following sections.

## Tests
Tests are conducted to measure the maximum throughput of the servers, connection time, and evaluate the behavior of the servers when multiple clients are connected (scalability). It was challenging to find the limiting factor for each test. Also, external factors affect the results of the tests. But some methods are used to overcome these challenges. Details will be provided in the related chapter.

## Autobahn Server

Autobahn server implementation is constructed on the Twisted asynchronous networking library. The simple example from the original repository of the library is used for implementing a basic server that continuously broadcasts a message, including the sequence number of the message in string format.

### Test Results

| Client Library | Number of Clients | Total number of packages received (20 secs) |
| -------------- | ----------------- | ------------------------------------------- |
| Autobahn        | 1                 | 512224                                      |
| Autobahn        | 8                 | 571719                                      |
| Autobahn        | 16                | 446813                                      |
| Autobahn        | 4(M)              | 532792                                      |
| Autobahn        | 6(M)              | 415334                                      |

M indicates multiple processes for different clients. The test script is used in those test cases.

The test indicates the following results:
The average number of packets that an Autobahn server can send is 25224 per second (504482 packets in approximately 20 secs).

The server is capable of handling successful connections up to 16 clients. Most probably more clients are also possible, but the number of packages that are sent by the server is decreasing with the increasing number of clients. Therefore, though the connection is successful, the performance is decreasing linearly with the increasing number of clients.

Actually, the number of packages sent by the server is higher, but since some packages are dropped most probably because of buffering issues, I only reported the number of packages successfully transmitted.

## Socketify Server

Socketify server implementation is constructed on uWebSocket, a networking library written in C++. The simple example from the original repository of the library is used for implementing a basic server. The broadcast functionality is added to that implementation to continuously broadcast a message including the timestamp in seconds.

### Test Results

| Client Library | Number of Clients | Total number of packages received (20 secs) |
| -------------- | ----------------- | ------------------------------------------- |
| Socketify      | 1                 | 414574                                      |
| Socketify      | 2(M)              | 751007                                      |
| Socketify      | 4(M)              | 1281229                                     |
| Socketify      | 6(M)              | 1640598                                     |

M indicates multiple processes for different clients. The test script is used in those test cases.

The first two results are not included in the average calculation since the limiting factor is the client side in that case.

The test indicates the following results:
The average number of packets that a Socketify server can send is 73195 per second (1463913 packets in approximately 20 secs).

The server is capable of handling successful connections up to 16 clients. Most probably more clients are also possible, but the number of packages that are sent by the server is decreasing with the increasing number of clients. Therefore, though the connection is successful, the performance is decreasing linearly with the increasing number of clients, just like the Autobahn Server.

Actually, the number of packages sent by the server is quite higher, but since some packages are dropped, most probably because of buffering issues, I only reported the number of packages successfully transmitted to the client side. The dropping rate is pretty high compared to the Autobahn websocket server.

## Autobahn Client

Autobahn client implementation used is constructed using Asyncio and Twisted in Python. The simple example from the original repository of the library is used for implementing a basic client. The client is further developed for logging the results and asynchronously running multiple clients to test the scalability of the servers.

### Test Results

| Server Library | Number of Clients | Number of packages received per client (20 secs) |
| -------------- | ----------------- | ------------------------------------------------- |
| Socketify      | 1                 | 414574                                            |
| Socketify      | 2(M)              | 375503                                            |
| Socketify      | 4(M)              | 320307                                            |
| Socketify      | 6(M)              | 273433                                            |
| Autobahn       | 1                 | 414656                                            |
| Autobahn       | 4(M)              | 133198                                            |
| Autobahn       | 6(M)              | 69222                                             |

Only the first two results for Socketify server and the first result for Autobahn server give a valid idea about the performance of the client. The limiting factor at the other results is the server side. Therefore, we can indicate that the number of packets received by the client is 20078 on average (401577 in 20 secs).

## Websocket Client

Autobahn client implementation is written in Python. The simple example from the original repository of the library is used for implementing a basic client. The client is further developed for logging the results and asynchronously running multiple clients to test the scalability of the servers.

| Server Library | Number of Clients | Number of packages received per client (20 secs) |
| -------------- | ----------------- | ------------------------------------------------- |
| Socketify      | 1                 | 627                                               |
| Socketify      | 8                 | 623                                               |
| Socketify      | 16                | 623                                               |
| Autobahn       | 1                 | 625                                               |
| Autobahn       | 8                 | 562                                               |
| Autobahn       | 16                | 548                                               |

All the results are taken into account since the limiting factor is always the client side. We can indicate that the number of packets received by the client is 30 per second on average (601 in 20 secs).

Though the connection time is pretty short when it connects to the Socketify, it takes approximately 2 seconds when it tries to connect to the Autobahn server.

## Comparison of The Performance of Servers

In terms of throughput, Socketify performs approximately 3 times better than the Autobahn. Since the autobahn-python is a pure python implementation, the difference in the performance is understandable.

The connection time of the clients to the servers is not reported explicitly, but the connection times are similar.

In terms of scalability, both servers are performing worse as the number of clients is increased. The total number of packages that a server can send is stated above and since they cannot exceed this limit, the number of packages sent to a client decreases as the number of clients increases. So to use the clients with the maximum performance, the number of clients connected to the a server should be kept at a minimum. (For Autobahn client, Socketify can handle 3 clients and Autobahn can handle 1 client according to test results if we want to run the clients with the maximum performance)

## Comparison of The Performance of Clients

Clearly, Autobahn performs far more better than the websocket-client implementation. Both libraries are implemented in Python, but most probably websocket-client is not optimized and for that reason, it's performing poorly. Also, connection time of the websocket-client to the different servers is not consistent.

## Websockets Synchronous Client

Lastly, I wanted to test a synchronous client of the websockets library. The number of received packets is 17415 on average (348319 packets in 20 secs). Since two clients are adequate, I do not provide details for this one, but I wanted to add this one as well since websockets is one of the most popular libraries.
