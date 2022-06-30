#include <fcntl.h>
#include <string.h>
#include <stdlib.h>
#include <errno.h>
#include <stdio.h>
#include <netinet/in.h>
#include <resolv.h>
#include <sys/socket.h>
#include <arpa/inet.h>
#include <unistd.h>
#include <pthread.h>
#include "hello.pb.h"
#include <iostream>
#include <proto_serialize.hpp>
#include <google/protobuf/io/coded_stream.h>
#include <google/protobuf/io/zero_copy_stream_impl.h>
#include <google/protobuf/message.h>
#include <google/protobuf/descriptor.h>
#include <google/protobuf/io/zero_copy_stream_impl_lite.h>

using namespace std;
using namespace google::protobuf::io;

void *SocketHandler(void *);

class ProtoServerDeclare{
        public:        
                int host_port;
                int hsock;
                int *p_int;
                int err;
                int *csock;
};

class ProtoClientDeclare{
        public:        
                int host_port_client;
                char *host_name;
                int bytecount_client;
                int hsock_client;
                int *p_int_client;
                int err_client;
};

class ProtoTransceiveInitializer{
        public:
                int serverBinder(int host_port, int hsock, int *p_int, int err);
                int clientBinder(char *host_name, int host_port_client, int hsock_client, int *p_int_client, int err_client);
                int transceiveExecuter(int hsock, int *csock,  int err, int hsock_client, int bytecount_client);
};

int ProtoTransceiveInitializer::serverBinder(int host_port, int hsock, int *p_int, int err) {
        struct sockaddr_in my_addr;
        if (hsock == -1)
              {
                      printf("Error initializing socket %d\n", errno);
                      return -1;
              }
              p_int = (int *)malloc(sizeof(int));
              *p_int = 1;
              if ((setsockopt(hsock, SOL_SOCKET, SO_REUSEADDR, (char *)p_int, sizeof(int)) == -1) ||
                  (setsockopt(hsock, SOL_SOCKET, SO_KEEPALIVE, (char *)p_int, sizeof(int)) == -1))
              {
                      printf("Error setting options %d\n", errno);
                      free(p_int);
                      return -2;
              }
              free(p_int);
              my_addr.sin_family = AF_INET;
              my_addr.sin_port = htons(host_port);
              memset(&(my_addr.sin_zero), 0, 8);
              my_addr.sin_addr.s_addr = INADDR_ANY;
              if (bind(hsock, (sockaddr *)&my_addr, sizeof(my_addr)) == -1)
              {
                      fprintf(stderr, "Error binding to socket, make sure nothing else is listening on this port %d\n", errno);
                      return -3;
              }
              if (listen(hsock, 10) == -1)
              {
                      fprintf(stderr, "Error listening %d\n", errno);
                      return -4;
              }
              

}

int ProtoTransceiveInitializer::clientBinder(char *host_name, int host_port_client, int hsock_client, int *p_int_client, int err_client) {
        struct sockaddr_in my_addr_client;
        if (hsock_client == -1)
        {
                printf("Error initializing socket %d\n", errno);
                return -1;
        }

        p_int_client = (int *)malloc(sizeof(int));
        *p_int_client = 1;

        if ((setsockopt(hsock_client, SOL_SOCKET, SO_REUSEADDR, (char *)p_int_client, sizeof(int)) == -1) ||
            (setsockopt(hsock_client, SOL_SOCKET, SO_KEEPALIVE, (char *)p_int_client, sizeof(int)) == -1))
        {
                printf("Error setting options %d\n", errno);
                free(p_int_client);
                return -2;
        }

        free(p_int_client);
        my_addr_client.sin_family = AF_INET;
        my_addr_client.sin_port = htons(host_port_client);
        memset(&(my_addr_client.sin_zero), 0, 8);
        my_addr_client.sin_addr.s_addr = inet_addr(host_name);

        if (connect(hsock_client, (struct sockaddr *)&my_addr_client, sizeof(my_addr_client)) == -1)
        {
                if ((err_client = errno) != EINPROGRESS)
                {
                        fprintf(stderr, "Error connecting socket %d\n", errno);
                        return -3;
                }
        }
}
                                                
