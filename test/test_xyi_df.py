import sys
sys.path.append('../')

import ms_logic.gh_xic_data_reader as xdr  #ms_logic.gh_xic_data_reader as xdr


def test_download_raw():
    text_lines = xdr.get_defaut_data_lines()
    print(str(len(text_lines)))
    assert( 10591 == len(text_lines))
