"""Optional OpenSim 4.3 adapter.

The lightweight repository does not bundle an OpenSim model or claim that its
surrogate outputs are OpenSim outputs. Supply a validated .osim model and the
OpenSim Python bindings to implement model-specific forward dynamics here.
"""
def require_opensim():
    try:
        import opensim  # type: ignore
    except ImportError as exc:
        raise RuntimeError("OpenSim Python bindings are required for this path") from exc
    return opensim

