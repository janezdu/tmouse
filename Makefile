default :
	PYTHONPATH="." luigi --module "src.pipeline.tasks" RunSimulator --route 10 --is-diesl
	PYTHONPATH="." luigi --module "src.pipeline.tasks" RunSimulator --route 10
local :
	rm -r tmp
	PYTHONPATH="." luigi --local-scheduler --module "src.pipeline.tasks" RunSimulator --route 17 --is-diesl
	PYTHONPATH="." luigi --local-scheduler --module "src.pipeline.tasks" RunSimulator --route 17
all :
    PYTHONPATH="." luigi --local-scheduler --module "src.pipeline.tasks" AllReports
