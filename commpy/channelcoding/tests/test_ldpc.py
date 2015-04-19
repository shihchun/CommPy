# Authors: Veeresh Taranalli <veeresht@gmail.com>
# License: BSD 3-Clause

from numpy import array, sqrt, zeros
from numpy.random import randn
from numpy.testing import assert_allclose
from commpy.channelcoding.ldpc import get_ldpc_code_params, ldpc_bp_decode
from commpy.utilities import hamming_dist

class TestLDPCCode(object):

    @classmethod
    def setup_class(cls):
        ldpc_design_file_1 = "channelcoding/designs/ldpc/gallager/96.33.964.txt"
        cls.ldpc_code_params = get_ldpc_code_params(ldpc_design_file_1)

    @classmethod
    def teardown_class(cls):
        pass

    def test_ldpc_bp_decode(self):
        N = 96
        k = 48
        rate = 0.5
        Es = 1.0
        snr_list = array([1.0, 1.5, 2.0, 2.5])
        niters = 10000000
        tx_codeword = zeros(N, int)
        ldpcbp_iters = 100

        fer_array_ref = array([200.0/350, 200.0/550, 200.0/1000, 200.0/2000])
        fer_array_test = zeros(4)

        for idx, ebno in enumerate(snr_list):

            noise_std = 1/sqrt((10**(ebno/10.0))*rate*2/Es)
            fer_cnt_bp = 0

            for iter_cnt in xrange(niters):

                awgn_array = noise_std * randn(N)
                rx_word = 1-(2*tx_codeword) + awgn_array
                rx_llrs = 2.0*rx_word/(noise_std**2)

                [dec_word, out_llrs] = ldpc_bp_decode(rx_llrs, self.ldpc_code_params,
                                                      ldpcbp_iters)

                num_bit_errors = hamming_dist(tx_codeword, dec_word)
                if num_bit_errors > 0:
                    fer_cnt_bp += 1

                if fer_cnt_bp >= 200:
                    fer_array_test[idx] = float(fer_cnt_bp)/(iter_cnt+1)
                    break

        assert_allclose(fer_array_test, fer_array_ref, rtol=1e-1, atol=0)
