import unittest
from polynomial_class import *


class PolynomialTests(unittest.TestCase):

    def test_init(self):
        p1 = Polynomial('x', {1: 1})
        self.assertIsInstance(p1, Polynomial)

    def test_poly_attributes(self):
        p1 = Polynomial('x', {1: 1})
        self.assertEqual(p1.degree, 1)
        self.assertEqual(p1.terms, {1: 1})
        self.assertEqual(p1.variable, 'x')
        self.assertTrue(p1.leading_coeff, 1)

    def test_poly_equal(self):
        p1 = Polynomial('x', {1: 1})
        self.assertEqual(p1, p1)

    def test_poly_equal_same_int(self):
        p1 = Polynomial('x', {0: 5})
        p2 = Polynomial('y', {0: 5})
        self.assertEqual(p1, p2)

    def test_poly_equal_diff_int(self):
        p1 = Polynomial('x', {0: 1})
        p2 = Polynomial('y', {0: 5})
        self.assertNotEqual(p1, p2)

    def test_add(self):
        p1 = Polynomial('x', {1: 1})
        p2 = Polynomial('x', {1: 2})
        self.assertEqual(p1 + p1, p2)

    def test_subtract(self):
        p1 = Polynomial('x', {1: 1})
        p2 = Polynomial('x', {1: 2})
        self.assertEqual(p2 - p1, p1)

    def test_multiply_poly_poly(self):
        p1 = Polynomial('x', {1: 1, 0: 1})
        p2 = Polynomial('x', {2: 1, 1: 2, 0: 1})
        self.assertEqual(p1 * p1, p2)

    def test_multiply_poly_int(self):
        p1 = Polynomial('x', {1: 1, 0: 1})
        p2 = 5
        p3 = Polynomial('x', {1: 5, 0: 5})
        self.assertEqual(p1 * p2, p3)

    def test_pow_monomial(self):
        p1 = Polynomial('x', {1: 1})
        p2 = Polynomial('x', {3: 1})
        self.assertEqual(p1 ** 3, p2)

    def test_pow_perf_square(self):
        p1 = Polynomial('x', {1: 1, 0: 1})
        p2 = Polynomial('x', {2: 1, 1: 2, 0: 1})
        self.assertEqual(p1 ** 2, p2)

    def test_pow_1(self):
        p1 = Polynomial('x', {1: 1, 0: 1})
        self.assertEqual(p1 ** 1, p1)

    def test_pow_0(self):
        p1 = Polynomial('x', {1: 1, 0: 1})

        self.assertEqual(p1 ** 0, p1)

    def test_eval_mon(self):
        p1 = Polynomial('x', {1: 1, 0: 1})
        self.assertEqual(p1.eval_at_n(1), 2)

    def test_eval(self):
        p1 = Polynomial('x', {2: 1, 1: 2, 0: 1})
        self.assertEqual(p1.eval_at_n(4), 25)

    def test_str_to_poly(self):
        p1 = Polynomial('x', {1: 1})
        p2 = string_to_poly('x')
        self.assertEqual(p1, p2)

    def test_str_to_poly_2_dig_coeff(self):
        p1 = string_to_poly("35p^2+2p-24")
        p2 = Polynomial('p', {2: 35, 1: 2, 0: -24})
        self.assertEqual(p1, p2)

    def test_neg_linear_term(self):
        p1 = string_to_poly("7n - 5n^4+6n^3")
        p2 = string_to_poly("3n^3-2n^4+8n")
        p3 = p1 - p2
        self.assertEqual(str(p3), '-3n^4+3n^3-n')

    def test_true_div_1(self):
        p1 = Polynomial('x', {1: 2, 1: -1})
        p2 = Polynomial('x', {1: 1, 1: -1})
        p3 = Polynomial('x', {1: 1, 0: 1})
        self.assertEqual(p1 / p2, p3)

    def test_true_div_2(self):
        p1 = Polynomial('x', {2: 1, 1: 2, 0: 1})
        self.assertEqual(p1 ** 3 / p1 ** 2, p1)

    def test_ddx_1(self):
        p1 = Polynomial('x', {2: 1, 1: 1, 0: 1})
        p2 = Polynomial('x', {1: 2, 0: 1})
        self.assertEqual(p1.derivitive(), p2)

    # def test_multiply_int_poly(self):
    #     p1 = 5
    #     p2 = Polynomial('x', {1: 1, 0: 1})
    #     p3 = Polynomial('x', {1: 5, 0: 5})
    #     self.assertEqual(p1 * p2, p3)


def main():
    unittest.main()


if __name__ == '__main__':
    main()
