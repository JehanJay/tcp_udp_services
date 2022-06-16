#pragma once

#include <google/protobuf/any.pb.h>
#include <malloc.h>

#include <cstddef>
#include <cstring>

#ifndef DllExport
#    ifdef _WIN32
#        define DllExport __declspec( dllexport )
#    else
#        define DllExport
#    endif
#endif

namespace drives {

namespace proto {


template<typename M>
static google::protobuf::Any
msgToAny( const M& msg )
{
    google::protobuf::Any any;
    any.PackFrom( msg );
    return any;
}

template<typename M>
static M
parseFromAny( const google::protobuf::Any& msg )
{
    M result;
    if( msg.Is<M>() ) {
        msg.UnpackTo( &result );
    }
    return result;
}

template<typename M>
static M
parseFromArray( const void* msg, size_t size )
{
    M result;

    google::protobuf::Any any;
    any.ParseFromArray( msg, static_cast<int>( size ) );
    return parseFromAny<M>( any );
}

template<typename M>
static bool
is( const void* msg, size_t size )
{
    google::protobuf::Any any;
    any.ParseFromArray( msg, static_cast<int>( size ) );

    return any.Is<M>();
}

class DllExport Serialized {
public:
    // Constructor for Proto Messages that are not Any
    template<typename M>
    explicit Serialized( const M& msg )
    {
        google::protobuf::Any anyMsg = msgToAny( msg );
        size                         = anyMsg.ByteSizeLong();
        ptr                          = malloc( size );
        memoryAllocated              = true;
        anyMsg.SerializeToArray( ptr, static_cast<int>( size ) );
    }

    // Constructor for Any messages
    explicit Serialized( const google::protobuf::Any& msg ) : size( msg.ByteSizeLong() ), ptr( malloc( size ) ), memoryAllocated( true )
    {
        msg.SerializeToArray( ptr, static_cast<int>( size ) );
    }
    Serialized( void* buf, size_t size, bool copyMemory ) : size( size ), memoryAllocated( copyMemory )
    {
        if( copyMemory ) {
            ptr = malloc( size );
            memcpy( ptr, buf, size );
        } else {
            ptr = buf;
        }
    }
    ~Serialized()
    {
        if( memoryAllocated ) {
            free( ptr );
        }
    }
    Serialized( const Serialized& ) = delete;
    Serialized( Serialized&& other ) noexcept : size( other.size ), ptr( other.ptr ), memoryAllocated( other.memoryAllocated )
    {
        other.ptr = nullptr;
    }

    Serialized& operator=( const Serialized& ) = delete;
    Serialized& operator                       =( Serialized&& other ) noexcept
    {
        if( this != &other ) {
            ptr             = other.ptr;
            size            = other.size;
            other.ptr       = nullptr;
            memoryAllocated = other.memoryAllocated;
        }

        return *this;
    }


    template<typename M>
    M toMsg() const
    {
        return parseFromArray<M>( ptr, size );
    }

    void printDebug()
    {
        if( cached_any ) {
            std::cout << cached_any->ShortDebugString() << std::endl;
        }
    }

    template<typename M>
    bool Is()
    {
        if( cached_any ) {
            return cached_any->Is<M>();
        } else {
            google::protobuf::Any a;
            a.ParseFromArray( ptr, (int)size );
            cached_any = std::unique_ptr<google::protobuf::Any>( new google::protobuf::Any( a ) );
            return cached_any->Is<M>();
        }
    }

    std::size_t get_size() const noexcept { return size; }

    void* get_ptr() const noexcept { return ptr; }

private:
    std::size_t                            size = 0;
    void*                                  ptr  = nullptr;
    bool                                   memoryAllocated;
    std::unique_ptr<google::protobuf::Any> cached_any;
};

// template<typename... Values>
// DllExport Serialized toSerialized(Values... values); // Proto Developers: implement this for your message!

}  // namespace proto

}  // namespace drives
