import pyrocksdb
import tempfile
import pytest

#  foo = pyrocksdb.get_foo()
#  del foo

#  class Cat(pyrocksdb.Animal):
    #  def go(self, n_times):
        #  print ('aaa')
        #  return "meow! " * n_times

#  c = Cat()
#  pyrocksdb.call_go(c)

#  a = pyrocksdb.Animal()
#  a.vvv()


@pytest.fixture
def db():
    db = pyrocksdb.DB()
    opts = pyrocksdb.Options()
    opts.IncreaseParallelism()
    opts.OptimizeLevelStyleCompaction()
    opts.create_if_missing = True
    tmp = tempfile.TemporaryDirectory()
    s = db.open(opts, tmp.name)
    assert s.ok()
    yield db
    db.close()

@pytest.fixture
def transaction_db():
    opts = pyrocksdb.Options()
    opts.create_if_missing = True
    txn_db_opts = pyrocksdb.TransactionDBOptions()
    tmp = tempfile.TemporaryDirectory()
    db = pyrocksdb.transaction_db()
    s = db.open(opts, txn_db_opts, tmp.name)
    assert(s.ok())
    yield db
    db.close()

#  #  def test_option():
    #  #  opts = pyrocksdb.Options()
    #  #  assert opts.create_if_missing == False
    #  #  assert opts.error_if_exists == False


#  #  def test_put_get(db):
    #  #  opts = pyrocksdb.WriteOptions()
    #  #  s = db.put(opts, b"key1", b"value1")
    #  #  assert s.ok()
    #  #  opts = pyrocksdb.ReadOptions()
    #  #  blob = db.get(opts, b"key1")
    #  #  assert blob.status.ok()
    #  #  assert blob.data == b'value1'

#  #  def test_delete(db):
    #  #  opts = pyrocksdb.WriteOptions()
    #  #  s = db.put(opts, b"key1", b"value1")
    #  #  assert s.ok()
    #  #  opts = pyrocksdb.ReadOptions()
    #  #  blob = db.get(opts, b"key1")
    #  #  assert blob.status.ok()
    #  #  assert blob.data == b'value1'
    #  #  opts = pyrocksdb.WriteOptions()
    #  #  s = db.delete(opts, b"key1")
    #  #  assert s.ok()
    #  #  opts = pyrocksdb.ReadOptions()
    #  #  blob = db.get(opts, b"key1")
    #  #  assert not blob.status.ok()

#  #  def test_iterator(db):
    #  #  opts = pyrocksdb.WriteOptions()
    #  #  s = {b'key1': b'value1', b'key2': b'value2', b'key3': b'value3'}
    #  #  for k, v in s.items():
        #  #  db.put(opts, k, v)

    #  #  opts = pyrocksdb.ReadOptions()
    #  #  it = db.iterator(opts)
    #  #  it.seek_to_first()
    #  #  assert it.status().ok()
    #  #  assert it.valid()
    #  #  for k, v in s.items():
        #  #  assert it.key() == k
        #  #  assert it.value() == v
        #  #  it.next()

    #  #  assert not it.valid()

    #  #  it.seek(b'key1')
    #  #  assert it.valid()
    #  #  assert it.key() == b'key1'
    #  #  assert it.value() == b'value1'
    #  #  it.seek(b'key2')
    #  #  assert it.valid()
    #  #  assert it.key() == b'key2'
    #  #  assert it.value() == b'value2'

    #  #  it.seek(b'key4')
    #  #  assert not it.valid()

    #  #  it.seek_for_prev(b'key0')
    #  #  assert not it.valid()
    #  #  it.seek_for_prev(b'key4')
    #  #  assert it.valid()

#  #  def test_write_batch(db):
    #  #  update = pyrocksdb.WriteBatch()

    #  #  update.put(b'key1', b'value1')
    #  #  update.put(b'key2', b'value2')
    #  #  update.delete(b'key1')
    #  #  opts = pyrocksdb.WriteOptions()
    #  #  s = db.write(opts, update)
    #  #  assert s.ok()
    #  #  opts = pyrocksdb.ReadOptions()
    #  #  blob = db.get(opts, b'key1')
    #  #  assert blob.status.is_not_found()
    #  #  blob = db.get(opts, b'key2')
    #  #  assert blob.status.ok()
    #  #  assert blob.data == b'value2'

