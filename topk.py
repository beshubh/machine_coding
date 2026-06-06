import threading
import unittest
from abc import ABC, abstractmethod
from collections import defaultdict
from sortedcontainers import SortedDict, SortedSet




class Entity(ABC):
    uid: str
    score: float

    def __init__(self, uid: int, score: int) -> None:
        self._uid = uid
        self._score = score

    @property
    def score(self):
        return self._score

    @score.setter
    def score(self, value: int):
        self._score = value

    @property
    def uid(self):
        return self._uid


class Person(Entity):
    pass



class RankManger:

    def __init__(self) -> None:
        self._lock = threading.Lock()
        self._scores = SortedSet()
        self._entities = {}


    def update(self, entity_id: int, new_score: int) -> None:
        with self._lock:
            if entity_id in self._entities:
                old_entity: Entity = self._entities[entity_id]
                old_score = old_entity.score
                old_entity.score = new_score
                old_key = (-old_score, entity_id)
                # remove entity from old score
                if old_key in self._scores: # although this be impossible
                    self._scores.remove(old_key)
                self._scores.add((-new_score, entity_id))
            else:
                self._entities[entity_id] = Entity(uid=entity_id, score=new_score)
                self._scores.add((-new_score, entity_id))

    def remove(self, entity_id: int) -> None:
        # no-op on not found
        with self._lock:
            if entity_id not in self._entities:
                return

            entity = self._entities[entity_id]
            key = (-entity.score, entity_id)
            if key not in self._scores:
                raise RuntimeError('impossible state')
            self._scores.remove(key)


    def top_k(self, k: int) -> list[Entity]:
        # get top scores
        with self._lock:
            result = []
            for (_, entity_id) in self._scores:
                if len(result) >= k:
                    break
                if entity_id not in self._entities:
                    raise RuntimeError("entity in score but not in the entities map, state should be impossible")
                result.append(self._entities[entity_id])
            return result



