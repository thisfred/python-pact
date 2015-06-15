ACTIVATE = .venv/bin/activate
REQS = pip install -Ur requirements.txt
TESTREQS = pip install -Ur test-requirements.txt

pact-spec:
	test -d pact-specification || git clone git@github.com:bethesque/pact-specification.git && cd pact-specification && git checkout version-1.1

venv: requirements.txt
	test -d .venv || virtualenv -p python3 .venv
	. $(ACTIVATE); $(REQS)
	. $(ACTIVATE); $(TESTREQS)
	. $(ACTIVATE); $(DEVREQS)
	. $(ACTIVATE); $(INSTALL)
	touch $(ACTIVATE)

vpytest:
	. $(ACTIVATE); py.test -rf -l -s -x  --cov-report term-missing --doctest-glob=*.rst --cov pact

lint: venv
	. $(ACTIVATE); flake8 --max-complexity=10 pact tests

clean:
	rm -rf .venv

test: pact-spec venv vpytest lint
