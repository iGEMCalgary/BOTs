from django.contrib import admin
from sequence_optimization.models import *

# Register your models here.
admin.site.register(AncestorSequence)
admin.site.register(AncestorSequenceOptimized)
admin.site.register(SequenceParameters)
admin.site.register(MutatedSequence)
admin.site.register(GCInfo)
admin.site.register(GCParameters)
