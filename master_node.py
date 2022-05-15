from absl import app, flags, logging
from concurrent import futures

import grpc
import master_comm_pb2
import master_comm_pb2_grpc
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


class MasterComm(master_comm_pb2_grpc.ReplicationServicer):
    # Functions for Gateway
    def NewNodeUpdate(self, request, context):
        logging.info(f"NewNodeUpdate invoked with request: {request}")
        if request.newnodeip:
            # Save new node to Redis DB
            redis_client.sadd(NETWORK_NODES, request.newnodeip)
            return master_comm_pb2.StatusResponse(master_comm_pb2.SUCCESS)
        else:
            logging.error("NewNodeUpdate invoked with empty request")
            return master_comm_pb2.StatusResponse(master_comm_pb2.FAILURE)

    def GetNodeForDownload(self, request, context):
        logging.info(f"GetNodeForDownload invoked with request: {request}")
        if request.filename:
            nodes = redis_client.smembers(NETWORK_DATA_FILE % request.filename)
            if nodes:
                # Return random node that contains the file
                node = random.choice(list(nodes))
                return master_comm_pb2.GetNodeForDownloadResponse(nodeip=node)
            else:
                return master_comm_pb2.GetNodeForDownloadResponse(nodeip="")
        else:
            logging.error("GetNodeForDownload invoked with empty request")
            return master_comm_pb2.GetNodeForDownloadResponse(nodeip="")

    def GetNodeForUpload(self, request, context):
        return master_comm_pb2.GetNodeForUploadResponse(nodeip="test0")

    # Functions for Sentinel
    def NodeDownUpdate(self, request, context):
        return master_comm_pb2.StatusResponse(master_comm_pb2.SUCCESS)

    # Functions for Node
    def GetNodeIpsForReplication(self, request, context):
        return master_comm_pb2.NodeIpsReply(nodeips=["test0", "test1"])

    def UpdateReplicationStatus(self, request, context):
        return master_comm_pb2.ReplicationDetailsResponse()

    # Functions for CLI
    def GetListOfFiles(self, request, context):
        logging.info(f"GetListOfFiles invoked with request: {request}")
        if request.nodeips:
            files = set()
            for node in request.nodeips:
                # Get list of files on node
                node_files = redis_client.smembers(NETWORK_NODE_DATA % node)
                files.update(node_files)

            return master_comm_pb2.GetListOfFilesResponse(files=list(files))
        else:
            # Return list of all files on the network
            files = redis_client.smembers(NETWORK_DATA)
            return master_comm_pb2.GetListOfFilesResponse(filenames = list(files))
        return master_comm_pb2.GetListOfFilesResponse()


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    master_comm_pb2_grpc.add_ReplicationServicer_to_server(MasterComm(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    server.wait_for_termination()


def setup_redis():
    """
    Setup Redis client
    """
    global redis_client
    try:
        redis_client = redis.Redis(host=FLAGS.redis_host, port=FLAGS.redis_port, password=FLAGS.redis_password, decode_responses=True)
    except Exception as e:
        logging.error("Error while connecting to redis: %s", e)
        exit(1)


def main(argv):
    logging.info("Setting up redis client...")
    setup_redis()
    logging.info("Starting gRPC server...")
    serve()


if __name__ == '__main__':
    app.run(main)
