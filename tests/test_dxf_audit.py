import ezdxf


def test_dxf_audit_placeholder():
    doc = ezdxf.new("R2010")
    msp = doc.modelspace()
    msp.add_text("TEST", dxfattribs={'height': 100}).set_pos((0, 0))
    auditor = doc.audit()
    assert not auditor.has_fatal_errors, "DXF auditor found fatal errors"
    # Ensure text entity present
    texts = [e for e in msp if e.dxftype() == 'TEXT']
    assert len(texts) == 1