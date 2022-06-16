#include <unistd.h>
#include "hello.pb.h"
#include <proto_serialize.hpp>
#include <iostream>
#include <sys/socket.h>
#include <netinet/in.h>
#include <arpa/inet.h>
#include <google/protobuf/message.h>
#include <google/protobuf/descriptor.h>
#include <google/protobuf/io/zero_copy_stream_impl.h>
#include <google/protobuf/io/coded_stream.h>
#include <google/protobuf/io/zero_copy_stream_impl_lite.h>

using namespace google::protobuf::io;

using namespace std;

int main(int argv, char **argc)
{

        /* Coded output stream */

        opa3l::Person payload;
        payload.set_name("Jehan");
        payload.set_id(26);   
        payload.set_email("jehan@uni-bremen.de");

        cout << "size after serilizing is " << payload.ByteSize() << endl;
        int siz = payload.ByteSize() + 4;
        char *pkt = new char[siz];
        google::protobuf::io::ArrayOutputStream aos(pkt, siz);
        CodedOutputStream *coded_output = new CodedOutputStream(&aos);
        coded_output->WriteVarint32(payload.ByteSize());

        // payload.SerializeToCodedStream(coded_output);
        drives::proto::Serialized protoMessage = drives::proto::Serialized(payload);
        

        int host_port = 1101;
        char *host_name = (char *)"127.0.0.1";

        struct sockaddr_in my_addr;

        char buffer[1024];

        int bytecount;
        int buffer_len = 0;
        int hsock;
        int *p_int;
        int err;

        hsock = socket(AF_INET, SOCK_STREAM, 0);

        if (hsock == -1)
        {
                printf("Error initializing socket %d\n", errno);
                goto FINISH;
        }

        p_int = (int *)malloc(sizeof(int));
        *p_int = 1;

        if ((setsockopt(hsock, SOL_SOCKET, SO_REUSEADDR, (char *)p_int, sizeof(int)) == -1) ||
            (setsockopt(hsock, SOL_SOCKET, SO_KEEPALIVE, (char *)p_int, sizeof(int)) == -1))
        {
                printf("Error setting options %d\n", errno);
                free(p_int);
                goto FINISH;
        }

        free(p_int);
        my_addr.sin_family = AF_INET;
        my_addr.sin_port = htons(host_port);
        memset(&(my_addr.sin_zero), 0, 8);
        my_addr.sin_addr.s_addr = inet_addr(host_name);

        if (connect(hsock, (struct sockaddr *)&my_addr, sizeof(my_addr)) == -1)
        {
                if ((err = errno) != EINPROGRESS)
                {
                        fprintf(stderr, "Error connecting socket %d\n", errno);
                        goto FINISH;
                }
        }

        for (int j = 0; j < 10; j++)
        {
                // if ((bytecount = send(hsock, (void *)pkt, siz, 0)) == -1)
                // {
                //         fprintf(stderr, "Error sending data %d\n", errno);
                //         goto FINISH;
                // }
                if ((bytecount = send(hsock, (void *)protoMessage.get_ptr(), protoMessage.get_size(), 0)) == -1)
                {
                        fprintf(stderr, "Error sending data %d\n", errno);
                        goto FINISH;
                }
                printf("[%i] Sent the proto msg as bytes with size %d\n", j, bytecount);
                usleep(1);
        }

        delete pkt;

FINISH:
        close(hsock);
}