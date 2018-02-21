import re
import unittest


poly_re = r'([+-]?\d?[A-Za-z]\^\d+)|([+-]?\d?[A-Za-z])|([+-]?\d?)'

poly_reg = re.compile(poly_re)
term_reg = re.compile(r'[A-Za-z]\^')


def string_to_poly(poly):
    '''
    Takes a polynomial string on the form ax^n + bx^m + ... c and returns
    a Polynomial object
    '''
    if type(poly) is not str:
        raise TypeError
    poly_in = poly.replace(' ', '')
    if poly_in == '':
        raise TypeError
    var = [x for x in list(poly_in) if x.isalpha()][0]
    terms = [x for x in poly_reg.split(poly_in) if x is not None and x != '']
    terms = [[deg, coeff] for coeff, deg in [term_split(x) for x in terms]]
    degs = {x[0] for x in terms}
    return Polynomial(var, {deg: sum([x[1] for x in terms if x[0] == deg])
                            for deg in degs})


def term_split(term):
    '''
    takes a monomial match object and returns a tuple of
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

    def __init__(self, variable, terms):
        self.variable = variable
        self.terms = terms
        self.degree = max(self.terms.keys())

    def term_formater(self, coeff, deg):
        term_out = str(coeff)
        if coeff == 1 and deg != 0:
            term_out = "+" + term_out[1:]
        elif coeff > 0:
            term_out = '+' + term_out
        if deg == 0:
            return term_out
        term_out += self.variable
        if deg == 1:
            return term_out
        return term_out + '^' + str(deg)

    def __add__(self, other):
        max_deg = max(self.degree, other.degree)
        sum_terms = {deg: self.terms.get(deg, 0) + other.terms.get(deg, 0)
                     for deg in range(max_deg + 1)}
        return Polynomial(self.variable, sum_terms)

    def __sub__(self, other):
        max_deg = max(self.degree, other.degree)
        diff_terms = {deg: self.terms.get(deg, 0) - other.terms.get(deg, 0)
                      for deg in range(max_deg + 1)}
        return Polynomial(self.variable, diff_terms)

    def __mul__(self, other):
        if type(other) != Polynomial:
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

    def __repr__(self):
        term_list = sorted([(value, key) for key, value in self.terms.items()
                            if value != 0], key=lambda x: x[1], reverse=True)
        return ''.join([self.term_formater(coeff, deg) for coeff, deg in
                        term_list]).lstrip('+')

    def eval_at_n(self, n):
        '''Evaluates a polynomial at n and returns a number'''
        return sum([coeff * n ** deg for deg, coeff in self.terms.items()])

    def derivitive(self):
        '''Returns the derivative of the polynomial'''
        new_terms = {n - 1: n * self.terms.get(n, 0) for n
                     in range(1, self.degree + 1)}
        return Polynomial(self.variable, new_terms)

    def __eq__(self, other):
        if self.variable != other.variable:
            return False
        for deg in range(max(self.degree, other.degree)):
            if self.terms.get(deg, 0) != other.terms.get(deg, 0):
                return False
        else:
            return True


# # poly = "-5x^2+3x+2"
# # p1 = string_to_poly(poly)

# # poly2 = "6x^4-5x^2+3x+2+4x-3"
# # p2 = string_to_poly(poly2)

# # print(p1, "+", p2, "=", p1 + p2)
# # print(p1, "-", p2, "=", p1 - p2)
# # print(p1, "*", p2, "=", p1 * p2)

# # pt1 = string_to_poly("x+1")
# # pt2 = string_to_poly("x-1")

# # pds = pt1 * pt2

# # print(pds)


# # pds_t_2 = pds * 2
# # print(pds_t_2)

# p1 = string_to_poly("x+4")
# p2 = string_to_poly("2x^2-3x+5")

# print(p1 * p2)

# print(p1.eval_at_n(5))
# print(p2.derivitive())


class PolynomialTests(unittest.TestCase):

    def test_str_to_poly(self):
        pn = Polynomial('x', {1: 4, 0: -3})
        self.assertEqual(string_to_poly('4x-3'), pn)

    def test_mul(self):
        p1 = Polynomial('x', {1: 1, 0: 1})
        p2 = Polynomial('x', {2: 1, 1: 2, 0: 1})
        self.assertEqual(p1 * p1, p2)


def main():
    unittest.main()


if __name__ == '__main__':
    main()
