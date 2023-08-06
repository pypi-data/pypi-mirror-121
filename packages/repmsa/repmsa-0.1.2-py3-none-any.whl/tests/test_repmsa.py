from . import repmsa

def test_repmsa():
    filename='test3.fasta'
    assert repmsa.RankMatrix(filename)
    assert repmsa.RankMatrix(filename).iterator()
