## SMART CONTRACT
TAG = all # [mock, svg, rsvg]
NETWORK = localhost

solidity-check:
	hh compile

deploy-smart-contract:
	make solidity-check
	hh deploy --tags ${TAG} --network ${NETWORK}

## SVG GENERATOR
SVG_GENERATOR = svg/rose_svg_generator.py

python-check:
	pylint --rcfile=.pylintrc ${FILE}

generate-svgs:
	make python-check FILE=${SVG_GENERATOR}
	python3 ${SVG_GENERATOR}
