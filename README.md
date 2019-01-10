# sb_finder

Find suspicous data in network streams

`sb_finder` is the analyzing part of the StalkerBuster. It is based on
third-party libraries to scan `.pcap` files.

## `.pcap` Libraries

For now, we are experimenting with different libs that allow scanning `.pcap`
streams.

The candidates:

- [libpcap](https://pypi.org/project/libpcap/)
- [pcapy](https://github.com/SecureAuthCorp/pcapy)
- [scapy](https://scapy.net)
- [pyshark](https://pypi.org/project/pyshark/)
- [pycapfile](https://pypi.org/project/pypcapfile/)

Currently evaluated: *pcapy*
