import astropy.units as u
import periodictable as pt
import random
from nexoclom.atomicdata import atomicmass


def test_atomicmass():
    sp = random.choice(list(pt.elements))

    assert atomicmass(sp.symbol) == sp.mass * u.u, 'Element mass failure'
    assert atomicmass('H2O') == pt.formula('H2O').mass * u.u, (
        'H2O mass failure')
    assert atomicmass('AAb') is None, 'Bad species failure'