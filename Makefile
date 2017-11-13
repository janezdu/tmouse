default :
	PYTHONPATH="." luigi --module "src.pipeline.tasks" RunSimulator --route 10 --is-diesl
	PYTHONPATH="." luigi --module "src.pipeline.tasks" RunSimulator --route 10
local :
	rm -r tmp
	PYTHONPATH="." luigi --local-scheduler --module "src.pipeline.tasks" RunSimulator --route 10 --is-diesl
	PYTHONPATH="." luigi --local-scheduler --module "src.pipeline.tasks" RunSimulator --route 10
clean:
    rm -rf ./tmp
graph:
	python ./src/plotting/plot_fuel.py
remake: 
	clean default