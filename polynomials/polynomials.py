from numbers import Number

from numpy import outer, asarray, resize, sum, trim_zeros


class Polynomial:

    def __init__(self, coefs):
        self.coefficients = coefs

    def degree(self):
        return len(self.coefficients) - 1

    def __str__(self):
        coefs = self.coefficients
        terms = []

        if coefs[0]:
            terms.append(str(coefs[0]))
        if self.degree() and coefs[1]:
            terms.append(f"{'' if coefs[1] == 1 else coefs[1]}x")

        terms += [f"{'' if c == 1 else c}x^{d}"
                  for d, c in enumerate(coefs[2:], start=2) if c]

        return " + ".join(reversed(terms)) or "0"

    def __repr__(self):
        return self.__class__.__name__ + "(" + repr(self.coefficients) + ")"

    def __eq__(self, other):

        return isinstance(other, Polynomial) and\
            self.coefficients == other.coefficients

    def __add__(self, other):

        if isinstance(other, Polynomial):
            common = min(self.degree(), other.degree()) + 1
            coefs = tuple(a + b for a, b in zip(self.coefficients,
                                                other.coefficients))
            coefs += self.coefficients[common:] + other.coefficients[common:]

            return Polynomial(coefs)

        elif isinstance(other, Number):
            return Polynomial((self.coefficients[0] + other,)
                              + self.coefficients[1:])

        else:
            return NotImplemented

    def __radd__(self, other):
        return self + other

    def __sub__(self, other):
        if isinstance(other, Polynomial):
            common = min(self.degree(), other.degree()) + 1
            coefs = tuple(a - b for a, b in zip(self.coefficients,
                                                other.coefficients))
            if self.degree() > other.degree():
                coefs += self.coefficients[common:]
            elif other.degree() > self.degree():
                coefs += tuple(-1*other.coefficients[common:][j]
                               for j in range(0, len(other.coefficients[common:])))

            return Polynomial(coefs)

        elif isinstance(other, Number):
            return Polynomial((self.coefficients[0] - other,)
                              + self.coefficients[1:])

        else:
            return NotImplemented

    def __rsub__(self, other):
        return Polynomial((other - self.coefficients[0],) + tuple(-1*self.coefficients[1:][j] for j in range(0, len(self.coefficients[1:]))))

    def __mul__(self, other):
        if isinstance(other, Polynomial):
            max_degree = self.degree() + other.degree() + 1

            self_array = asarray(self.coefficients)
            other_array = asarray(other.coefficients)

            self_array.resize(max_degree)
            other_array.resize(max_degree)

            outer_array = outer(self_array, other_array)

            terms = []

            for line in range(1, max_degree + max_degree):
                # Get column index of the first element
                # in this line of output. The index is 0
                # for first ROW lines and line - ROW for
                # remaining lines
                start_col = max(0, line - max_degree)

                # Get count of elements in this line.
                # The count of elements is equal to
                # minimum of line number, COL-start_col and ROW
                count = min(line, (max_degree - start_col), max_degree)

                rows = []
                for j in range(0, count):
                    rows.append(outer_array[min(max_degree, line) - j - 1][start_col + j])

                terms.append(sum(rows))

            terms = trim_zeros(terms, 'b')

            return Polynomial(tuple(terms))

        elif isinstance(other, Number):
            terms = []
            for i in range(len(self.coefficients)):
                terms.append(self.coefficients[i] * other)
            return Polynomial(tuple(terms))
        
        else:
            return NotImplemented

    def __rmul__(self, other):
        return self * other

    def __pow__(self, other):
        result = self

        for i in range(1, other):
            result = result*self
        return result

    def __call__(self, other):
        result = []

        for i in range(len(self.coefficients)):
            if i == 0:
                result.append(self.coefficients[i])
            else:
                result.append((other**i) * self.coefficients[i])

        result = sum(result)
        return result