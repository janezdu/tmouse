default :
	PYTHONPATH="." luigi --module "src.pipeline.tasks" RunSimulator --route 10 --is-diesl
	# PYTHONPATH="." luigi --module "src.pipeline.tasks" RunSimulator --route 10