#  def test_transaction_db():
    #  opts = pyrocksdb.Options()
    #  opts.create_if_missing = True
    #  txn_db_opts = pyrocksdb.TransactionDBOptions()
    #  tmp = tempfile.TemporaryDirectory()
    #  db = pyrocksdb.transaction_db()
    #  s = db.open(opts, txn_db_opts, tmp.name)
    #  assert(s.ok())
    #  wopts = pyrocksdb.WriteOptions()
    #  txn = db.begin_transaction(wopts)
    #  assert(txn)
    #  ropts = pyrocksdb.ReadOptions()
    #  blob = txn.get(ropts, b'key1')
    #  assert(blob.status.is_not_found())
    #  del txn

    #  txn = db.begin_transaction(wopts)
    #  s = txn.put(b'key1', b'value1')
    #  assert(s.ok())
    #  s = txn.put(b'key2', b'value2')
    #  assert(s.ok())
    #  blob = txn.get(ropts, b'key1')
    #  assert(blob.status.ok())
    #  assert(blob.data == b'value1')

    #  # the data won't be written unitl the commit
    #  blob = db.get(ropts, b'key1')
    #  assert(blob.status.is_not_found())

    #  s = db.put(wopts, b'key3', b'value3')
    #  assert(s.ok())

    #  s = db.put(wopts, b'key1', b'value1')
    #  assert(not s.ok())

    #  s = txn.commit()
    #  assert(s.ok())
    #  del txn

    #  txn_opts = pyrocksdb.TransactionOptions()
    #  txn_opts.set_snapshot = True
    #  txn = db.begin_transaction(wopts, txn_opts)
    #  snapshot = txn.get_snapshot()
    #  del txn

def test_transaction_snapshot(transaction_db):
    db = transaction_db

    wopts = pyrocksdb.WriteOptions()
    txn_opts = pyrocksdb.TransactionOptions()
    txn_opts.set_snapshot = True
    txn = db.begin_transaction(wopts, txn_opts)
    snapshot = txn.get_snapshot()

    # Write a key OUTSIDE of transaction
    s = db.put(wopts, b'abc', b'xyz')
    assert(s.ok())

    #  Attempt to read a key using the snapshot.  This will fail since
    #  the previous write outside this txn conflicts with this read.
    ropts = pyrocksdb.ReadOptions()
    ropts.snapshot = snapshot
    blob = txn.get_for_update(ropts, b"abc")
    assert(blob.status.is_busy());

    # Discard all batched writes in this transaction.

    txn.rollback()
    # be sure to clear the snapshot
    txn.clear_snapshot()

    del txn

def test_transaction_read_commited(transaction_db):


    #  "Read Committed" (Monotonic Atomic Views) Example
    #  --Using multiple Snapshots

    #  In this example, we set the snapshot multiple times.  This is probably
    #  only necessary if you have very strict isolation requirements to
    #  implement.

    #  opts = pyrocksdb.Options()
    #  opts.create_if_missing = True
    #  txn_db_opts = pyrocksdb.TransactionDBOptions()
    #  tmp = tempfile.TemporaryDirectory()
    #  db = pyrocksdb.transaction_db()
    #  s = db.open(opts, txn_db_opts, tmp.name)
    #  assert(s.ok())
    db = transaction_db

    # Set a snapshot at start of transaction
    wopts = pyrocksdb.WriteOptions()
    txn_opts = pyrocksdb.TransactionOptions()
    txn_opts.set_snapshot = True
    txn = db.begin_transaction(wopts, txn_opts)
    snapshot = txn.get_snapshot()

    #  Do some reads and writes to key "x"
    ropts = pyrocksdb.ReadOptions()
    ropts.snapshot = snapshot
    blob = txn.get(ropts, b"x");
    assert(blob.status.is_not_found())
    txn.put(b"x", b"x")
    # Do a write outside of the transaction to key "y"
    s = db.put(wopts, b"y", b"y");
    assert(s.ok())


    #  Set a new snapshot in the transaction
    txn.set_snapshot();
    txn.set_savepoint();
    ropts.snapshot = db.get_snapshot();


    # Do some reads and writes to key "y"
    #  Since the snapshot was advanced, the write done outside of the
    #  transaction does not conflict.
    blob = txn.get_for_update(ropts, b"y")
    assert(blob.status.ok())
    assert(blob.data == b'y')
    txn.put("y", "y");


    # Decide we want to revert the last write from this transaction.
    txn.rollback_to_savepoint()

    # Commit.
    s = txn.commit()
    assert(s.ok())
    del txn;
    # Clear snapshot from read options since it is no longer valid
    db.release_snapshot(ropts.snapshot)
