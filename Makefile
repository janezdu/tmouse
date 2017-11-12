default:
	PYTHONPATH="." luigi --module "src.pipeline.tasks" AllReports

clean:
	rm -rf ./tmp

remake: clean default
