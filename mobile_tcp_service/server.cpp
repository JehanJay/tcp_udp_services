#include <iostream>
#include <sys/types.h>
#include <unistd.h>
#include <sys/socket.h>
#include <netdb.h>
#include <arpa/inet.h>
#include <string.h>
#include <string>

using namespace std;


int main()
{
    // Create a socket
    int listening = socket(AF_INET, SOCK_STREAM, 0); //AF_INET6 for ipv6
    if (listening == -1)
    {
        cerr << "ERROR: Cannot create a socket! Quitting" << endl;
        return -1;
    }
 
    // Bind the ip address and port to a socket
    sockaddr_in hint; //sockaddr_in6 for ipv6
    hint.sin_family = AF_INET;
    hint.sin_port = htons(1441); //54000 
    inet_pton(AF_INET, "0.0.0.0", &hint.sin_addr);
 
    if (bind(listening, (sockaddr*)&hint, sizeof(hint)) == -1)
    {
      cerr << "ERROR: Cannot bind to IP / Port!";
      return -2;
    }

    if (listen(listening, SOMAXCONN) == -1)
    {
      cerr << "ERROR: Cannot listen! ";
      return -3;
    }
    
    cout << "Socket created and Server: Listening.." << endl;

    // bind(listening, (sockaddr*)&hint, sizeof(hint));
    // listen(listening, SOMAXCONN);
 
    // Wait for a connection
    sockaddr_in client;
    socklen_t clientSize = sizeof(client);
 
    int clientSocket = accept(listening, (sockaddr*)&client, &clientSize);
 
    char host[NI_MAXHOST];      // Client's remote name
    char service[NI_MAXSERV];   // Service (i.e. port) the client is connect on

    if (clientSocket == -1)
    {
      cerr << "ERROR: Problem with client connecting!";
      return -4;
    } 


    memset(host, 0, NI_MAXHOST); // cleans garbage;
    memset(service, 0, NI_MAXSERV);

    if (getnameinfo((sockaddr*)&client, sizeof(client), host, NI_MAXHOST, service, NI_MAXSERV, 0) == 0)
    {
        cout << host << " OK: Connected on port: " << service << endl;
    }
    else
    {
        inet_ntop(AF_INET, &client.sin_addr, host, NI_MAXHOST);
        cout << host << " OK: Connected on port manually: " << ntohs(client.sin_port) << endl;
    }
 
    // Close listening socket
    close(listening);
 
    // While loop: accept and echo message back to client
    char buf[4096];
 
    while (true)
    {
        memset(buf, 0, 4096); // clear the buffer
 
        // Wait for client to send data
        int bytesReceived = recv(clientSocket, buf, 4096, 0); // wait for message
        if (bytesReceived == -1)
        {
            cerr << "Error in recv(). Quitting" << endl;
            break;
        }
 
        if (bytesReceived == 0)
        {
            cout << "Client disconnected " << endl;
            break;
        }
 
        //Display message
        cout << "Received: " << string(buf, 0, bytesReceived);

        // Echo ACK back to client 
        (void)strncpy(buf, "ACK Received \n", sizeof(buf)); // avoid this to send the received message again
        if (send(clientSocket, buf, bytesReceived + 15, 0))
        {
          cout << "ACK sent back to the port: " << service << endl;
        }    
    }
 
    // Close the socket
    close(clientSocket);
 
    return 0;
}