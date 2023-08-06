import numpy as np

class Lagrange:
  def __init__(self, xs, ys):
    self.n = len(xs)
    self.xs = xs
    self.ys = ys
    self.coef = np.zeros(self.n)
    for i in range(self.n):
      self.coef[i] = np.multiply.reduce(xs[i] - xs[:i]) * np.multiply.reduce(xs[i] - xs[i+1:])

  def __call__(self, x):
    res = 0
    for i in range(self.n):
      res += self.ys[i] * np.multiply.reduce(x - self.xs[:i]) * np.multiply.reduce(x - self.xs[i+1:]) / self.coef[i]
    return res
