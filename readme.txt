<Lightweigth Network Simulator>

This simulator is made to simulate routing algorithm and check deadlock state.

python setconf.py [alias] [network type] [args..]
: you can generate configuration files for specific network.
: sentence that starts with '//' is recognized as comment.
: configuration files are saved into conf/[alias].conf
: to add packet generation senarios, modify this file according to the comment.
: in current version, we support following algorithms:
: - KNC (k_ary_n_cube)
: - KNC_DF (k_ary_n_cube_dfree)
: - CCC (cube_connected_cycle)
: - CCC_DF (cube_connected_cycle_dfree)

python main.py [conf_alias]
: you can load network environment from the configuration files.
: the program prints information of nodes, channels and senario.

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

(LNS) i r
: print routing table

(LNS) i [target]
: print information of target (node, channel, flit)

(LNS) i r [source] [destination]
: search routing table for source->destination

(LNS) q
: exit the simulator