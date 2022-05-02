# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

import node_comm_pb2 as node__comm__pb2


class NodeReplicationStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.CreateReplica = channel.stream_unary(
                '/stream.NodeReplication/CreateReplica',
                request_serializer=node__comm__pb2.CreateReplicaRequest.SerializeToString,
                response_deserializer=node__comm__pb2.CreateReplicaReply.FromString,
                )


class NodeReplicationServicer(object):
    """Missing associated documentation comment in .proto file."""

    def CreateReplica(self, request_iterator, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_NodeReplicationServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'CreateReplica': grpc.stream_unary_rpc_method_handler(
                    servicer.CreateReplica,
                    request_deserializer=node__comm__pb2.CreateReplicaRequest.FromString,
                    response_serializer=node__comm__pb2.CreateReplicaReply.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'stream.NodeReplication', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class NodeReplication(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def CreateReplica(request_iterator,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.stream_unary(request_iterator, target, '/stream.NodeReplication/CreateReplica',
            node__comm__pb2.CreateReplicaRequest.SerializeToString,
            node__comm__pb2.CreateReplicaReply.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)