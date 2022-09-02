from download_stats import pypistats




def test_recent():
	assert isinstance(pypistats.recent('shopyo'), dict)
	assert isinstance(pypistats.recent('shopyo', period='day'), dict)
	assert isinstance(pypistats.recent('shopyo', period='week'), dict)
	assert isinstance(pypistats.recent('shopyo', period='month'), dict)


def test_version():
	assert isinstance(pypistats.version('shopyo'), dict)

def test_system():
	assert isinstance(pypistats.system('shopyo'), dict)