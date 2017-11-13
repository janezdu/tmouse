import luigi
import json
import pandas
from src.pathing.path_import import PathImporter
from src.sim.model import Simulator, SimpleDriver, Engine, Path, Schedule


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
                .format(self.route, 'diesl' if self.is_diesl else 'hybrid'))

    def inputs(self):
        return {
                'schedule': 'data/routes/route_{}/schedule.csv'.format(self.route),
        }

    def requires(self):
        return CreateRouteJson(route=self.route)

    def run(self):
        print("abc")
        with self.requires().output().open() as fp:
            path = Path.from_file(fp)
        schedule_csv = pandas.read_csv(self.inputs()['schedule'], header=0)
        schedule = Schedule(schedule_csv.values.tolist())

        sim = Simulator(path, SimpleDriver().run, schedule, Engine())
        print("I'm here!")
        results = sim.run(self.is_diesl)
        print("asdf")

        with self.output().open('w') as fp:
            json.dump(results, fp)
