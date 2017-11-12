import luigi
from src.pathing.path_import import PathImporter
from src.sim.model import Simulator, SimpleDriver, Engine, Path


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


class RunSimulator(luigi.Task):
    route = luigi.IntParameter()
    is_diesl = luigi.BoolParameter()

    def output(self):
        return luigi.LocalTarget('tmp/route_{}/simulator_results_{}.json'
                .format(self.route, 'diesl' if is_diesl else 'hybrid'))

    def inputs(self):
        return {
                'schedule': 'data/routes/route_{}/schedule.csv'.format(self.route),
        }

    def requires(self):
        return CreateRouteJson(route=self.route)

    def run(self):
        schdule_csv = pandas.read_csv(self.inputs['schedule'], header=0)
        schdule = schdule.iloc[:,1].tolist()

        sim = Simulator(

