from sequence_optimization import models


def clean_and_save_ancestor_sequence(model):
    pass


def clean_and_save_ancestor_sequence_optimized(model):
    pass


def clean_and_save_sequence_parameters(model):
    pass


def clean_and_save_mutated_sequence(model):
    pass


def clean_and_save_gc_info(model):
    pass


def clean_and_save_gc_parameters(model):
    pass


def clean_and_save(model):
    if isinstance(model, models.AncestorSequence):
        clean_and_save_ancestor_sequence(model)
    elif isinstance(model, models.AncestorSequenceOptimized):
        clean_and_save_ancestor_sequence_optimized(model)
    elif isinstance(model, models.SequenceParameters):
        clean_and_save_sequence_parameters(model)
    elif isinstance(model, models.MutatedSequence):
        clean_and_save_mutated_sequence(model)
    elif isinstance(model, models.GCInfo):
        clean_and_save_gc_info(model)
    elif isinstance(model, models.GCParameters):
        clean_and_save_gc_parameters(model)
    else:
        raise LookupError("model seems to not exist")
