"""
Master Node implementation in Python3 for Space Opera
"""

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
        """
        NewNodeUpdate is invoked when a new node joins the network
        Invoked by Gateway
        """
        logging.info(f"NewNodeUpdate invoked with request: {request}")
        if request.newnodeip:
            # Save new node to Redis DB
            redis_client.sadd(NETWORK_NODES, request.newnodeip)
            return master_comm_pb2.NewNodeUpdateResponse(status = "SUCCESS")
        else:
            logging.error("NewNodeUpdate invoked with empty request")
            return master_comm_pb2.NewNodeUpdateResponse(status = "FAILURE")


    def GetNodeForDownload(self, request, context):
        """
        GetNodeForDownload is invoked when a client wants to download a file
        Invoked by Gateway
        """
        logging.info(f"GetNodeForDownload invoked with request: {request}")
        if request.filename:
            nodes = redis_client.smembers(NETWORK_DATA_FILE % request.filename)
            if nodes:
                # Return random node that contains the file
                node = random.choice(list(nodes))
                return master_comm_pb2.GetNodeForDownloadResponse(nodeip=node)
            else:
                return master_comm_pb2.GetNodeForDownloadResponse()
        else:
            logging.error("GetNodeForDownload invoked with empty request")
            return master_comm_pb2.GetNodeForDownloadResponse()


    def GetNodeForUpload(self, request, context):
        """
        GetNodeForUpload is invoked when a client wants to upload a file
        Invoked by Gateway
        """
        logging.info(f"GetNodeForUpload invoked with request: {request}")
        if request.filename:
            # Build mapping of nodes to number of files stored on them
            nodes = {}
            for node in redis_client.smembers(NETWORK_NODES):
                nodes[node] = len(redis_client.smembers(NETWORK_NODE_DATA % node))

            # Sort nodes by number of files stored on them
            sorted_nodes = sorted(nodes.items(), key=lambda x: x[1])

            # Node with least number of files
            node_ip = sorted_nodes[0][0]

            redis_client.sadd(NETWORK_DATA, request.filename)
            redis_client.sadd(NETWORK_NODE_DATA % node_ip, request.filename)
            redis_client.sadd(NETWORK_DATA_FILE % request.filename, node_ip)

            return master_comm_pb2.GetNodeForUploadResponse(nodeip = node_ip)
        else:
            logging.error("GetNodeForUpload invoked with empty request")
            return master_comm_pb2.GetNodeForUploadResponse()


    # Functions for Sentinel
    def NodeDownUpdate(self, request, context):
        """
        NodeDownUpdate is invoked when a node is unresponsive as detected by the Sentinel
        Invoked by Sentinel
        """
        logging.info(f"NodeDownUpdate invoked with request: {request}")
        if request.nodeip:
            # Replicate all the files stored on the node
            files = redis_client.smembers(NETWORK_NODE_DATA % request.nodeip)
            for file in files:
                replica_nodes = redis_client.sdiff(NETWORK_NODES, NETWORK_DATA_FILE % file)
                replica_node = random.choice(list(replica_nodes))
                # TODO: Send message to node to replicate file to replica_node
                
               
        with grpc.insecure_channel('localhost:50051') as channel:
         stub = helloworld_pb2_grpc.GreeterStub(channel)
         response = stub.SayHello(helloworld_pb2.HelloRequest(name='you'))
         print("Greeter client received: " + response.message)
         response = stub.SayHelloAgain(helloworld_pb2.HelloRequest(name='you'))
         print("Greeter client received: " + response.message)
        
                logging.info(f"Replicating file {file} to {replica_node}")
                # TODO
                # Get a node that has the required file
                
                # Send message to node to replicate file to replica_node

            # Remove node from network
            redis_client.srem(NETWORK_NODES, request.nodeip)
            return master_comm_pb2.NodeDownUpdateResponse(status = "SUCCESS")
        else:
            logging.error("NodeDownUpdate invoked with empty request")
            return master_comm_pb2.NodeDownUpdateResponse(status = "FAILURE")


    def GetListOfNodes(self, request, context):
        """
        GetListOfNodes is invoked when the Sentinel wants to know the list of nodes in the network
        Invoked by Sentinel
        """
        logging.info(f"GetListOfNodes invoked with request: {request}")
        nodes = redis_client.smembers(NETWORK_NODES)
        return master_comm_pb2.GetListOfNodesResponse(nodeips=list(nodes))


    # Functions for Node
    def GetNodeIpsForReplication(self, request, context):
        """
        GetNodeIpsForReplication is invoked when a file has been uploaded to the Node and needs to be replicated
        Invoked by Node
        """
        logging.info(f"GetNodeIpsForReplication invoked with request: {request}")
        if request.filename:
            # Get list of nodes that don't have the file
            new_nodes = redis_client.sdiff(NETWORK_NODES, NETWORK_DATA_FILE % request.filename)

            # Build map of number of files per node
            nodes = {}
            for node in new_nodes:
                nodes[node] = len(redis_client.smembers(NETWORK_NODE_DATA % node))

            # Sort nodes by number of files stored on them
            sorted_nodes = sorted(nodes.items(), key=lambda x: x[1])

            replication_nodes = []
            count = 0
            for node in sorted_nodes:
                replication_nodes.append(node[0])
                count += 1
                if count == FLAGS.replication_factor - 1:
                    break
            
            # Return list of nodes to replicate
            return master_comm_pb2.NodeIpsReply(nodeips = replication_nodes)
        else:
            logging.error("GetNodeIpsForReplication invoked with empty request")
            return master_comm_pb2.NodeIpsReply()


    def UpdateReplicationStatus(self, request, context):
        """
        UpdateReplicationStatus is invoked when a node has finished replicating a file to all the nodes
        Invoked by Node
        """
        logging.info(f"UpdateReplicationStatus invoked with request: {request}")
        if request.filename and request.nodeips:
            for node in request.nodeips:
                # Add file to node
                redis_client.sadd(NETWORK_NODE_DATA % node, request.filename)
                # Add node to file
                redis_client.sadd(NETWORK_DATA_FILE % request.filename, node)
            return master_comm_pb2.StatusResponse(status = master_comm_pb2.Status.Value("SUCCESS"))
        else:
            logging.error("UpdateReplicationStatus invoked with empty request")
            return master_comm_pb2.StatusResponse(status = master_comm_pb2.Status.Value("FAILURE"))


    # Functions for CLI
    def GetListOfFiles(self, request, context):
        """
        GetListOfFiles is invoked when the CLI wants to know the list of files in the network
        Invoked by CLI
        """
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
