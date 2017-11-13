<<<<<<< HEAD
default :
	rm -r tmp
	PYTHONPATH="." luigi --module "src.pipeline.tasks" RunSimulator --route 10 --is-diesl
	PYTHONPATH="." luigi --module "src.pipeline.tasks" RunSimulator --route 10
local :
	rm -r tmp
	PYTHONPATH="." luigi --local-scheduler --module "src.pipeline.tasks" RunSimulator --route 10 --is-diesl
	PYTHONPATH="." luigi --local-scheduler --module "src.pipeline.tasks" RunSimulator --route 10
=======
default:
	PYTHONPATH="." luigi --module "src.pipeline.tasks" AllReports

clean:
	rm -rf ./tmp

remake: clean default
>>>>>>> b020d3b2128ca58c039a973a0b39c53ccab1e900
