from scapy.all import IP, sniff
from sampler import SampleMaker


class TestSampleMaker(object):
    # tests for `SampleMaker`

    def test_create(self):
        # we can create SampleMaker instances
        sm = SampleMaker()
        assert sm is not None
        assert sm.dev is None
        assert sm.outpath == "sample.pcapng"

    def test_update_outfile(self, tmpdir):
        # we can append packets to an outfile
        sample_path = tmpdir.join('test-update.pcap')
        sm = SampleMaker(outpath=str(sample_path))
        pkts = (IP(), IP())
        sm.update_outfile(pkts)
        assert sample_path.isfile()
        sm.update_outfile(IP())
        read = sniff(offline=str(sample_path))
        assert len(read) == 3

    def test_update_outfile_no_file(self, tmpdir):
        # updating a non-existent file means creating it
        sample_path = tmpdir.join('test-update.pcap')
        sm = SampleMaker(outpath=str(sample_path))
        pkts = IP(src="1.2.3.4")
        sm.update_outfile(IP(src="1.2.3.4"))
        read = sniff(offline=str(sample_path))
        assert len(read) == 1
        assert read[0].src == "1.2.3.4"
