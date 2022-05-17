# master-node
Master Node implementation for Space Opera in Python

## Getting Started
- `pip3 install -r requirements.txt` to install all required packages
- `python3 -m grpc_tools.protoc -I./protos --python_out=. --grpc_python_out=. ./protos/*.proto` to generate the client and server stubs from proto files
- `python3 master_node.py` to run the Master Node
- `python3 master_node.py --help` to see the available options
- Install Redis to test locally
    - For MacOS: `brew install redis`
- Postman can be used to test the gRPC server locally

## Team Members
- Anupriya, Arpitha, Rounak, Sandhya


Replicating Node:

<img width="1601" alt="repl" src="https://user-images.githubusercontent.com/89316938/168875021-3aef222f-249f-49c7-b351-2606a558cc63.png">

Getting List of Nodes:

<img width="1652" alt="list" src="https://user-images.githubusercontent.com/89316938/168875027-cd3e40b4-fc3a-4f01-b68f-70b677c34eb6.png">


