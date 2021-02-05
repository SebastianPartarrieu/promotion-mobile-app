#   ##########
#	#		  #
#	#		  #		########      ##########	#            # 	 ##########
#	#		  #		#		#	  #			#	#  #       # #	 #		  #
#	##########		#		#     #			#	#    #   #   #	 #		  #
#	#				#	 #		  #			#	#      #	 #	 #		  #
#	#				#   #		  #			#	#			 #	 #		  #
#	#				#	  #		  #			#	#			 #	 #		  #
#	#               #       #	  ##########    #			 #   #########
#
#
#Promotion Back-end
#

SHELL	= /bin/bash
.ONESHELL:
PYTEST	= pytest

.PHONY: default
default: clean

#
# Databases
#

PG	= psql
DB	= promotion

# defaults for local tests
ENGINE	= pg
FLASK.opt	= --host="0.0.0.0"

#
# Postgres
#

.PHONY: pg
pg:
	createdb $(DB)
	$(PG) $(DB) < create.sql
	$(PG) $(DB) < data.sql

#
# cleanup
#

.PHONY: clean clean-venv
clean: stop
	pkill flask
	-dropdb $(DB)
	$(RM) app.log app.pid VERSION *~
	$(RM) -r __pycache__ .mypy_cache .pytest_cache

clean-venv:
	$(RM) -r env_promo

#
# Generated assets
#

MD2HTML	= pandoc -s -f markdown -t html

.PHONY: version html clean-html

version:
	branch=$$(git rev-parse --abbrev-ref HEAD)
	rev=$$(git log -1|head -1|cut -d' ' -f2)
	date=$$(git log -1 --date=iso8601 | sed -n 3p | cut -c 9-27 | tr ' ' 'Z')
	echo -n "$$branch $$rev $$date" > VERSION

F.md	= $(wildcard assets/*.md)
F.html	= $(F.md:%.md=%.html) $(wildcard *.html)

html: $(F.html)

%.html: %.md
	$(MD2HTML) -o $@ $<
	touch -r $< $@

clean: clean-html
clean-html:
	$(RM) $(F.html)

#
# Flask process management
#

.PHONY: run run-pg stop

run: app.pid

app.pid: pg

app.pid: version
	export FLASK_APP=app.py FLASK_ENV=development
	export APP_CONFIG='app.conf'
	flask run $(FLASK.opt) >> app.log 2>&1 &
	echo $$! > app.pid

run-pg: run

stop:
	[ -f app.pid ] && kill $$(cat app.pid)
	$(RM) app.pid

#
# Local tests
#

.PHONY: check-engine check-pg check-types check-style check

check-engine:
	echo "# Running Tests for $(ENGINE)"
	shopt -s -o errexit
	export APP_URL="http://0.0.0.0:5000"
	$(MAKE) run-$(ENGINE)
	sleep 1
	curl -s $$APP_URL/version || exit 1
	$(PYTEST) -v test.py
	$(MAKE) stop

check-pg:
	$(MAKE) ENGINE=pg check-engine

check-types:
	mypy app.py

check-style:
	flake8 --ignore=E302,E305,E402 app.py test.py

check: clean
	shopt -s -o errexit
	$(MAKE) check-types
	$(MAKE) check-style
	$(MAKE) check-pg
	$(MAKE) clean

#
# Python Virtual Env
#

venv:
	python3 -m venv env_promo
	. env_promo/bin/activate
	pip install wheel
	pip install anosql anodb flask
	pip install psycopg2
	pip install pytest requests
	pip install mypy flake8 
	pip install pyjwt
	pip install geopy
