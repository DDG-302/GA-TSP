from ui.app import Tspapp
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--epoch", type=int)
parser.add_argument("--init_size", type=int)
parser.add_argument("--p_mutation", type=float)
parser.add_argument("--size_of_population", type=int)


args = parser.parse_args()


app = Tspapp(args.epoch, args.init_size, args.p_mutation, args.size_of_population)
app.exec()




