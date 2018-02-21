import re


poly_re = r'([+-]?\d*[A-Za-z]\^\d+)|([+-]?\d*[A-Za-z])|([+-]?\d+)'

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
    Takes a monomial match object and returns a tuple of
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

    def __repr__(self):
        term_list = sorted([(value, key) for key, value in self.terms.items()
                            if value != 0], key=lambda x: x[1], reverse=True)
        return ''.join([self.term_formater(coeff, deg) for coeff, deg in
                        term_list]).lstrip('+')

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
        '''a * b'''
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

    def __pow__(self, other):
        p_out = self
        for _ in range(1, other):
            p_out *= self
        return p_out

    def __truediv__(self, other):
        partial = self
        new_terms = dict()
        q_place = self.degree - other.degree
        divisor_coeff = other.leading_coeff
        while q_place >= 0:
            q_factor = partial.leading_coeff / divisor_coeff
            if int(q_factor) == q_factor:
                q_factor = int(q_factor)
            partial -= other * Polynomial(self.variable, {q_place: q_factor})
            # print(partial.leading_coeff)
            new_terms[q_place] = q_factor
            q_place -= 1
            # print(new_terms)
            # print(partial)
        return Polynomial(self.variable, new_terms)

    def __mod__(self, other):
        temp_q = self // other
        return self - other * temp_q

##############

    def term_formater(self, coeff, deg):
        term_out = str(coeff)
        if coeff == 1 and deg != 0:
            term_out = "+"
        elif coeff == -1 and deg != 0:
            term_out = '-'
        elif coeff > 0:
            term_out = '+' + term_out
        if deg == 0:
            return term_out
        term_out += self.variable
        if deg == 1:
            return term_out
        return term_out + '^' + str(deg)

    def eval_at_n(self, n):
        '''Evaluates a polynomial at n and returns a number'''
        return sum([coeff * n ** deg for deg, coeff in self.terms.items()])

    def derivitive(self):
        '''Returns the derivative of the polynomial'''
        new_terms = {n - 1: n * self.terms.get(n, 0) for n
                     in range(1, self.degree + 1)}
        return Polynomial(self.variable, new_terms)

    # def indef_integral(self, *constant):
    #     '''Returns the indefinite integral of the polynomial'''
