from bnlearn2py import fetch_model


def test_fetch_model():
    model, cpds = fetch_model('asia')
    assert(set(model.edges) == set([('asia', 'tub'), ('tub', 'either'),
                                    ('either', 'xray'), ('either', 'dysp'),
                                    ('smoke', 'lung'), ('smoke', 'bronc'),
                                    ('lung', 'either'), ('bronc', 'dysp')]))
    for node, cpd in cpds.items():
        assert(model.get_cpds(node) is cpd)
