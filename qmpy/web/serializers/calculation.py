from rest_framework import serializers
from qmpy.analysis.vasp import Calculation

class CalculationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Calculation
        fields = ('id', 'label', 'band_gap', 'converged', 'energy_pa')