int ProtoTransceiveInitializer::transceiveExecuter(int hsock, int *csock,  int err, int hsock_client, int bytecount_client) {
        socklen_t addr_size = 0;
        sockaddr_in sadr;
        pthread_t thread_id = 0;
        addr_size = sizeof(sockaddr_in);

        while (true)
        {
                printf("Waiting for a client connection..\n");
                csock = (int *)malloc(sizeof(int));
                if ((*csock = accept(hsock, (sockaddr *)&sadr, &addr_size)) != -1)
                {
                        printf("---------------------\nReceived connection from %s\n", inet_ntoa(sadr.sin_addr));
                        pthread_create(&thread_id, 0, &SocketHandler, (void *)csock);
                        pthread_detach(thread_id);
                }
                else
                {
                        fprintf(stderr, "Error accepting %d\n", errno);
                }

                opa3l::Person payload;
                payload.set_name("JehanTransceive");
                payload.set_id(27);   
                payload.set_email("drives@uni-bremen.de");

                cout << "Size after serilizing the proto message: " << payload.ByteSize() << endl;
                int siz = payload.ByteSize() + 4;
                char *pkt = new char[siz];
                google::protobuf::io::ArrayOutputStream aos(pkt, siz);
                CodedOutputStream *coded_output = new CodedOutputStream(&aos);
                coded_output->WriteVarint32(payload.ByteSize());
                drives::proto::Serialized protoMessage = drives::proto::Serialized(payload);
                
                if ((bytecount_client = send(hsock_client, (void *)protoMessage.get_ptr(), protoMessage.get_size(), 0)) == -1)
                {
                        fprintf(stderr, "Error sending data %d\n", errno);
                        return -1;
                } else {
                printf("[%i] Server found.. Sent the proto msg as bytes with size: %d\n ", bytecount_client);
                }
                usleep(1);
                delete pkt;
                // close(hsock_client);
        }
}

int main(int argv, char **argc)
{
        ProtoServerDeclare server;
        ProtoClientDeclare client;
        ProtoTransceiveInitializer transceiveInitializer;

        //SERVER
        server.host_port = 1102;
        server.hsock = socket(AF_INET, SOCK_STREAM, 0);


        //CLIENT 
        client.host_port_client = 1101;
        client.host_name = (char *)"127.0.0.1"; 
        client.hsock_client = socket(AF_INET, SOCK_STREAM, 0);

        //SERVER CONNECTIVITY BINDING
        transceiveInitializer.serverBinder(server.host_port, server.hsock, server.p_int, server.err);

        //CLIENT CONNECTIVITY BINDING
        transceiveInitializer.clientBinder(client.host_name, client.host_port_client, client.hsock_client, client.p_int_client, client.err_client);

        //TRANSCEIVE EXECUTION
        transceiveInitializer.transceiveExecuter(server.hsock, server.csock, server.err, client.hsock_client, client.bytecount_client);

FINISH:;
}

void *SocketHandler(void *lp)
{
        int *csock = (int *)lp;
        char buffer[1000];
        int bytecount = 0;
        string output, pl;
        while (1)
        {
                if ((bytecount = recv(*csock,
                                      buffer,
                                      1000, MSG_PEEK)) == -1)
                {
                        fprintf(stderr, "Error receiving data %d\n", errno);
                }
                else if (bytecount == 0)
                        break;
                const auto payload_received = drives::proto::parseFromArray<opa3l::Person>((void *)buffer, 1000);
                cout << "Payload received:  \n" << payload_received.DebugString() << endl;
                        
                // system("./../../proto_socket/worhp/cpp-example");
                // system("./spline0");
                // system("./../../transworhp/spline0");
                // system("./../../proto_socket/spline0");
                break;
        }

FINISH:
        free(csock);
        return 0;
}

