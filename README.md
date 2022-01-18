# sleeper

I kept it as simple as possible, one file, straight to the point.
Directly from favorite python 3.* virtual env:

```
pip install pysyncobj
```

Video:
https://www.loom.com/share/86b1b624ba3b466aac9806ed88fcc25b
How it works: Call the script with address:port. The first argument is where the process within the terminal will run. Other processes are the ones associated.
For example:
```bash
>> python main.py localhost:8000 localhost:8001 localhost:8002
>> python main.py localhost:8001 localhost:8000 localhost:8002
>> python main.py localhost:8002 localhost:8000 localhost:8001
```

pysyncobj lib is using the ports for communications between nodes; therefore, the HTTP port for the get request is incremented by 1000:
```bash
>> curl http://localhost:9000
>> curl http://localhost:9001
>> curl http://localhost:9002
```
- Design a system that will select a single node as a "Goose" within a cluster of nodes. Every other node should be considered a "Duck". ✅
- If the Goose dies, another Duck should become the new Goose. ✅
- If a dead Goose rejoins, it should become a Duck (assuming there is already another Goose) ✅
- There can be only one Goose, even if some working nodes are unreachable (network partition) ✅
- Each node should run an HTTP server with an endpoint allowing us to check if that node is a Duck or a Goose. ✅
- Your design should accommodate a dynamic and changing number of nodes (elastic scale). ✅?
  - But it does not appear to be done once it runs with the current lib. I would have to dig a little further. Three hours might be a little short for this kind of task :P.
- There should be a way to make your design highly available.
  - I guess it refers to the availability of each node to handle requests? In a real-time interview, I would have dug with you a little to know the requirements.
One idea would be to bring this to the cloud. Without going into vendor-specific details, nodes would run inside elastic vms/docker with the help of an orchestrator.


### Early attempts 
- I was doing the implementation based on Martin Fowler and Zixuan Zhang. I had the two RPC calls implemented (with gRPC) + the HTTP call to return goose/duck wired up after ~2 hours. Then, I realized this would take me more than 1 hour to finish this up, so I thought you might want to see something a little simpler.
- Then I switch to pysyncobj.
- Because each node needed to be reachable through HTTP and returns its state, using a solution like Kafka would have been a little more work.

---
Materials that helped me out
- [pysyncobj](https://github.com/bakwc/PySyncObj) lib manages the draft algorithm between the processes. 
- [Leader and follower](https://martinfowler.com/articles/patterns-of-distributed-systems/leader-follower.html) by Martin Fowler
- [Raft algorithm explained](https://towardsdatascience.com/raft-algorithm-explained-a7c856529f40) by Zixuan Zhang (Part 1&2)
The code used ends up being different than the one used. 

[This code](https://github.com/bakwc/PySyncObj/blob/012aeb1b34be7b98f3b5c33e735836a9fc0c4cba/examples/kvstorage.py#L9-L13) is copy pasted to the example used in the pysyncobj
