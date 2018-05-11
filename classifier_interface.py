#!/usr/bin/env python

"""
Front-facing API for classifier
"""

import argparse
import os, os.path
import csv

import classifier


parser = argparse.ArgumentParser(
    description='Sasquatch SVRT classifier.',
    #formatter_class = argparse.ArgumentDefaultsHelpFormatter
)

parser.add_argument('problems',
                    type = int,
                    nargs = '*',
                    help = 'Problem number')

parser.add_argument('--parsed_data_dir',
                    type = str,
                    required = True,
                    help = 'Directory containing all problems as parsed'
                           ' strings')

parser.add_argument('--output_dir',
                    type = str,
                    default = 'output',
                    help = 'Directory where output accuracies should be'
                           ' recorded')

parser.add_argument('--classifier',
                    type = str,
                    choices = ['bayesian', 'non_bayesian'],
                    default = 'bayesian',
                    help = 'Which classifier to use')

parser.add_argument('-n', '--nb_training_samples',
                    type = int,
                    default = 3,
                    help = 'Number of both positive and negative training'
                           ' examples (total number of samples twice the'
                           ' supplied value for N).')

parser.add_argument('-s', '--nb_repetitions',
                    type = int,
                    default = 20,
                    help = 'How many models to build')

parser.add_argument('--classes_by',
                    type = str,
                    choices = ['dir', 'fname'],
                    default = 'dir',
                    help = 'How classes are distinguished')

######################################################################

args = parser.parse_args()

if args.classifier == 'bayesian':
    fn = classifier.Bayesian_classifier
elif args.classifier == 'non_bayesian':
    fn = classifier.classifier_accuracies
else:
    raise ValueError('Bad classifier specified: {}'.format(args.classifier))

if not os.path.isdir(args.output_dir):
    os.makedirs(args.output_dir)

for problem in args.problems:
    if args.classes_by == 'fname':
        raise NotImplementedError(
            "Can't handle classes distinguished within filenames")
    elif args.classes_by == 'dir':
        base_dir = os.path.join(args.parsed_data_dir,
                                'problem_{:02d}'.format(problem))
        positive_dir = os.path.join(base_dir, 'class_1')
        positive_paths = [os.path.join(positive_dir, path)
                          for path in sorted(os.listdir(positive_dir))]
        negative_dir = os.path.join(base_dir, 'class_0')
        negative_paths = [os.path.join(negative_dir, path)
                          for path in sorted(os.listdir(negative_dir))]
    else:
        raise ValueError('Bad class distinguisher specified: {}'.format(
            args.classifier))

    accuracies = fn(positive_paths,
                    negative_paths,
                    N=args.nb_training_samples,
                    S=args.nb_repetitions)

    dirname = os.path.join(args.output_dir,
                           args.parsed_data_dir,
                           args.classifier)
    if not os.path.isdir(dirname):
        os.makedirs(dirname)
    fname = 'accuracies_problem_{:02d}_N={}_S={}.csv'.format(
        problem,
        args.nb_training_samples,
        args.nb_repetitions)

    with open(os.path.join(dirname, fname), "w") as f:
        cw = csv.writer(f)
        cw.writerow(accuracies)
