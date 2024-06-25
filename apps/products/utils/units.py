from measurement.base import MeasureBase
from measurement.measures import Weight

zero_weight = Weight(kg=0)


class WeightUnits:
    G = "g"
    LB = "lb"
    OZ = "oz"
    KG = "kg"
    TONNE = "tonne"

    CHOICES = [
        (G, "Gram"),
        (LB, "Pound"),
        (OZ, "Ounce"),
        (KG, "kg"),
        (TONNE, "Tonne"),
    ]


__all__ = [
    'Mass',
    'Weight',
]


class Mass(MeasureBase):
    STANDARD_UNIT = 'g'
    UNITS = {
        'g': 1.0,
        'tonne': 1000000.0,
        'oz': 28.3495,
        'lb': 453.592,
        'stone': 6350.29,
        'short_ton': 907185.0,
        'long_ton': 1016000.0,
    }
    ALIAS = {
        'mcg': 'ug',
        'gram': 'g',
        'ton': 'short_ton',
        'metric tonne': 'tonne',
        'metric ton': 'tonne',
        'ounce': 'oz',
        'pound': 'lb',
        'short ton': 'short_ton',
        'long ton': 'long_ton',
    }
    SI_UNITS = ['g']


# For backward compatibility
Weight = Mass
