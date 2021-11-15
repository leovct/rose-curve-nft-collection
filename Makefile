## SMART CONTRACT
sc-test: # Test the smart contract code (compile + deploy to a local blockchain)
	hh compile
	hh deploy

sc-deploy: # Deploy the smart contract to the rinkeby network (ethereu testnet)
	make test
	hh deploy --network rinkeby

## SVG GENERATOR
SVG_GENERATOR = svg/rose_svg_generator.py

python-check: # Check the pythoon code
	pylint --rcfile=.pylintrc ${FILE}

generate-svgs:
	make python-check FILE=${SVG_GENERATOR}
	python3 ${SVG_GENERATOR}
