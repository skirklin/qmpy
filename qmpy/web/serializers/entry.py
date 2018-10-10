from rest_framework import serializers
from django.db.models import Q

from qmpy.materials.entry import Entry
from qmpy.materials.structure import Structure
from qmpy.materials.formation_energy import FormationEnergy
from qmpy.analysis.vasp import Calculation

from calculation import CalculationSerializer
from composition import CompositionSerializer
from structure import StructureSerializer
from formationenergy import FormationEnergySerializer

class EntrySerializer(serializers.ModelSerializer):
    composition = serializers.SerializerMethodField('get_comp')
    calculations = serializers.SerializerMethodField('get_calc')
    structures = serializers.SerializerMethodField('get_strct')
    formationenergies = serializers.SerializerMethodField('get_fe')

    def get_comp(self, entry):
        serializer = CompositionSerializer(instance=entry.composition)
        return serializer.data

    def get_calc(self, entry):
        qs = Calculation.objects.filter(converged=True, 
                                        label__in=['static', 'hse06'], 
                                        entry=entry)
        serializer = CalculationSerializer(instance=qs, many=True)
        return serializer.data

    def get_strct(self, entry):
        sts = Structure.objects.filter(label='static', 
                                       entry=entry)
        serializer = StructureSerializer(instance=sts, many=True)
        return serializer.data

    def get_fe(self, entry):
        fes = FormationEnergy.objects.filter(entry=entry)
        serializer = FormationEnergySerializer(instance=fes, many=True)
        return serializer.data

    class Meta:
        model = Entry
        fields = ('id', 'name', 'path', 'composition', 'prototype', 
                  'ntypes', 'natoms', 'energy', 'keywords', 'holds',
                  'structures', 'calculations', 'formationenergies')
