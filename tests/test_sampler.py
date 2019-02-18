from scapy.all import IP
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
