#!/bin/bash
for i in users ipdiag aggregate gui; do
	cd $i
	docker build --tag mkwm/siuu-tip-$i .
	docker push mkwm/siuu-tip-$i
	cd ..
done
