from absl import app
from absl import logging
from concurrent import futures

import grpc
import master_comm_pb2
import master_comm_pb2_grpc


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