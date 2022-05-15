from absl import app, flags, logging
from concurrent import futures

import grpc
import master_comm_pb2
import master_comm_pb2_grpc
import redis

REDIS_HOST = "localhost"
REDIS_PORT = 6379
REDIS_PASSWORD = ""

# Absl flags
FLAGS = flags.FLAGS

flags.DEFINE_string('redis_host', REDIS_HOST, 'Redis host')
flags.DEFINE_integer('redis_port', REDIS_PORT, 'Redis port')
flags.DEFINE_string('redis_password', REDIS_PASSWORD, 'Redis password')


# Setup redis client that will store all network node and file information
redis_client = None
try:
    redis_client = redis.Redis(host=FLAGS.redis_host, port=FLAGS.redis_port, password=FLAGS.redis_password, decode_responses=True)
except Exception as e:
    logging.error("Error while connecting to redis: %s", e)
    exit(1)


class MasterComm(master_comm_pb2_grpc.ReplicationServicer):
    def GetNodeIpsForReplication(self, request, context):
        return master_comm_pb2.NodeIpsReply(nodeips=["test0", "test1"])

    def UpdateReplicationStatus(self, request, context):
        return master_comm_pb2.ReplicationDetailsResponse()


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    master_comm_pb2_grpc.add_ReplicationServicer_to_server(MasterComm(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    server.wait_for_termination()


def main(argv):
    logging.info("Starting gRPC server...")
    serve()


if __name__ == '__main__':
    app.run(main)
