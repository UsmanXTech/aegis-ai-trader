from aegis.walk_forward import make_walk_forward_windows


def test_walk_forward_sorts_and_splits() -> None:
    data = [(f"2026-01-0{i}T00:00:00Z", i) for i in range(6, 0, -1)]
    windows = make_walk_forward_windows(data, train_size=2, validation_size=2, test_size=2)
    assert len(windows) == 1
    assert [x[1] for x in windows[0].train] == [1, 2]
    assert [x[1] for x in windows[0].validation] == [3, 4]
    assert [x[1] for x in windows[0].test] == [5, 6]


def test_walk_forward_multiple_rolling_windows() -> None:
    data = [(f"2026-01-{i:02d}T00:00:00Z", i) for i in range(1, 13)]
    windows = make_walk_forward_windows(data, train_size=4, validation_size=2, test_size=2, step=2)
    assert len(windows) == 4
    assert windows[-1].test[-1][1] == 12
