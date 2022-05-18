"""
Master Node implementation in Python3 for Space Opera
"""

from absl import app, flags, logging
from concurrent import futures

import grpc
import master_comm_pb2
import master_comm_pb2_grpc
import node_comm_pb2
import node_comm_pb2_grpc
import random
import redis

# Redis configuration
REDIS_HOST = "localhost"
REDIS_PORT = 6379
REDIS_PASSWORD = ""

# Redis keys
NETWORK_NODES = "network:nodes"
NETWORK_DATA = "network:data"
NETWORK_NODE_DATA = "network:data:node:%s"
NETWORK_DATA_FILE = "network:data:file:%s"

# Constants
REPLICATION_FACTOR  = 3

# Absl flags
FLAGS = flags.FLAGS

flags.DEFINE_string('redis_host', REDIS_HOST, 'Redis host')
flags.DEFINE_integer('redis_port', REDIS_PORT, 'Redis port')
flags.DEFINE_string('redis_password', REDIS_PASSWORD, 'Redis password')
flags.DEFINE_integer('replication_factor', REPLICATION_FACTOR, 'Replication factor for Space Opera network')


# Redis client that will store all network node and file information
redis_client = None


class NodeComm(node_comm_pb2_grpc.NodeReplicationServicer):
    def ReplicateFile(self, request, context):
        logging.info(f"ReplicateFile invoked with request: {request}")
        return master_comm_pb2.ReplicateFileResponse(status = "SUCCESS")


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    node_comm_pb2_grpc.add_NodeReplicationServicer_to_server(NodeComm(), server)
    server.add_insecure_port('[::]:50052')
    server.start()
    server.wait_for_termination()


def main(argv):
    logging.info("Starting gRPC server...")
    serve()


if __name__ == '__main__':
    app.run(main)
