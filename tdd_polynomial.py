import unittest
import re


# Figure out how to deal with constants


poly_re = r'([+-]?\d*[A-Za-z]\^\d+)|([+-]?\d*[A-Za-z])|([+-]?\d*)'

poly_reg = re.compile(poly_re)
term_reg = re.compile(r'[A-Za-z]\^')


def string_to_poly(poly):
    '''Takes a polynomial string on the form ax^n + bx^m + ... c and returns
    a Polynomial object
    '''
    poly_in = poly.replace(' ', '')
    var = [x for x in list(poly_in) if x.isalpha()]
    if var == []:
        return int(poly)
    var = var[0]
    terms = [x for x in poly_reg.split(poly_in) if x is not None and x != '']
    terms = [[deg, coeff] for coeff, deg in [term_split(x) for x in terms]]
    degs = {x[0] for x in terms}
    return Polynomial(var, {deg: sum([x[1] for x in terms if x[0] == deg])
                            for deg in degs})


def term_split(term):
    '''takes a monomial match object and returns a tuple of
    the form (coeff, deg)
    '''
    if term[0] in ["+", "-"] and not term[1].isdigit():
        term = term[0] + '1' + term[1:]
    elif term[0].isalpha():
        term = "1" + term
    if '^' in term:
        temp = term_reg.split(term)
        return tuple([int(x) for x in temp])
    elif term[-1].isalpha():
        return (int(term[:-1]), 1)
    else:
        return (int(term), 0)


class Polynomial():
    """
    Creates a polynomial object with methods for typical polynomial operations
    """

    def __init__(self, variable, terms):
        self.variable = variable
        self.terms = {deg: coeff for deg, coeff in terms.items()
                      if coeff != 0 or deg == 0}
        self.degree = max(self.terms.keys())
        self.leading_coeff = self.terms[self.degree]

    def __eq__(self, other):
        '''a == b '''
        if self.degree == 0 and other.degree == 0:
            return self.leading_coeff == other.leading_coeff
        if self.variable != other.variable:
            return False
        for deg in range(max(self.degree, other.degree)):
            if self.terms.get(deg, 0) != other.terms.get(deg, 0):
                return False
        return True

    def __add__(self, other):
        '''a + b'''
        max_deg = max(self.degree, other.degree)
        sum_terms = {deg: self.terms.get(deg, 0) + other.terms.get(deg, 0)
                     for deg in range(max_deg + 1)}
        return Polynomial(self.variable, sum_terms)

    def __sub__(self, other):
        '''a - b'''
        max_deg = max(self.degree, other.degree)
        diff_terms = {deg: self.terms.get(deg, 0) - other.terms.get(deg, 0)
                      for deg in range(max_deg + 1)}
        return Polynomial(self.variable, diff_terms)

    def __mul__(self, other):
        if type(self) != Polynomial:
            new_terms = {deg: self * coeff for deg, coeff
                         in other.terms.items()}
        elif type(other) != Polynomial:
            new_terms = {deg: other * coeff for deg, coeff
                         in self.terms.items()}
        else:
            terms_in_prod = [[c1 * c2, d1 + d2] for d1, c1 in
                             self.terms.items() for d2, c2 in
                             other.terms.items()]
            degs = {x[1] for x in terms_in_prod}
            new_terms = {deg: sum([x[0] for x in terms_in_prod if x[1] == deg])
                         for deg in degs}
        return Polynomial(self.variable, new_terms)

    def __pow__(self, other):
        p_out = self
        for _ in range(1, other):
            p_out *= self
        return p_out

    def evalf(self, n):
        '''
        returns the result of evaluating a polynomial at n
        '''
        return sum([coeff * n ** deg for deg, coeff in self.terms.items()])


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

    def test_evalf_mon(self):
        p1 = Polynomial('x', {1: 1, 0: 1})
        self.assertEqual(p1.evalf(1), 2)

    def test_evalf(self):
        p1 = Polynomial('x', {2: 1, 1: 2, 0: 1})
        self.assertEqual(p1.evalf(4), 25)

    def test_str_to_poly(self):
        p1 = Polynomial('x', {1: 1})
        p2 = string_to_poly('x')
        self.assertEqual(p1, p2)

    def test_str_to_poly_2_dig_coeff(self):
        p1 = string_to_poly("35p^2+2p-24")
        p2 = Polynomial('p', {2: 35, 1: 2, 0: -24})
        self.assertEqual(p1, p2)


    # def test_multiply_int_poly(self):
    #     p1 = 5
    #     p2 = Polynomial('x', {1: 1, 0: 1})
    #     p3 = Polynomial('x', {1: 5, 0: 5})
    #     self.assertEqual(p1 * p2, p3)


def main():
    unittest.main()


if __name__ == '__main__':
    main()



# deal with
##the following issue with -1n
##>>> p1 = string_to_poly("7n - 5n^4+6n^3")
##>>> p1
##-5n^4+6n^3+7n
##>>> p2 = string_to_poly("3n^3-2n^4+8n")
##>>> p2
##-2n^4+3n^3+8n
##>>> p1-p2
##-3n^4+3n^3-1n

##second issue>>> p3 = string_to_poly("35p^2+2p-24")
##p3
##5p^2+2p+5