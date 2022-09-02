from download_stats.pepy import stats


def test_stat():

	assert isinstance(stats('shopyo'), dict)