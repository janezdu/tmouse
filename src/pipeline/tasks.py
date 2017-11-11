import luigi
from src.pathing.path_import import PathImporter


class CreateRouteJson(luigi.Task):
    route = luigi.IntParameter()

    def output(self):
        return luigi.LocalTarget('tmp/route_{}/path.json'.format(self.route))

    def inputs(self):
        return {
                'path': 'data/routes/route_{}/path.gpx'.format(self.route),
                'stops': 'data/routes/route_{}/stops.csv'.format(self.route)
        }

    def run(self):
        input = self.inputs()
        importer = PathImporter(input['path'], input['stops'])
        with self.output().open('w') as fp:
            importer.run(fp)

