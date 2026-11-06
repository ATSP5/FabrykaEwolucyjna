from CUDAKernelLoader import CUDAKernelLoader
from PolishNumberFormat import PolishNumberFormat
from FactoryCatalog import FactoryCatalog
from OrderStreamGenerator import OrderStreamGenerator
from ProblemEncoder import ProblemEncoder
from PriorityRuleSeeder import PriorityRuleSeeder
from PopulationInitializer import PopulationInitializer
from EvolutionEngine import EvolutionEngine
from ScheduleDecoder import ScheduleDecoder
from ScheduleAnalysis import ScheduleAnalysis
from AnalysisFileWriter import AnalysisFileWriter
from FactoryDashboard import FactoryDashboard


def main():
	catalog = FactoryCatalog()
	number_format = PolishNumberFormat()
	loader = CUDAKernelLoader()

	machines = catalog.machines()
	recipes = catalog.recipes()
	formatter = number_format.formatter()
	orders = OrderStreamGenerator(machines, recipes).orders()
	problem = ProblemEncoder(machines, recipes, orders).problem()
	seeds = PriorityRuleSeeder(problem).seeds()
	initializer = PopulationInitializer(problem, seeds)
	engine = EvolutionEngine(loader.evaluate_schedules(), loader.breed_generation(), loader.replace_survivors(),
	                         problem, initializer.population(), initializer.params(), formatter)
	result = engine.result()
	schedules = ScheduleDecoder(problem, result, seeds).schedules()
	report = ScheduleAnalysis(problem, result, schedules).report()
	writer = AnalysisFileWriter(machines, recipes, orders, report)
	dashboard = FactoryDashboard(writer.input_tables(), result, report, writer.written_paths(), formatter)
	dashboard.show()


if __name__ == "__main__":
	main()
