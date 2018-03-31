# coding=utf-8
import os
import sys
sys.path.append('Functions/')
sys.path.append('Ops/')
sys.path.append('Outils/')
sys.path.append('Databases/')
sys.path.append('Architectures/')

from outils import load_autopilot, get_commands
import architectures
import vehicles 
import argparse
import warnings
warnings.filterwarnings("ignore")

models_path = '/Models'

parser = argparse.ArgumentParser(description='Axionaut')
parser.add_argument('--mode', default='self_driving', help='self_driving, records or training') # PoSelf driving, Record, Training
parser.add_argument('--architecture', default='ConvNets', help='ConvNets or ConvLSTM')
parser.add_argument('--tl', default='transfer_learning', help='Weights initialization - Random or Transfer Learning')
parser.add_argument('-e', '--epochs', default=150, type=int)
parser.add_argument('-b', '--batch_size', default=64, type=int)
parser.add_argument('-op', '--optimizer', default='Adam')


args = parser.parse_args()


if (args.mode == 'self_driving'):
    print('Vehicle started in self driving mode.')

    # Load self-driving pre-train model
    model, graph = load_autopilot('autopilot_500k.hdf5')

    print('Model loaded...')

    # Create Axionaut car with default settings
    axionaut = vehicles.Axionaut()

    # Configure PDW control commands as default
    axionaut.commands = get_commands(path=None, default=True)

    # Test camera position
    axionaut.camera_test()

    print('Hardware configured...')

    # Set Axionaut to auto pilot mode / Wrap driving model to vehicle
    axionaut.autopilot(model, graph)

    # Start Axtionaut :)
    raw_input('Self self_driving started. Pres any key to start driving. Press Crtl + C to exit.')
    
    axionaut.start()

elif(args.mode == 'training'):

    print('Vehicle started in training mode.')

    # Create Axionaut car with default settings
    axionaut = Axionaut()

    # Configure PDW control commands as default
    axionaut.commands = get_commands(path=None, default=True)

    # Training mode started with Transfer Learning
    if (args.tl == True):

        # Load self-driving pre-trained model
        model, graph = load_model('autopilot_500k.hdf5')

        # Freeze all no convolutional layers
        #for layer in model.layers:
        #  layer.trainable = False

        # Training routine
        print('Training routine started with transfer learning. Press Crtl + C to exit.')

        history, model = axionaut.train(model, graph, transfer_learning=True, 
                        epochs=args.epochs, 
                        batch_size=args.batch_size,
                        optimizer=args.optimizer)

        outils.plot_losses(history)

        print('trained finished. Model saved')

    else:
        if args.arch == 'ConvNets':
            # Create a new ConvNet model from library
            model =  architectures.ConvNets()

            # Train model
            history, model = model.train(model, graph, transfer_learning=True, 
                          epochs=args.epochs, 
                          batch_size=args.batch_size,
                          optimizer=args.optimizer)

            outils.plot_losses(history)

            print('trained finished. Model saved')

        else:

            # Create a new ConvNet model from library
            model =  architectures.ConvNets()

            # Train model
            history, model = model.train(model, graph, transfer_learning=True, 
                          epochs=args.epochs, 
                          batch_size=args.batch_size,
                          optimizer=args.optimizer)

            print('Architecture ConvLSTM')

else:
    print('Vehicle started in Record model')