class TestRankManager(unittest.TestCase):
    def setUp(self):
        self.rm = RankManger()

    def test_top_k_empty_returns_empty_list(self):
        self.assertEqual(self.rm.top_k(3), [])

    def test_remove_missing_entity_is_no_op(self):
        self.rm.remove(999)
        self.assertEqual(self.rm.top_k(3), [])

    def test_insert_single_entity(self):
        self.rm.update(1, 100)

        result = self.rm.top_k(1)

        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].uid, 1)
        self.assertEqual(result[0].score, 100)

    def test_insert_multiple_entities_returns_highest_score_first(self):
        self.rm.update(1, 10)
        self.rm.update(2, 30)
        self.rm.update(3, 20)

        result = self.rm.top_k(3)

        self.assertEqual([e.uid for e in result], [2, 3, 1])
        self.assertEqual([e.score for e in result], [30, 20, 10])

    def test_top_k_smaller_than_total_entities(self):
        self.rm.update(1, 10)
        self.rm.update(2, 30)
        self.rm.update(3, 20)
        self.rm.update(4, 40)

        result = self.rm.top_k(2)

        self.assertEqual(len(result), 2)
        self.assertEqual([e.uid for e in result], [4, 2])
        self.assertEqual([e.score for e in result], [40, 30])

    def test_top_k_larger_than_total_entities(self):
        self.rm.update(1, 10)
        self.rm.update(2, 30)

        result = self.rm.top_k(10)

        self.assertEqual(len(result), 2)
        self.assertEqual([e.uid for e in result], [2, 1])
        self.assertEqual([e.score for e in result], [30, 10])

    def test_top_k_zero_returns_empty_list(self):
        self.rm.update(1, 10)
        self.rm.update(2, 20)

        result = self.rm.top_k(0)

        self.assertEqual(result, [])

    def test_duplicate_scores_are_all_returned(self):
        self.rm.update(1, 100)
        self.rm.update(2, 100)
        self.rm.update(3, 90)

        result = self.rm.top_k(3)

        self.assertEqual(len(result), 3)
        self.assertEqual([(e.uid, e.score) for e in result], [
            (1, 100),
            (2, 100),
            (3, 90),
        ])

    def test_duplicate_scores_respect_sorted_entity_ids(self):
        self.rm.update(3, 100)
        self.rm.update(1, 100)
        self.rm.update(2, 100)

        result = self.rm.top_k(3)

        self.assertEqual([e.uid for e in result], [1, 2, 3])
        self.assertEqual([e.score for e in result], [100, 100, 100])

    def test_update_existing_entity_to_higher_score(self):
        self.rm.update(1, 10)
        self.rm.update(2, 20)
        self.rm.update(1, 30)

        result = self.rm.top_k(2)

        self.assertEqual([(e.uid, e.score) for e in result], [
            (1, 30),
            (2, 20),
        ])

    def test_update_existing_entity_to_lower_score(self):
        self.rm.update(1, 100)
        self.rm.update(2, 90)
        self.rm.update(1, 80)

        result = self.rm.top_k(2)

        self.assertEqual([(e.uid, e.score) for e in result], [
            (2, 90),
            (1, 80),
        ])

    def test_update_existing_entity_to_same_score(self):
        self.rm.update(1, 100)
        self.rm.update(1, 100)

        result = self.rm.top_k(1)

        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].uid, 1)
        self.assertEqual(result[0].score, 100)

    def test_remove_existing_entity(self):
        self.rm.update(1, 100)
        self.rm.update(2, 90)
        self.rm.remove(1)

        result = self.rm.top_k(2)

        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].uid, 2)
        self.assertEqual(result[0].score, 90)

    def test_remove_one_entity_from_duplicate_score_bucket(self):
        self.rm.update(1, 100)
        self.rm.update(2, 100)
        self.rm.update(3, 90)

        self.rm.remove(1)

        result = self.rm.top_k(3)

        self.assertEqual([(e.uid, e.score) for e in result], [
            (2, 100),
            (3, 90),
        ])

    def test_remove_all_entities(self):
        self.rm.update(1, 100)
        self.rm.update(2, 90)

        self.rm.remove(1)
        self.rm.remove(2)

        self.assertEqual(self.rm.top_k(10), [])

    def test_negative_scores(self):
        self.rm.update(1, -10)
        self.rm.update(2, -5)
        self.rm.update(3, -20)

        result = self.rm.top_k(3)

        self.assertEqual([(e.uid, e.score) for e in result], [
            (2, -5),
            (1, -10),
            (3, -20),
        ])

    def test_mixed_positive_zero_and_negative_scores(self):
        self.rm.update(1, -10)
        self.rm.update(2, 0)
        self.rm.update(3, 10)

        result = self.rm.top_k(3)

        self.assertEqual([(e.uid, e.score) for e in result], [
            (3, 10),
            (2, 0),
            (1, -10),
        ])

    def test_float_scores(self):
        self.rm.update(1, 10.5)
        self.rm.update(2, 10.7)
        self.rm.update(3, 10.1)

        result = self.rm.top_k(3)

        self.assertEqual([(e.uid, e.score) for e in result], [
            (2, 10.7),
            (1, 10.5),
            (3, 10.1),
        ])

    def test_large_number_of_entities(self):
        for i in range(1000):
            self.rm.update(i, i)

        result = self.rm.top_k(5)

        self.assertEqual([(e.uid, e.score) for e in result], [
            (999, 999),
            (998, 998),
            (997, 997),
            (996, 996),
            (995, 995),
        ])

    def test_repeated_updates_do_not_create_duplicate_results(self):
        self.rm.update(1, 10)
        self.rm.update(1, 20)
        self.rm.update(1, 30)
        self.rm.update(1, 40)

        result = self.rm.top_k(10)

        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].uid, 1)
        self.assertEqual(result[0].score, 40)

    def test_top_k_after_update_and_remove_sequence(self):
        self.rm.update(1, 50)
        self.rm.update(2, 60)
        self.rm.update(3, 70)

        self.rm.update(1, 80)
        self.rm.remove(3)
        self.rm.update(4, 75)

        result = self.rm.top_k(3)

        self.assertEqual([(e.uid, e.score) for e in result], [
            (1, 80),
            (4, 75),
            (2, 60),
        ])

    def test_concurrent_updates(self):
        def worker(start, end):
            for i in range(start, end):
                self.rm.update(i, i)

        threads = [
            threading.Thread(target=worker, args=(0, 250)),
            threading.Thread(target=worker, args=(250, 500)),
            threading.Thread(target=worker, args=(500, 750)),
            threading.Thread(target=worker, args=(750, 1000)),
        ]

        for t in threads:
            t.start()

        for t in threads:
            t.join()

        result = self.rm.top_k(3)

        self.assertEqual([(e.uid, e.score) for e in result], [
            (999, 999),
            (998, 998),
            (997, 997),
        ])

    def test_concurrent_updates_same_entities(self):
        def worker(score_offset):
            for i in range(100):
                self.rm.update(i, i + score_offset)

        threads = [
            threading.Thread(target=worker, args=(0,)),
            threading.Thread(target=worker, args=(1000,)),
            threading.Thread(target=worker, args=(2000,)),
        ]

        for t in threads:
            t.start()

        for t in threads:
            t.join()

        result = self.rm.top_k(100)

        self.assertEqual(len(result), 100)
        self.assertEqual(len({e.uid for e in result}), 100)

    def test_concurrent_remove_missing_entities(self):
        def worker():
            for i in range(1000):
                self.rm.remove(i)

        threads = [threading.Thread(target=worker) for _ in range(5)]

        for t in threads:
            t.start()

        for t in threads:
            t.join()

        self.assertEqual(self.rm.top_k(10), [])


if __name__ == "__main__":
    unittest.main()
