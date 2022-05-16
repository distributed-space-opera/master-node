# master-node
Master Node implementation for Space Opera in Python

## Getting Started
- `pip3 install -r requirements.txt` to install all required packages
- `python3 -m grpc_tools.protoc -I./protos --python_out=. --grpc_python_out=. ./protos/*.proto` to generate the client and server stubs from proto files
- `python3 master_node.py` to run the Master Node
- `python3 master_node.py --help` to see the available options

## Team Members
- Anupriya, Arpitha, Rounak, Sandhya