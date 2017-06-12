import pytest
import liquidcounter as lc


class TestLiquidResolution:
    def test_resolveLiquids_simple(self):
        liquid = {
            'a': ['b', 'c'],
            'c': ['e', 'd'],
        }

        expected = {'a': ['b', 'c', 'd', 'e']}
        results = lc._resolveLiquids(liquid)
        assert set(expected.keys()) == set(results.keys())
        for r in results:
            if r != 'abstain':
                assert set(expected[r]) == set(results[r])
            else:
                assert expected[r] == results[r]

    def test_resolveLiquids_complex(self):
        liquid = {
            'a': ['b', 'c'],
            'c': ['d', 'e'],
            'b': ['f', 'g']
        }

        expected = {'a': ['b', 'c', 'd', 'e', 'f', 'g']}
        results = lc._resolveLiquids(liquid)
        assert set(expected.keys()) == set(results.keys())
        for r in results:
            if r != 'abstain':
                assert set(expected[r]) == set(results[r])
            else:
                assert expected[r] == results[r]

    def test_resolveLiquids_circular(self):
        liquid = {
            'a': ['b'],
            'c': ['a'],
            'b': ['c'],
            'd': ['e']
        }

        expected = {'abstain': 3, 'd': ['e']}
        results = lc._resolveLiquids(liquid)
        assert set(expected.keys()) == set(results.keys())
        for r in results:
            if r != 'abstain':
                assert set(expected[r]) == set(results[r])
            else:
                assert expected[r] == results[r]


#@pytest.mark.skip(reason="no way of currently testing this")
class TestSuiteLiquidCounter:
    def test_if_loads(self):
        empty_raw_votes_json = {}
        empty_result = {
            'yes': 0,
            'no': 0,
            'abstain': 0,
            'liquid': 0
        }
        assert empty_result == lc.resolveIt(empty_raw_votes_json)
        return None

    def test_handle_incomplete_table(self):
        incomplete_votes = {
            'yes': ['a']
        }

        incomplete_result = {
            'yes': 1,
            'no': 0,
            'abstain': 0,
            'liquid': 0
        }

        assert incomplete_result == lc.resolveIt(incomplete_votes)
        
    def test_simple_raw_votes_json(self):
        simple_raw_votes_json = {
            'yes': ['a', 'b', 'c'],
            'no': ['d'],
            'abstain': ['e', 'f'],
        }

        simple_result = {
            'yes': 3,
            'no': 1,
            'abstain': 2,
            'liquid': 0
        }

        assert simple_result == lc.resolveIt(simple_raw_votes_json)
        return None

    def test_resolved_liquid_raw_votes_json(self):
        resolved_liquid_raw_votes_json = {
            'yes': ['a', 'b', 'c'],
            'no': ['d'],
            'abstain': ['e', 'f'],
            'd': ['g', 'h'],
            'a': ['i'],
            'f': ['j']
        }

        resolved_liquid_result = {
            'yes': 4,
            'no': 3,
            'abstain': 3,
            'liquid': 0
        }

        assert resolved_liquid_result == lc.resolveIt(resolved_liquid_raw_votes_json)
        return None

    def test_resolved_complex_liquid_raw_votes_json(self):
        resolved_complex_liquid_raw_votes_json = {
            'yes': ['a', 'b', 'c'],
            'no': ['d'],
            'abstain': ['e', 'f'],
            'd': ['g', 'h'],
            'h': ['i', 'j'],
        }

        resolved_complex_liquid_result = {
            'yes': 3,
            'no': 5,
            'abstain': 2,
            'liquid': 0
        }

        assert resolved_complex_liquid_result == lc.resolveIt(resolved_complex_liquid_raw_votes_json)
        return None

    def test_unresolved_liquid_raw_votes_json(self):
        unresolved_liquid_raw_votes_json = {
            'yes': ['a', 'b', 'c'],
            'no': ['d'],
            'abstain': ['e', 'f'],
            'd': ['g', 'h'],
            'a': ['i'],
            'f': ['j'],
            'k': ['l', 'm', 'n']
        }

        unresolved_liquid_result = {
            'yes': 4,
            'no': 3,
            'abstain': 3,
            'liquid': 3
        }

        assert unresolved_liquid_result == lc.resolveIt(unresolved_liquid_raw_votes_json)
        return None

    def test_unresolved_complex_liquid_raw_votes_json(self):
        unresolved_complex_liquid_raw_votes_json = {
            'yes': ['a', 'b', 'c'],
            'no': ['d'],
            'abstain': ['e'],
            'd': ['g', 'h'],
            'a': ['i'],
            'f': ['j'],
            'j': ['l', 'm', 'n']
        }

        unresolved_complex_liquid_result = {
            'yes': 4,
            'no': 3,
            'abstain': 1,
            'liquid': 4
        }

        assert unresolved_complex_liquid_result == lc.resolveIt(unresolved_complex_liquid_raw_votes_json)
        return None

    def test_circular(self):
        circular_raw_votes_json = {
            'a': ['b'],
            'c': ['a'],
            'b': ['c']
        }

        circular_result = {
            'yes': 0,
            'no': 0,
            'abstain': 3,
            'liquid': 0
        }

        assert circular_result == lc.resolveIt(circular_raw_votes_json)
        return None

    def test_circular_and_unresolved(self):
        circular_raw_votes_json = {
            'a': ['b'],
            'c': ['a'],
            'b': ['c'],
            'd': ['e']
        }

        circular_result = {
            'yes': 0,
            'no': 0,
            'abstain': 3,
            'liquid': 1
        }

        assert circular_result == lc.resolveIt(circular_raw_votes_json)
        return None

    def test_empty_standard_vote(self):
        empty_standard_raw_json = {
            'yes': [],
            'no': ['d']
        }
        empty_standard_result = {
            'yes': 0,
            'no': 1,
            'abstain': 0,
            'liquid': 0
        }
        assert empty_standard_result == lc.resolveIt(empty_standard_raw_json)
        return None

#@pytest.mark.skip(reason="no way of currently testing this")
class TestInvalidVotesJson:
    def test_voting_twice(self):
        two_votes = {
            'yes': ['a'],
            'no': ['a'],
            'abstain': []
        }

        with pytest.raises(RuntimeError) as excinfo:
            lc.resolveIt(two_votes)
        excinfo.match('There are two or more votes from: a')

        return None

    def test_voting_twice_complicated(self):
        two_votes_complicated = {
            'yes': ['a', 'b', 'c'],
            'no': ['d'],
            'abstain': ['e'],
            'd': ['g', 'h'],
            'b': ['i'],
            'f': ['j'],
            'j': ['l', 'b', 'n']
        }

        with pytest.raises(RuntimeError) as excinfo:
            lc.resolveIt(two_votes_complicated)
        excinfo.match('There are two or more votes from: b')

        return None