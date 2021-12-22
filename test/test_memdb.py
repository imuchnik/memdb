import sys
import pytest
sys.path.append('../in_mem_db')

from memdb import InMemDb


class Test_memdb:

    @pytest.fixture
    def db(self):
        return InMemDb()

    def test_setget(self, db):
        db.set("a",2)
        assert db.get("a") == 2

    def test_shouldReturnNullIfNotInDB(self, db):
        assert db.get("a") == "NULL"

    def test_deleteFunction(self, db):
        db.set("a",2)
        assert db.get("a") ==2
        db.delete("a")
        assert db.get("a") =="NULL"


    def test_countFunction(self, db):
        db.set("a", 1)
        db.set("b", 1)
        db.set("c", 1)
        db.set("d", 1)
        assert db.get_count(1) == 4
        db.set("d", "foo")
        assert db.get_count(1) == 3
        assert db.get_count("foo") == 1
        db.set("c", "foo")
        assert db.get_count(1) == 2
        assert db.get_count("foo") == 2
        db.delete("a")
        assert db.get_count(1) == 1
        assert db.get_count("bar") == 0

        db.delete("b")
        assert db.get_count(1) == 0

    def test_beginTransactionSet(self, db):
        db.begin()
        assert db.get_transaction_state()
        db.set("a",  2)
        assert len(db.transactions) > 0
        assert db.transactions[-1] == [['delete', 'a']]

    def test_beginTransactionSetUpdate(self, db):
        db.set("a",  2)
        db.begin()
        assert len(db.transactions) > 0
        db.set("a",  4)
        db.set("b", 5)
        assert db.transactions[-1] == [['delete', 'b'], ['set', 'a', 2]]

    def test_beginTransactionSetUpdateNewValue(self, db):
        db.set("a",  2)
        db.begin()
        assert len(db.transactions) > 0
        db.set("a",  4)
        db.set("b", 5)
        db.delete("a")
        assert db.transactions[-1] == [['set', 'a', 4],['delete', 'b'], ['set', 'a', 2]]

    def test_transactionRollbackNoTransaction(self, db):
        res = db.rollback()
        assert res == 'T​RANSACTION NOT FOUND'

    def test_transactionRollbackReplayTransaction(self, db):
        db.set("a",  2)
        assert db.get('d') =='NULL'

        db.begin()
        assert len(db.transactions) > 0
        db.set("a",  4)
        db.set("b", 5)

        assert db.get('a')==4
        assert db.get('b') == 5
        assert db.get_count(2) == 0
        assert db.get_count(4) == 1
        assert db.get_count(5) == 1

        db.delete("a")
        assert db.get('a') == "NULL"
        assert db.get_count(4) == 0
        assert db.get_transaction_state()

        db.rollback()

        assert db.get('a') == 2
        assert db.get('b') == "NULL"
        assert not db.get_transaction_state()




    def test_transactionRollbackReplayTransactions(self, db):
        db.set("a",  2)
        db.begin()

        assert len(db.transactions) == 1
        db.set("a",  4)
        db.set("b", 5)

        assert db.get_count(2) == 0
        assert db.get_count(4) == 1
        assert db.get_count(5) == 1

        assert db.get("a") == 4
        assert db.get("b") == 5
        assert db.get("d") == 'NULL'

        db.begin()
        assert len(db.transactions) == 2
        db.set("d",  2)
        db.set("a", 5)

        assert db.get_count(2) == 1
        assert db.get_count(4) == 0
        assert db.get_count(5) == 2
        assert db.get("a") == 5
        assert db.get("b") == 5
        assert db.get("d") == 2

        db.begin()
        assert len(db.transactions) == 3
        db.set("d",  4)
        db.delete("a")
        assert db.get("a") == "NULL"
        assert db.get("b") == 5
        assert db.get("d") == 4

        assert db.get_count(2) == 0
        assert db.get_count(4) == 1
        assert db.get_count(5) == 1

        db.rollback()
        assert len(db.transactions) == 2
        assert db.get_count(2) == 1
        assert db.get_count(4) == 0
        assert db.get_count(5) == 2
        assert db.get("a") == 5
        assert db.get("b") == 5
        assert db.get("d") == 2

        db.rollback()
        assert len(db.transactions) == 1
        assert db.get_count(2) == 0
        assert db.get_count(4) == 1
        assert db.get_count(5) == 1
        assert db.get("a") == 4
        assert db.get("b") == 5
        assert db.get("d") == 'NULL'

        db.rollback()

        assert len(db.transactions) == 0
        assert db.get("a") == 2
        assert db.get("b") == 'NULL'
        assert db.get("d") == "NULL"

        assert not db.get_transaction_state()





    def test_transactionCommit(self, db):
        db.commit()
        assert not db.get_transaction_state()
