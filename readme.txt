<Lightweigth Network Simulator>

This simulator is made to simulate routing algorithm and check deadlock state.

python setconf.py [alias] [network type] [args..]
: you can generate configuration files for specific network.
: sentence that starts with '//' is recognized as comment.
: configuration files are saved into conf/[alias]_[policy].conf
: configuration files for following policies are automatically generated:
: - RR (round-robin)
: - FCFS (first-come first-served)
: - OF (oldest first)
: to add packet generation scenarios, modify this file according to the comment.
: in current version, we support following algorithms:
: - KNC (k-ary n-cubes)
: - CCC (cube-connected cycles)
: - SEN (shuffle-exchange networks)

python main.py [conf_alias]
: you can load network environment from the configuration files.
: the program prints information of nodes, channels and scenario.

(LNS) r
: run the simulation from the beginning.

(LNS) c
: run the simulation from current state.

(LNS) b
: print current breakpoints.

(LNS) b [tick]
: set breakpoint at specified tick and print current breakpoints.

(LNS) d
: remove all breakpoints and print current breakpoints.

(LNS) d [tick]
: remove breakpoint at specified tick and print current breakpoints.

(LNS) t
: proceed the simulation for one tick.

(LNS) t [tick]
: proceed the simulation for specified ticks.

(LNS) i n
: print information of all nodes

(LNS) i c
: print information of all channels

(LNS) i f
: print information of all flits

(LNS) i [target]
: print information of target (node, channel, flit)

(LNS) i p [source] [destination]
: search path from source to destination

(LNS) q
: exit the simulator